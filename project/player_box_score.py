import pandas as pd
import requests
from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType
import os
import time
from project.utils import DATA_PATH, nba_start_end_date
from typing import Dict

class player_box_score:
    def __init__(self):
        self.df_season_start_end_dates = nba_start_end_date(overwrite=True)
        thisyear=self.df_season_start_end_dates['season'].tail(1).item() # thisyear represents the newest NBA season with games data. 2024 represents 2023-2024 season. 
        startyear=thisyear-3

    def get_data(self) -> Dict[int, pd.DataFrame]:
        # player box score game-by-game
        df_pbs = dict()

        crawl_date0 = pd.Timestamp(df_season_start_end_dates[df_season_start_end_dates['season']==thisyear]['start_date'].iloc[0])
        crawl_date1 = min(to_tz_aware(pd.Timestamp.today()), pd.Timestamp(df_season_start_end_dates[df_season_start_end_dates['season']==thisyear]['end_date'].iloc[0]))
        print(f'start date is {crawl_date0}')
        if os.path.exists(os.path.join(DATA_PATH, f'pbs{thisyear}-raw.csv')):
            df_pbs[thisyear] = pd.read_csv(os.path.join(DATA_PATH, f'pbs{thisyear}-raw.csv'), index_col=0)
            crawl_date0 = to_tz_aware(pd.Timestamp(df_pbs[thisyear]['date'].max())) + pd.Timedelta(days=1)
            print(f'next crawl date: {crawl_date0}')

        try:
            while crawl_date0 <= crawl_date1:  # only regular season.  
                i=0
                try: 
                    df_tmp = pd.DataFrame.from_dict(client.player_box_scores(day=crawl_date0.day, month=crawl_date0.month, year=crawl_date0.year))
                except requests.exceptions.HTTPError as err:
                    print(f'A HTTPError was thrown: {err}')
                    df_pbs[thisyear].to_csv(f'pbs{thisyear}-raw.csv')
                except Exception as e:
                    print(f"Exception while getting basketball ref data: {e}")
                    df_pbs[thisyear].to_csv(f'pbs{thisyear}-raw.csv')

                df_tmp['date'] = crawl_date0
                if thisyear not in df_pbs:
                    df_pbs[thisyear] = df_tmp
                else: 
                    df_pbs[thisyear] = pd.concat([df_pbs[thisyear], df_tmp])
                
                print(f'{crawl_date0} finished')
                print(df_pbs[thisyear].tail(1))
                crawl_date0 = crawl_date0 + pd.Timedelta(days=1)
                print(f'next crawl date: {crawl_date0}')
                time.sleep(10) # delay for 10 seconds (takes a total of 30min). sometimes you'll need longer. 
                i+=1
                if i%50==0: # backup every 50 iterations
                    df_pbs[thisyear].to_csv(f'pbs{thisyear}-raw.csv')
        except KeyboardInterrupt:
            print("Keyboard Interrupt..")
            df_pbs[thisyear].to_csv(f'pbs{thisyear}-raw.csv')

        df_pbs[thisyear].to_csv(os.path.join(DATA_PATH, f'pbs{thisyear}-raw.csv'))
