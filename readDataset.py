#!/usr/bin/python
import json
import gzip
import sys
from pymongo import MongoClient
import unicodedata
def parse(path):
	g=gzip.open(path, 'r')
	for l in g:
		yield eval(l)

print sys.argv[1]

n=0
debug=1
client = MongoClient("localhost:27017")
db = client.amazon1

# student_record = {'name':'song','grade':98}
# db.students.insert(student_record)
# student_record = {'name':'song','grade':97}
# db.students.insert(student_record)
# student_record = {'name':'song','grade':96}
# db.students.insert(student_record)

# student_record = {'name':'qin','grade':99.6}
# db.students.insert(student_record)
# student_record = {'name':'qin','grade':99.5}
# db.students.insert(student_record)
# student_record = {'name':'qin','grade':99.4}
# db.students.insert(student_record)

# results = db.students.find()
# for record in results:
# 	print record
# 	print(record['name'] + ',',record['grade'])
	# print type(record['name'])
	# print type(record['grade'])
	# print record['grade']
	# print type(float(record['grade']))
	# print float(record['grade'])
# to use aggregate, you need a newer version of mongodb. I'm using 3.0.12
# results = db.students.aggregate([{
# 	"$group":{
# 	"_id": "$name",
# 	"avg": {"$avg":"$grade"}
# 	}}])
# for record in results:
# 	print record

# get top10000 uid
with open('top10000.txt', 'r') as f:
	content = f.readlines()
content = [x.strip('\n') for x in content]
content = [x.split(' ')[1] for x in content] #http://www.amazon.com/gp/pdp/profile/A1TWM78I835NGZ
top10000 = [x.split('profile/')[1] for x in content] #A1TWM78I835NGZ
# print top10000

r=0
# a file with the product id ( with duplicates) of the products reviewed by top 10000 reviewers
f1=open('pidTop10000.txt', 'w')

# create table and a file of products
for review in parse(sys.argv[1]):
	n+=1
	uid = review["reviewerID"]
	pid = review["asin"]
	s = review["overall"]
	t = review["reviewText"]
	# uid_pid_score_text

	# print uid, pid, s
	if(uid in top10000):
		r+=1
		record = {
		'uid': uid,
		'pid': pid,
		'score': s
		# ,
		# 'text': t
		}
		# print record
		# db.uid_pid_score_text.insert(record)
		# f.write(pid+'\n')
	if(debug):
		if(n==1000):
			break

# end 

results = db.uid_pid_score_text.find()
for record in results:
	print record
results = db.uid_pid_score_text.aggregate([{
	"$group":{
	"_id": "$pid",
	"avg": {"$avg":"$score"}
	}}])
print results
dict={}
for record in results:
	pid =  record['_id']
	ave = record['avg']
	dict[pid] = ave
print dict
# add average score field to table
for k in dict:
	# result = db.uid_pid_score_text.find({pid:key})
	# print result
	v=dict[k]
	db.uid_pid_score_text.update(
		{'pid':k},
		{
			'$set':{
				'ave': v
			}
		},
			upsert = False,		
			multi=  True
	)
print ''
print ''
print ''
print ''
print ''
results = db.uid_pid_score_text.find()
for record in results:
	print record
# print dict['3998899561']
# results = db.uid_pid_score_text.find()
# for record in results:
# 	print record
# print ''
# print ''
# print ''
# result = db.uid_pid_score_text.find({"pid":u"3998899561"})
# print result
# for record in result:
# 	print record


# r= db.uid_pid_score_text.update(
# 	{"pid":"3998899561"},
# 	{
# 		'$set':{
# 			'ave': dict['3998899561']#bug: ave should be 'ave'
# 		}
# 	},
# 		upsert = False,		
# 		multi=  True
# )
# print r

# result = db.uid_pid_score_text.find({"pid":u"3998899561"})
# print result
# for record in result:
# 	print record
# results = db.uid_pid_score_text.find()
# for record in results:
# 	print record

client.close()
# f.close()
