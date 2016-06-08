# amazonDatasetAnalysis
Analyze an Amazon.com dataset of product reviews in a machine learning approach. 

Dataset: meta_Cell_Phones_and_Accessories.json.gz
To run :
dataset1: Cell Phones and Accessories 
 	reviews (3,447,249 reviews) 	metadata (346,793 products)
./readDataset.py  ./dataset/reviews_Cell_Phones_and_Accessories.json.gz
dataset2: Home and Kitchen 
 	reviews (4,253,926 reviews) 	metadata (436,988 products)
./readDataset.py ./dataset/reviews_Home_and_Kitchen.json.gz
 	5-core (551,682 reviews) 	ratings only (4,253,926 ratings)
./readDataset.py ./dataset/reviews_Home_and_Kitchen_5.json.gz
dataset 3: Sports and Outdoors 
reviews (3,268,695 reviews) 	metadata (532,197 products)
./readDataset.py  ./dataset/reviews_Sports_and_Outdoors.json.gz
dataset 4: Electronics 
 	reviews (7,824,482 reviews) 	metadata (498,196 products)
./readDataset.py  ./dataset/reviews_Electronics.json.gz
dataset 5: Movies and TV 
 	reviews (4,607,047 reviews) 	metadata (208,321 products)
./readDataset.py  ./dataset/reviews_Movies_and_TV.json.gz
dataset 6: Clothing, Shoes and Jewelry 5,748,920 reviews
./readDataset.py  ./dataset/
dataset 7: Kindle Store 3,205,467 reviews
./readDataset.py  ./dataset/
dataset 8: Apps for Android 2,638,173 reviews
./readDataset.py  ./dataset/ 
dataset 9: Grocery and Gourmet Food  1,297,156 reviews
./readDataset.py  ./dataset/ 500,176 reviews
dataset 10:  Digital Music  	reviews (500,176 reviews) 	metadata (84,901 products)
./readDataset.py  ./dataset/

sorted order: 

asin: product id
reviewerID: reviewer id
overall: score of review

Goal: 
Procedures:
1. get the product IDs in the reviewes that were reviewed by the top10000 reviewers, put it in a list/map pidMap
1.1. get the stats:distribution of the scores of the product reviewed by the top10000
2. create a table: uid_pid_score_text (uid, pid, score, text) and populate it with the reviews that uid is in the top10000 reviewers list. 
3. compute the ave_score for each productID (aggregation) in table:t1, and create a table t2 (productID, ave_score)
4. create a table t3 (uid, pid, score, ave_score, ) where pid is in the pidMap. 
5. count the CPT based on the rules.

rules (Assumption)
1. RW=T, if: uid in top10000 || score ave_score (in)
RW=F, if: 
2. CS=T, if ave_score>3 (Why 3? because if it's lower than 3, people probably think it's not good product. )
CS=F, if ave_score<=3


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

Output:
# of reviews reviewed by top10000 = 34705
# of all reviews  = 3447249
