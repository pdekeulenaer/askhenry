import ConfigParser

_CFG_FILE = 'CONFIG.CFG'

def load():
	config = ConfigParser.RawConfigParser()
	config.read(_CFG_FILE)
	return config

def create_default():
	config = ConfigParser.RawConfigParser()

	config.add_section('DATABASE')
	config.set('DATABASE', 'DB_TYPE', 'sqlite')

	f = open(_CFG_FILE, 'wb')
	config.write(f)
	f.close()

_config = load()
DB_TYPE = _config.get('DATABASE', 'DB_TYPE')
DB_NAME = _config.get('DATABASE', 'DB_NAME')