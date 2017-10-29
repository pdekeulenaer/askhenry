import slugify
import os

# string utilities
# decodes a string to unicode, creates a 'slug' and then encodes it
# slug uses a machine readable string (e.g., "I am Philip$", becomes "i-am-philip")
def cleanstr(s):
	if type(s) is not unicode: 
		s = s.decode()

	return slugify.slugify(s).encode()

def listfiles(s):
	files = []
	for f in os.listdir(os.getcwd() + s):
		files.append(f)
		print type(f)

	return files