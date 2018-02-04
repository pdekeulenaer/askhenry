import models
from  lib.util import log
from flask import session
from database import db
import uuid

# A module to keep track of users and their activities on the site

def open_session():
	if 'uuid' in session:
		log('uuid registered: %s' % (str(session['uuid'])))
	else:
		session['uuid'] = generate_uuid()
		session.permanent = True

def session_has_email():
	if 'email' in session:
		return True
	return refresh_email_from_trace()

def refresh_email_from_trace():
	if 'uuid' in session:
		res = models.Trace.query.filter(models.Trace.email.isnot(None)).filter_by(session_id=session['uuid']).order_by(models.Trace.timestamp.desc()).first()
		if res is None:
			return False
	session['email'] = res.email
	return True


def session_set_email(email):
	if session_has_email():
		log('overwriting email %s' % (session['email']))	
	log('setting up email')
	session['email'] = email

def close_session():
	session.clear()

def set_tracer(t):
	session['active_trace'] = t.id
	log("active trace id: " + str(session['active_trace']))

def close_trace():
	session.pop('active_trace', None)
	log("tracer closed")

def get_trace():
	if 'active_trace' not in session:
		log("No active trace found")
		return

	tid = session['active_trace']
	trace = models.Trace.query.get(tid)
	if trace is None:
		log("ERR Trace is empty")
		return

	return trace


def set_choice(chosen_id):
	log("Updating tracer choice to " + str(chosen_id))
	trace = get_trace()	

	trace.choice = chosen_id
	db.session.add(trace)
	db.session.commit()
	log("tracer updated")

def set_email(email):
	trace = get_trace()
	trace.email = email
	db.session.add(trace)
	db.session.commit()

# Helper functions
def generate_uuid():
	return str(uuid.uuid4())

def describe_session():
	for (k,v) in session.items():
		print "%s  :  %s" % (k,v)

