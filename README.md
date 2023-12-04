# YahooFantasyBasketball-project0
When playing yahoo's fantasy basketball's 9-cat game, looking at players stats everyday costs me too much time. I want to design a project that can assist with my decision making in drafting players. 

In the 9-cat game, I'm a "drafter" drafting basketball "players".  
As a drafter, we draft 13 players in total in a snake-draft with the other 11 drafters (12 drafters in total).  
We compete against other drafter's selected team.  
The 9 categories to compete against an opponent drafter in a 9-cat game are:  
  
FG%  
FT%  
3PTM  
Points  
Assists  
Rebounds  
Steals  
Blocks  
Turnovers  
Win at least 5 categories accumlated in a whole week against an opponent drafter.  

This Project aims at preprocessing raw data scraped from https://www.basketball-reference.com/  
Main steps in this project:  
  
1. Data Scraping and Preprocessing:  
- Includes EDA, filtering and joining tables using pandas.  
2. Create a Team Roster Auto-Builder, based on:  
- Weekly Player Performance Prediction.  
- Dynamic Programming for team roster selection.  

Notes: Fantasy basketball drafting is actually such a complex contrained optimization problem that I would like to dig deep in another project (Multiple Knapsack Assignment Problem).
Right now I just want to "assist" my decision making rather than creating a whole automated roster building algorithm.