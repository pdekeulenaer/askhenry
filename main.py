from flask import Flask, render_template, redirect, url_for
import admin, security, models
from database import db, sqlite_str
from flask_admin import helpers as admin_helpers
from flask_security import logout_user

app = Flask(__name__)


def configurate_app():
	app.secret_key = 'herebemysecretkey'
	app.config['SESSION_TYPE'] = 'filesystem'
	app.config['SQLALCHEMY_DATABASE_URI'] = sqlite_str()
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	
	security.initialize(app)
	admin.initialize(app)

	db.init_app(app)
	app.app_context().push()

@app.route('/')
def index():
	return 'Hello'

@app.route('/app/')
def main():
	return render_template('hello_gradient.html')

@app.route('/app/resto/')
def resto():
	return render_template('restaurant.html')

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

if __name__ == '__main__':
	configurate_app()
	app.run(debug=True)