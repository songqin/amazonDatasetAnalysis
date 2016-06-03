# amazonDatasetAnalysis
Analyze an Amazon.com dataset of product reviews in a machine learning approach. 

Dataset: meta_Cell_Phones_and_Accessories.json.gz
To run :
./readDataset.py  ./dataset/reviews_Cell_Phones_and_Accessories.json.gz

asin: product id
reviewerID: reviewer id
overall: score of review

Goal: 
Procedures:
1. get the product IDs in the reviewes that were reviewed by the top10000 reviewers, put it in a list/map pidMap
1.1. get the stats:distribution of the scores of the product reviewed by the top10000
2. create a table:t1 and populate it with the reviews that uid is in the top10000 reviewers list. 
3. compute the ave_score for each productID (aggregation) in table:t1, and create a table t2 (productID, ave_score)
4. create a table t3 (uid, pid, score, ave_score, ) where pid is in the pidMap. 
5. count the CPT based on the rules.

rules (Assumption)
1. RW=T, if: uid in top10000 || score ave_score (in)
2. CS=T, if ave_score>3 (Why 3? because if it's lower than 3, people probably think it's not good product. )
3. CS=F, if ave_score<=3


database table:
name:reviewstop10000 (reviewers from top 10000 reviewers)
uid pid score ave_score (user id, product id, review score, average review score of the users from top 10000 reviewers)

From table: reviewstop10000, we can train:
RW CS P(W)
T  T
T  F

Assumption: RW=T, if: uid in top10000 || score ave_score (in)
intiuition: 
	1.top10000 is reliable. 
	2. 

Possible experimental errors:
some products have low review score, because of the delivery lateness, damage of the product.

