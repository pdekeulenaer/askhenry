import main
import lib
import models

import os

restos = models.Restaurant.query.all()
# base = os.getcwd() + "\\static\\img\\restaurants\\"

# for r in restos:
# 	path = r.foldername()
# 	pn = base + path + '\\'

# 	if not os.path.exists(pn):
# 		print "creating"
# 		os.makedirs(pn)
# 	else:
# 		print "exists"


# lib.util.listfiles(os.getcwd() + '\\static\\img\\restaurants\\1-billies-bier-kafetaria')

for r in restos:
	print r.img()
	print type(r.img())