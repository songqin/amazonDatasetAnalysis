#!/usr/bin/python
import json
import gzip
import sys
def parse(path):
	g=gzip.open(path, 'r')
	for l in g:
		yield eval(l)

print sys.argv[1]

n=0
debug=1
for review in parse(sys.argv[1]):
	n+=1
	print review
	reviewer = review["reviewerID"]
	print reviewer
	print ''
	if(debug):
		if(n==10):
			break