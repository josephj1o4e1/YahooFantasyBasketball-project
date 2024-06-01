# Use Prefect to build our DAG workflow. 

# 2021~2023 pbs data doesn't need frequent update.  Crawl it beforehand and upload to S3 manually.  
# Only crawl new 2024 player box score(pbs) data (every game stats of all players)

# Transform to 9-cat analysis friendly and ML training ready data.  

# 1. season_start_end_date =>
# 2. pbs-raw -> (transf(cleaning)) -> pbs -> (transf(agg/create view)) -> view_pbs(yr, N, method)...save
# 2-1. sched -> (transf(create week)) -> weekly_games_count(yr)...save
# 3. view_pbs(yr, N, method) + weekly_games_count(yr) ==> weekly_projection using "method"=('avg' or 'total')

import pandas as pd
from prefect import task, flow, get_run_logger
# import boto3
# from boto3.s3.key import key

# Extract pbs
@task
def extract_pbs_raw() -> dict:
    pass


# Trans pbs
@task
def transform_pbs_raw() -> dict:
    pass


# Extract weekly_gc
@task
def extract_weekly_gc_raw() -> dict:
    pass


# Trans weekly_gc
@task
def transform_weekly_gc_raw() -> dict:
    pass


# Load
@task
def dfdict_to_s3(dfdict):
    # for yr in dfdict.keys():
    #     dfdict[yr].to_csv(f'view_pbs{yr}.csv')
    #     # load to S3
    #     # USE CONCURRENCY (task.submit, task.result())
    pass


@flow
def subflow_view_pbs(): 
    dfdict_pbs_raw = extract_pbs_raw()
    dfdict_pbs = transform_pbs_raw(dfdict_pbs_raw)
    dfdict_to_s3(dfdict_pbs)
    return dfdict_pbs


@flow
def subflow_weekly_gamecount(): 
    dfdict_weekly_gc_raw = extract_weekly_gc_raw()
    dfdict_weekly_gc = transform_weekly_gc_raw(dfdict_weekly_gc_raw)
    dfdict_to_s3(dfdict_weekly_gc)
    return dfdict_weekly_gc

@task
def generate_weeklyproj(dfdict_pbs, dfdict_weekly_gc):
    pass


# I want to let subflow_view_pbs and subflow_weekly_gamecount run concurrently. 
# But subflow concurrency seems to have issues even using asyncio.gather  (https://discourse.prefect.io/t/how-can-i-run-multiple-subflows-or-child-flows-in-parallel/96/24)
# "Only the first task is concurrent, but the rest are sequential. "
@flow
def mainflow_weeklyproj(): 
    dfdict_pbs = subflow_view_pbs()
    dfdict_weekly_gc = subflow_weekly_gamecount()
    dfdict_weeklyproj = generate_weeklyproj(dfdict_pbs, dfdict_weekly_gc)
    dfdict_to_s3(dfdict_weeklyproj)
    pass



