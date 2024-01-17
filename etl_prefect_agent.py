# Use Prefect to build our DAG workflow. 
# Prefect needs python >= 3.8, but basketball scraper environment is 3.7!!!!!!!!! 

# 2021~2023 pbs data doesn't need frequent update.  Crawl it beforehand and upload to S3 manually.  
# Only crawl new 2024 player box score(pbs) data (every game stats of all players)


# Transform to 9-cat friendly and ML training ready data.  

