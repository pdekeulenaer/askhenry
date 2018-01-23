import json
from flask import Flask, render_template, redirect, url_for, request, session
import admin, security, models, search
from database import db, sqlite_str
from flask_admin import helpers as admin_helpers
from flask_security import logout_user

from flask_sslify import SSLify

import lib
import tracer

# fixing encoding temporarily
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

app = Flask(__name__)
sslify = SSLify(app)

def configurate_app():
	app.secret_key = 'herebemysecretkey'
	app.config['SESSION_TYPE'] = 'filesystem'
	app.config['SQLALCHEMY_DATABASE_URI'] = sqlite_str()
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	app.config['SECURITY_REGISTERABLE'] = True
	app.config['SECRET_KEY'] = 'youcanaskhenryanythinganytime'
	app.config['SESSION_COOKIE_SECURE'] = False
	app.config['WTF_CSRF_ENABLED'] = False
	(security_ctx, user_datastore) = security.initialize(app)
	admin_ctx = admin.initialize(app)


	@security_ctx.context_processor
	def security_context_processor():
	    return dict(
	        admin_base_template=admin_ctx.base_template,
	        admin_view=admin_ctx.index_view,
	        h=admin_helpers,
                get_url=url_for
	    )

	db.init_app(app)
	app.app_context().push()


@app.route('/app/')
def main_app():
	tracer.open_session()
	return render_template('app_index.html')

@app.route('/')
def index():
	return redirect(url_for('main_app'))

@app.route('/app/show-restos/', methods=['POST'])
def resto():
	# find 3 restaurants
    loc = request.form['location']
    dist = search.radius(int(request.form['foot']), int(request.form['bike']), int(request.form['car']))
    algo = search.balancedAlg()

    # Apply genre filter
    if int(request.form['breakfast']) == 1:
    	genre = 'breakfast'
    	algo = search.basicAlg().add(search.BreakfastFilter())
    elif int(request.form['lunch']) == 1:
    	genre = 'lunch'
    	algo = search.basicAlg().add(search.LunchFilter())
    else:
    	genre = 'dinner'

    # setting up the tracer
    # TODO - abstract into method
    t = models.Trace()
    t.transport = (request.form['foot'])+(request.form['bike'])+(request.form['car'])
    t.food_type = genre

    restos = search.search(loc, dist, algo, t)
    t.resto1 = restos[0][1].id
    t.resto2 = restos[1][1].id
    t.resto3 = restos[2][1].id
    t.session_id = session['uuid']

    db.session.add(t)
    db.session.commit()

    tracer.set_tracer(t)

    # render the output
    return render_template('app_restos.html', restaurants=restos)


@app.route('/app/api/make_choice', methods=['POST'])
def make_choice():
	choice = int(request.json['choice'])
	tracer.set_choice(choice)
	
	return json.dumps({'status':'OK'})

@app.route('/app/api/add_email', methods=['POST'])
def add_email():
	email = str(request.json['email'])
	tracer.set_email(email)	
	return json.dumps({'status':'OK'})

@app.route('/app/api/close_trace', methods=['POST'])
def close_trace():
	tracer.close_trace()
	return json.dumps({'status':'OK'})


@app.route('/user/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

configurate_app()
if __name__ == '__main__':
	app.run(debug=True)
