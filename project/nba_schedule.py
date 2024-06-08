import pandas as pd
import requests
from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType
import os
import time
from project.utils import DATA_PATH, nba_start_end_date
from typing import Dict

class nba_schedule:
    def __init__(self):
        self.df_season_start_end_dates = nba_start_end_date(overwrite=True)

    def get_data(self) -> Dict[int, pd.DataFrame]:
        pass
