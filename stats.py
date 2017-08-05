"""
Stats for /r/loseit Super Hero Summer Challenge.

This needs "data.json" in the same directory.
"data.json" is the data from the google spreadsheet in json format.
To get it use get_data.py.

You can find examples on how to use different functions in examples()
down below (just uncomment it in main() and run this file to see output).
"""
import json

# this string is used to represent all teams
ALL_TEAMS = "all"

# users as a global var
with open("data.json", "r") as f:
    users = json.load(f)

# some users had typos when entering weights
# TODO add reasons as well
ignored_users = ["Ott3r", "Rvaughangeib", "bassi123"]

def main():
    #examples()
    pass

def examples():
    """ this has examples on how to use other functions in this file """
    # print top 10 users after weight loss (global)
    print_top_weight_loss(10)

    # print top 10 users after weight loss from team Wonder Woman
    print_top_weight_loss(10, team="Wonder Woman")

    # print top 10 users after % of weight loss (global)
    print_top_weight_percentage_loss(10, team=ALL_TEAMS)

    # print top 10 users after BMI change from team Hulk
    print_top_bmi_loss(10, team="Hulk")

    # print top 20 users after BMI % change from team IronMan
    print_top_bmi_percentage_loss(20, team="IronMan")

    # get the rank for some user after different criteria
    print get_rank_bmi_percentage_loss("ddryhten")
    print get_rank_weight_loss("ddryhten", team="Wonder Woman")

    # to get more info on a specific user just use the global var users
    global users
    print(users["ddryhten"])

    # to view the info in a nice format use print_info_user
    print_info_user("ddryhten")

def print_top_bmi_percentage_loss(n, team=ALL_TEAMS):
    """ just a wrapper for print_top_weight_loss_generic """
    return print_top_generic(n, "bmi_percentage_loss", team=team)

def print_top_bmi_loss(n, team=ALL_TEAMS):
    """ just a wrapper for print_top_weight_loss_generic """
    return print_top_generic(n, "bmi_loss", team=team)

def print_top_weight_percentage_loss(n, team=ALL_TEAMS):
    """ just a wrapper for print_top_weight_loss_generic """
    return print_top_generic(n, "weight_percentage_loss", team=team)

def print_top_weight_loss(n, team=ALL_TEAMS):
    """ just a wrapper for print_top_weight_loss_generic """
    return print_top_generic(n, "weight_loss", team=team)

def print_top_generic(n, top, team=ALL_TEAMS):
    """
    prints results from top_(n) functions
    some flags can be added to this function with what to print
    """
    print("Top " + str(n) + " participants after " + top + ":")
    if top == "weight_loss":
        top_users = top_weight_loss(n, team=team)
    elif top == "weight_percentage_loss":
        top_users = top_weight_percentage_loss(n, team=team)
    elif top == "bmi_loss":
        top_users = top_bmi_loss(n, team=team)
    elif top == "bmi_percentage_loss":
        top_users = top_bmi_percentage_loss(n, team=team)
    else:
        print("Invalid top")
        return

    for user in top_users:
        username = user[0].encode("utf-8")
        if top == "weight_loss":
            weight_lost = user[1]["weight_lost"]
            print(username + " " + str(weight_lost) + "lbs"),
        elif top == "weight_percentage_loss":
            wpl = user[1]["weight_percentage_lost"]
            print(username + " "),
            print("%.2f%%" % wpl),
        elif top == "bmi_loss":
            bmi_change = user[1]["bmi_change"]
            print(username + " "),
            print("%.2f" % bmi_change),
        elif top == "bmi_percentage_loss":
            bmi_pc = user[1]["bmi_pc"]
            print(username + " "),
            print("%.2f%%" % bmi_pc),
        else:
            print("Invalid method")
            return

        team = user[1].get("team", None)
        if team:
            print(" " + team.encode("utf-8")),
        age = user[1].get("age", None)
        if age:
            print("age: " + age.encode("utf-8")),
        height = user[1].get("height", None)
        if height:
            print("height: " + height.encode("utf-8")),
        weeks = user[1].get("weeks")
        if weeks:
            starting_weight = weeks[0].get("weight")
            print("sw: " + starting_weight + "lbs"),
        print("")

def print_less_active():
    """ just a wrapper for min_weeks """
    print("The participant who logged his/her weight for the lowest "
          "number of weeks: " + str(min_weeks()))

def print_oldest():
    """ just a wrapper for max_age """
    print("Oldest participant: " + str(max_age()))

def print_youngest():
    """ just a wrapper for min_age """
    print("Youngest participant: " + str(min_age()))


def get_rank_bmi_percentage_loss(user, team=ALL_TEAMS):
    """ returns the rank of a user in the weight loss top """
    return get_rank(user, "bmi_percentage_loss", team=team)

def get_rank_bmi_loss(user, team=ALL_TEAMS):
    """ returns the rank of a user in the weight loss top """
    return get_rank(user, "bmi_loss", team=team)

def get_rank_weight_percentage_loss(user, team=ALL_TEAMS):
    """ returns the rank of a user in the weight percentage loss top """
    return get_rank(user, "weight_percentage_loss", team=team)

def get_rank_weight_loss(user, team=ALL_TEAMS):
    """ returns the rank of a user in the weight loss top """
    return get_rank(user, "weight_loss", team=team)

def get_rank(user, top, team=ALL_TEAMS):
    """ returns the rank of a user in the specified top """
    global users
    user_team = users[user].get("team", None)
    if not user_team and team != ALL_TEAMS:
        print("User not in the specified team")
        return None
    if team != ALL_TEAMS and user_team.encode("utf-8") != team:
        print("User not in the specified team")
        return None

    if top == "weight_loss":
        sorted_users = top_weight_loss(len(users), team=team)
    elif top == "weight_percentage_loss":
        sorted_users = top_weight_percentage_loss(len(users), team=team)
    elif top == "bmi_loss":
        sorted_users = top_bmi_loss(len(users), team=team)
    elif top == "bmi_percentage_loss":
        sorted_users = top_bmi_percentage_loss(len(users), team=team)
    else:
        return None

    rank = 1
    for usr in sorted_users:
        if user == usr[0].encode("utf-8"):
            return rank
        rank = rank + 1
    return rank

def top_bmi_percentage_loss(n, team=ALL_TEAMS):
    """
    returns top n users sorted after change in BMI percentage
    this will modify users variable

    percentage of BMI lost is the same as percentage of weight lost
    so I used (% weight) / height^2 to account for both % weight and
    height
    """
    global users
    for user, values in users.iteritems():
        bmi_pc = 0
        height_str = values.get("height", None)
        if (values["weeks"] and height_str):
            weight_start = float(values["weeks"][0]["weight"])
            weight_end = float(values["weeks"][-1]["weight"])
            height = float(height_str)
            bmi_pc = 70300 * (weight_start - weight_end) / \
                     (height ** 2 * weight_start)

        values["bmi_pc"] = bmi_pc

    # sort after bmi_pc lost
    top_users = sorted(users.items(),
                       key=lambda x:(x[1]["bmi_pc"]),
                       reverse=True)

    # remove ignored users & filter after team
    top_users = filter(filter_ignored_users, top_users)
    if team != ALL_TEAMS:
        top_users = filter(lambda x: filter_team(x, team), top_users)

    n = min(len(top_users), n)
    return top_users[:n]

def top_bmi_loss(n, team=ALL_TEAMS):
    """
    returns top n users sorted after lost BMI value
    this will modify users variable
    BMI formula: 703 * weight (lbs) / height^2 (in)
    """
    global users
    for user, values in users.iteritems():
        bmi_change = 0
        height_str = values.get("height", None)
        if values["weeks"] and height_str:
            weight_start = float(values["weeks"][0]["weight"])
            weight_end = float(values["weeks"][-1]["weight"])
            height = float(height_str)
            bmi_change = (703 * weight_start / (height * height)) - \
                         (703 * weight_end / (height * height))

        values["bmi_change"] = bmi_change

    # sort after bmi_change_lost
    top_users = sorted(users.items(),
                       key=lambda x:(x[1]["bmi_change"]),
                       reverse=True)

    # remove ignored users & filter after team
    top_users = filter(filter_ignored_users, top_users)
    if team != ALL_TEAMS:
        top_users = filter(lambda x: filter_team(x, team), top_users)

    n = min(len(top_users), n)
    return top_users[:n]

def top_weight_percentage_loss(n, team=ALL_TEAMS):
    """
    returns top n users sorted after lost percentage of weight
    this will modify users variable
    """
    global users
    for user, values in users.iteritems():
        weight_percentage_lost = 0
        if values["weeks"]:
            weight_lost = float(values["weeks"][0]["weight"]) - \
                          float(values["weeks"][-1]["weight"])
            weight_percentage_lost = (weight_lost * 100) / \
                                     float(values["weeks"][0]["weight"])
        values["weight_percentage_lost"] = weight_percentage_lost

    # sort after weight_percentage_lost
    top_users = sorted(users.items(),
                       key=lambda x:(x[1]["weight_percentage_lost"]),
                       reverse=True)

    # remove ignored users & filter after team
    top_users = filter(filter_ignored_users, top_users)
    if team != ALL_TEAMS:
        top_users = filter(lambda x: filter_team(x, team), top_users)

    n = min(len(top_users), n)
    return top_users[:n]

def top_weight_loss(n, team=ALL_TEAMS):
    """
    returns top n users sorted after lost weight
    this will modify users variable
    """
    global users
    for user, values in users.iteritems():
        weight_lost = 0
        if values["weeks"]:
            weight_lost = float(values["weeks"][0]["weight"]) -\
                          float(values["weeks"][-1]["weight"])
        values["weight_lost"] = weight_lost

    # sort after weight_lost
    top_users = sorted(users.items(),
                       key=lambda x:(x[1]["weight_lost"]), reverse=True)

    # remove ignored users & filter after team
    top_users = filter(filter_ignored_users, top_users)
    if team != ALL_TEAMS:
        top_users = filter(lambda x: filter_team(x, team), top_users)

    n = min(len(top_users), n)
    return top_users[:n]

def filter_ignored_users(user):
    """ returns True if user is not ignored """
    global ignored_users
    if user[0].encode("utf-8") in ignored_users:
        return False
    return True

def filter_team(user, team):
    """ returns True if user belongs to team """
    user_team = user[1].get("team", None)
    if not user_team:
        return False
    if user_team.encode("utf-8") != team:
        return False
    return True

def count_team(team_name):
    """ use ALL_TEAMS for all the teams and 'noteam' for none """
    cnt = 0
    global users
    for user, values in users.iteritems():
        user_team = values.get("team", None)
        if user_team:
            if team_name == ALL_TEAMS:
                cnt = cnt + 1
            elif user_team.encode("utf-8") == team_name:
                cnt = cnt + 1
        elif team_name == "noteam":
            cnt = cnt + 1
    return cnt

def min_weeks():
    """
    returns the participant who logged his/her weight for the lowest
    number of weeks; this could be turned into a histogram with number
    of weeks
    """
    global users
    min_weeks = 10
    min_user = ""
    for user, values in users.iteritems():
        weeks = values.get("weeks", None)
        if not weeks:
            continue
        num_weeks = len(weeks)
        if num_weeks < min_weeks:
            min_weeks = num_weeks
            min_user = user.encode("utf-8")
    return(min_user, min_weeks)

def max_age():
    """ returns the oldest participant """
    global users
    max_age = 0
    max_user = ""
    for user, values in users.iteritems():
        age_str = values.get("age", None)
        if not age_str:
            continue
        user_age = int(age_str)
        if user_age > max_age:
            max_age = user_age
            max_user = user.encode("utf-8")
    return(max_user, max_age)

def min_age():
    """ returns the youngest participant """
    global users
    min_age = 500
    min_user = ""
    for user, values in users.iteritems():
        age_str = values.get("age", None)
        if not age_str:
            continue
        user_age = int(age_str)
        if user_age < min_age:
            min_age = user_age
            min_user = user.encode("utf-8")
    return(min_user, min_age)

def print_info_user(user):
    """ prints info on user (json) in a readable format """
    global users
    user_data = users.get(user, None)
    if not user_data:
        print("Could not find user")
        return
    print json.dumps(user_data, indent=4, sort_keys=True)

main()
