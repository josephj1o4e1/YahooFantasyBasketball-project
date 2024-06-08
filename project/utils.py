import pandas as pd
import os

DATA_PATH = '../data'

def nba_start_end_date(overwrite=False) -> pd.DataFrame: 
    if overwrite: 
        df_season_start_end_dates = pd.DataFrame({
            'season': range(2021, 2024+1),
            'start_date': [pd.Timestamp('2020-12-22', tz='America/Indiana/Indianapolis'), 
                        pd.Timestamp('2021-10-19', tz='America/Indiana/Indianapolis'), 
                        pd.Timestamp('2022-10-18', tz='America/Indiana/Indianapolis'), 
                        pd.Timestamp('2023-10-24', tz='America/Indiana/Indianapolis')],
            'end_date': [pd.Timestamp('2021-5-16', tz='America/Indiana/Indianapolis'), 
                        pd.Timestamp('2022-4-10', tz='America/Indiana/Indianapolis'), 
                        pd.Timestamp('2023-4-9', tz='America/Indiana/Indianapolis'), 
                        pd.Timestamp('2024-4-14', tz='America/Indiana/Indianapolis')],
        })
        df_season_start_end_dates.to_csv(os.path.join(DATA_PATH, f'season_start_end_dates.csv'))
        return df_season_start_end_dates
    
    if os.path.exists(os.path.join(DATA_PATH, f'season_start_end_dates.csv')):
        return pd.read_csv(os.path.join(DATA_PATH, f'season_start_end_dates.csv'), index_col=0, parse_dates=['start_date', 'end_date'])
    else:
        df_season_start_end_dates = pd.DataFrame({
            'season': range(2021, 2024+1),
            'start_date': [pd.Timestamp('2020-12-22', tz='America/Indiana/Indianapolis'), 
                        pd.Timestamp('2021-10-19', tz='America/Indiana/Indianapolis'), 
                        pd.Timestamp('2022-10-18', tz='America/Indiana/Indianapolis'), 
                        pd.Timestamp('2023-10-24', tz='America/Indiana/Indianapolis')],
            'end_date': [pd.Timestamp('2021-5-16', tz='America/Indiana/Indianapolis'), 
                        pd.Timestamp('2022-4-10', tz='America/Indiana/Indianapolis'), 
                        pd.Timestamp('2023-4-9', tz='America/Indiana/Indianapolis'), 
                        pd.Timestamp('2024-4-14', tz='America/Indiana/Indianapolis')],
        })
        df_season_start_end_dates.to_csv(os.path.join(DATA_PATH, f'season_start_end_dates.csv'))
        return df_season_start_end_dates


def to_tz_aware(date_in: pd.Timestamp=pd.Timestamp.today(), timezone: str='America/Indiana/Indianapolis'):  
    if date_in.tz != None:
        date_in = date_in.tz_convert(timezone)
    else:
        date_in = date_in.tz_localize(timezone)
    return date_in

def isin_season_start_end_dates(date_in: pd.Timestamp):
    df_season_start_end_dates = nba_start_end_date(overwrite=True)
    if (df_season_start_end_dates.start_date.head(1).item() <= date_in) and (date_in <= df_season_start_end_dates.end_date.tail(1).item()):
        return True
    else:
        return False


def transform_to_nba_regular_week(date_in: pd.Timestamp=pd.Timestamp.today()):
    df_season_start_end_dates = nba_start_end_date(overwrite=True)
    date_in = to_tz_aware(date_in) 
    yr = transform_to_nba_regular_season(date_in)
    if yr!=None:
        nba_firstweek = df_season_start_end_dates[df_season_start_end_dates['season']==yr]['start_date'].iloc[0].week
        if date_in < to_tz_aware(pd.Timestamp(f'{yr}-1-1')): # Consider timezone problems later
            return date_in.week - nba_firstweek + 1
        else: 
            return int((date_in.week + to_tz_aware(pd.Timestamp(f'{yr-1}-12-31')).week) - nba_firstweek + 1)
    else: 
        # earliest_season_in_record = f'{df_season_start_end_dates.start_date.head(1).item().year}-{df_season_start_end_dates.start_date.head(1).item().year+1}'
        # latest_season_in_record = f'{df_season_start_end_dates.end_date.tail(1).item().year-1}-{df_season_start_end_dates.end_date.tail(1).item().year}'
        # print(f'Only have season-start date records from the {earliest_season_in_record} season to {latest_season_in_record} season. Please check. ')
        print(f'{date_in} is not during the regular season. ')
        return None    
    

def transform_to_nba_regular_season(date_in: pd.Timestamp=pd.Timestamp.today()):  
    df_season_start_end_dates = nba_start_end_date(overwrite=True)
    date_in = to_tz_aware(date_in)    
    if isin_season_start_end_dates(date_in):  
        for yr in range((max(date_in.year-1, df_season_start_end_dates.end_date.head(1).item().year)), min(date_in.year+2, df_season_start_end_dates.end_date.tail(1).item().year + 1)):  # should be (?) a slightly faster query to directly hop to the possible 3 seasons instead of iterating through all the seasons.  
            s_date = df_season_start_end_dates[df_season_start_end_dates.season==yr].start_date.item()
            if yr==df_season_start_end_dates.end_date.tail(1).item().year: 
                s_date_nextyear = None
            else: 
                s_date_nextyear = df_season_start_end_dates[df_season_start_end_dates.season==yr+1].start_date.item()
            e_date = df_season_start_end_dates[df_season_start_end_dates.season==yr].end_date.item()
            
            if (s_date <= date_in) and (date_in <= e_date):  
                nba_season = yr
                # print(f'{date_in} is during season {nba_season-1}-{nba_season}.  ')
                return nba_season
            elif s_date_nextyear!=None and (date_in < s_date_nextyear):  # find closest previous season
                nba_season = yr + 1
                # print(f'{date_in} is not in season, closest previous season is {nba_season}.  ')
                return nba_season
    else:     
        # earliest_season_in_record = f'{df_season_start_end_dates.start_date.head(1).item().year}-{df_season_start_end_dates.start_date.head(1).item().year+1}'
        # latest_season_in_record = f'{df_season_start_end_dates.end_date.tail(1).item().year-1}-{df_season_start_end_dates.end_date.tail(1).item().year}'
        # print(f'Only have season-start date records from the {earliest_season_in_record} season to {latest_season_in_record} season. Please check. ')
        print(f'{date_in} is not during the regular season. ')
        return None

