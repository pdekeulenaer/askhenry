from flask import url_for, redirect, request, abort
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.model import BaseModelView
from flask_security import current_user

from database import db
import models
import lib.geocode

def initialize(app):
	# admin.add_view(ManagementView(name="Antwerp", endpoint='restos/antwerp', category='Restaurants'))
	# admin.add_view(ManagementView(name="Brussels", endpoint='restos/brussels', category='Restaurants'))
	admin.add_view(RestoAdminView(models.Restaurant, db.session))
	admin.add_view(ModelView(models.City, db.session))
	admin.add_view(MapView(name='Map', endpoint='map'))
	admin.init_app(app)
	return admin

class AdminModelView(ModelView):
	def is_accessible(self):
		if not current_user.is_active or not current_user.is_authenticated:
			return False

		if current_user.has_role('superuser'):
			return True

		return False

	def _handle_view(self, name, **kwargs):
		if not self.is_accessible():
			if current_user.is_authenticated:

				abort(403)
			else:
				return redirect(url_for('security.login', next=request.url))


class MyAdminView(BaseView):
	@expose('/')	
	def index(self):
	    if not current_user.is_authenticated:
	        return redirect(url_for('security.login', next=request.url))
	    return self.render('admin/index.html')

class RestoAdminView(AdminModelView):
	form_excluded_columns = ('longitude', 'latitude',)
	form_widget_args = {
		'last_updated' : {
			'disabled' : True
		}
	}

	# Method to update the model with (lat, lng) coordinates based on the address
	# So the user does not have to enter these herself
	def on_model_change(self, form, model, is_created):
		addr = model.address
		(lat, lng) = lib.geocode.latlng(addr)
		model.latitude = lat
		model.longitude = lng

class MapView(BaseView):
	@expose('/')
	def index(self):
		restos = models.Restaurant.query.all()
		res = []

		for r in restos:
			x = {}
			x['lng'] = r.longitude
			x['lat'] = r.latitude
			x['name'] = r.name
			res.append(x)

		return self.render('admin_map.html', restos=res)

	def is_accessible(self):
		if not current_user.is_active or not current_user.is_authenticated:
			return False

		if current_user.has_role('superuser'):
			return True

		return False

	def _handle_view(self, name, **kwargs):
		print current_user.is_authenticated
		print current_user.is_active
		if not self.is_accessible():
			if current_user.is_authenticated:
				abort(403)
			else:
				return redirect(url_for('security.login', next=request.url))

admin = Admin(name="Master Henry", index_view=MyAdminView(url='/admin', static_folder='../static', endpoint='admin'))