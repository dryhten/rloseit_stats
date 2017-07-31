"""
Script to pull the data from Super Hero Summer Challenge google spreadsheet
into a local json file.

To get this to work you first have to copy the spreadsheet into a private one
(google spreasheets with "anyone with link can view" access don't work
apparently), then give access to your service account and put the credentials
in gcred.py (same directory as this file).

This was made for Super Hero Summer Challenge 2017 and it's not exactly
a release. There are a lot of hardcoded variables in here that need
to be modified (e.g. COPIED_SPREADSHEET_NAME, relevant_area, WEEK_ROWS etc).
Feel free to change these and make it more generic if you like.

This uses gspread: https://github.com/burnash/gspread
(you need to have this installed as well).
"""
import json
import gspread
import numpy as np

from gcred import credentials

# open spreadsheet
COPIED_SPREADSHEET_NAME = "Copy of rloseit"
gc = gspread.authorize(credentials)
gs = gc.open(COPIED_SPREADSHEET_NAME)

"""
Worksheets in this doc (in this order):
  Tracker (0),
  Stats (1)
  Week 0 (2),
  Week 1 (3),
  Week 2 (4),
  Week 3 (5),
  Week 4 (6),
  Week 5 (7),
  Week 6 (8),
  Extra Stats (9)
"""

# build users dict from Tracker
tracker_ws = gs.get_worksheet(0)
relevant_area = "B2:H1327"
num_rows = 1326
num_cols = 7

# much faster to pull entire relevant data at once and not for every cell
data = np.array(tracker_ws.range(relevant_area)).reshape(num_rows, num_cols)

users = {}
for i in xrange(0, num_rows):
    username = data[i][0].value
    team = data[i][1].value
    age = data[i][2].value
    height = data[i][6].value
    users[username] = {}
    users[username]["team"] = team
    users[username]["age"] = age
    users[username]["height"] = height
    users[username]["weeks"] = []

# get each week weight-in + timestamp
# TODO smth better than this
WEEK_ROWS = [2027, 1677, 1373, 1380, 1003, 909, 221]
first_week = 0
last_week = 6

for i in xrange(first_week + 2, last_week + 3):
    week_ws = gs.get_worksheet(i)
    week_name = "Week " + str(i - 2);
    data = week_ws.range("A2:C" + str(WEEK_ROWS[i-2] + 1))
    data = np.array(data).reshape(WEEK_ROWS[i-2], 3)
    for j in xrange(0, WEEK_ROWS[i-2]):
        username = data[j][1].value
        user = users.get(username, None)
        if not user:
            users[username] = {}
            users[username]["weeks"] = []

        week = {}
        week["name"] = week_name
        week["weight"] = data[j][2].value
        week["timestamp"] = data[j][0].value
        # this might append same week couple of
        # times for dubplicated submissions
        # an alternative would be to use a dict for weeks e.g. ["week 0"]
        users[username]["weeks"].append(week)

# save users in a json for future use
with open("data.json", "w") as f:
    json.dump(users, f)
