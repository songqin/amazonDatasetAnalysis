#!/usr/bin/python
import json
import gzip
import sys
from pymongo import MongoClient
import unicodedata
import time
start_time = time.time()
debug=0
createTempTable=1
createReviewTable=1
def parse(path):
	g=gzip.open(path, 'r')
	for l in g:
		yield eval(l)

print sys.argv[1]

n=0
client = MongoClient("localhost:27017")
# use a database named amazon1
client.drop_database('test2')
db = client.test2
products=[]#products reviewed by top10000 reviewers
# get top10000 reviewer's uid
if(createTempTable):
	with open('top10000.txt', 'r') as f:
		content = f.readlines()
	content = [x.strip('\n') for x in content]
	content = [x.split(' ')[1] for x in content] #http://www.amazon.com/gp/pdp/profile/A1TWM78I835NGZ
	top10000 = [x.split('profile/')[1] for x in content] #A1TWM78I835NGZ
	# a file with the pid ( with duplicates) of the products 
	# reviewed by top 10000 reviewers
	# f1=open('pidTop10000.txt', 'w')
	db.tempTable.remove()
	db.reviewTable.remove()
	# create table (tempTable) and a file of pid (pidTop10000.txt)
	for review in parse(sys.argv[1]):
		n+=1
		uid = review["reviewerID"]
		pid = review["asin"]
		s = review["overall"]
		t = review["reviewText"]
		# create a number of reviews reviewed only by top100000
		if(uid in top10000):
			record = {
			'uid': uid,
			'pid': pid,
			'score': s
			# ,
			# 'text': t
			}

			# print record
			db.tempTable.insert(record)
			if (pid not in products):
				products.append(pid)
			# f1.write(pid+'\n')
		if(debug):
			if(n==1000):
				break

	# f1.close()
	# to use aggregate, you need a newer version of mongodb. I'm using 3.0.12
	results = db.tempTable.aggregate([{
		"$group":{
		"_id": "$pid",
		"avg": {"$avg":"$score"}
		}}])
	dict={}
	for record in results:
		pid =  record['_id']
		ave = record['avg']
		dict[pid] = ave
	# add average score field to table
	# for k in dict:
	# 	# result = db.tempTable.find({pid:key})
	# 	# print result
	# 	v=dict[k]
	# 	db.tempTable.update(
	# 		{'pid':k},
	# 		{
	# 			'$set':{
	# 				'ave': v
	# 			}
	# 		},
	# 			upsert = False,		
	# 			multi=  True
	# 	)

if(createReviewTable):
	print 'create review table'
	# print 'dict', dict
	# with open('pidTop10000.txt', 'r') as f:
	# 	products = f.readlines()
	# products = [x.strip('\n') for x in products]

	# print "products", products
	# print "top10000", top10000
	n=0
	tt=tf=ft=ff=0 #cpt for reliability and eligibility
	for review in parse(sys.argv[1]):
		n+=1
		pid = review["asin"]
		if(pid in products):
			uid = review["reviewerID"]
			s = review["overall"]
			t = review["reviewText"]
			ave = dict[pid]
			# t ?
			if((uid in top10000) or (s>3 and ave>3) or (s<=3 and ave<=3)):
				if(ave>3):
					tt+=1
				else:
					tf+=1
			else:
				if(ave>3):
					ft+=1
				else:
					ff+=1

			# r = db.tempTable.find({"pid": pid}, {"ave" :1 })
			# if(r):
			# 	ave = r[0]["ave"]
			# record = {
			# 'uid': uid,
			# 'pid': pid,
			# 'score': s
			# ,'ave' : ave
			# ,
			# 'text': t
			# }
			# print record
			# db.reviewTable.insert(record)
		if(debug):
			if(n==1000):
				break
# print db.reviewTable.count()
print db.command("dbstats")
client.close()
print 'tt', tt
print 'tf', tf
print 'ft', ft
print 'ff', ff
all = tt+tf+ft+ff
print 'all', all
print tt*1.0/all
print tf*1.0/all
print ft*1.0/all
print ff*1.0/all
print("--- %s seconds ---" % (time.time() - start_time))