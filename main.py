from flask import Flask, render_template, redirect, url_for, request
import admin, security, models, search
from database import db, sqlite_str
from flask_admin import helpers as admin_helpers
from flask_security import logout_user

import lib

# fixing encoding temporarily
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')


app = Flask(__name__)


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
	return render_template('app_index.html')

@app.route('/')
def index():
	return redirect(url_for('main_app'))

@app.route('/app/show-restos/', methods=['POST'])
def resto():
	# find 3 restaurants
	print "what is happening???????????????????????????????????????????"
        loc = request.form['location']
	print loc
        dist = search.radius(int(request.form['foot']), int(request.form['bike']), int(request.form['car']))
        print dist
        restos = search.search(loc, dist)
	print restos
        for r in restos:
            print r[1]
            print r[1].foldername()
            print r[1].img()
        return render_template('app_restos.html', restaurants=restos)


@app.route('/user/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

# @security.context_processor
# def security_context_processor():
# 	return dict(
# 		admin_base_template=admin.base.template,
# 		admin_view=admin.index_view,
# 		h=admin_helpers,
# 		get_url=url_for
# 		)


configurate_app()

if __name__ == '__main__':
	app.run(debug=True)
