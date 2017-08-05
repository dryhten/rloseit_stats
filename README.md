# rloseit_stats
Python scripts for the Super Hero Summer Challenge 2017 from /r/loseit.

https://www.reddit.com/r/loseit/comments/6rkr7b/challenge_super_hero_summer_challenge_results
https://docs.google.com/spreadsheets/d/1VMfjVfSFs2wFLf3j_zUwABJJIZTyIdfDFraECHZnYyA/edit#gid=1317843042

These basically pull the data from the google spreadsheet and store it as a json file (data.json). In stats.py you have examples on how to use the file to play around with stats (if you're into that kind of things). I also made tops which I saved as xlsx files in tops/. Also, you have an example of how the json data is stored in json_example (e.g. users["ddryhten"]).

How to use the scripts (also for future versions of the challenge)
1. get gspread
https://github.com/burnash/gspread
2. create a gcred.py file and store the credentials (variable) there
3. copy the /r/loseit google spreadsheet to a private one and give access to your service account (similar to the gspread tutorial; apparently there's a problem with documents that have "anyone with link can view" access)
4. fix the hardcoded stuff from get_data.py (e.g. relevant cells, number of rows, google spreadsheet name etc)
5. run get_data.py to get the json file (data.json)
6. optional: play around with stats.py and check ranks and stuff
