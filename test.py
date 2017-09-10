import math

def calc_pq(a,b):
	pq = math.sqrt((b-a)**2 + ((b*b)-(a*a))**2)
	return pq

def calc_rs(a,b):
	rs = math.sqrt( (b-a)**2 + ( (b*b)/4 - (a*a)/4 )**2)
	return rs

r = range(0,10000)
r = map (float, r)
r = map(lambda l: l/10.0, r)

# for i in r:
# 	print "I is: " + str(i)
# 	for j in r:
# 		rs = calc_rs(i,j)
# 		pq = calc_pq(i,j)

# 		if pq > 0:
# 			delta = pq / rs
# 			print delta
# 			if delta > 3.5 and delta < 4.5:
# 				print ("%d, %d, %d" % (rs, pq, delta))


a = 1
b = 100000000000000

pq = calc_pq(a,b)
rs = calc_rs(a,b)

print ("%d, %d, %d" % (rs, pq, float(pq/rs)))