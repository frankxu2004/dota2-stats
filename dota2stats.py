import api

def get_hero_name(hero_id, heroes_list):
    for hero in heroes_list:
        if hero_id == hero["id"]:
            return hero["localized_name"]

def get_account_id():
    while True:
        steam_user = raw_input("Enter Steam Name/Vanity URL:")
        steam_id = api.get_steam_id(steam_user)
        if steam_id["response"]["success"] == 1:
            return int(steam_id["response"]["steamid"])
        print "User not found! Try again!"

account_id64 = get_account_id()
account_id32 = account_id64%(2**32)
matches = api.get_match_history(account_id=account_id64)["result"]["matches"]
heroes_list = api.get_heroes()["result"]["heroes"]

for match in matches:
    if match["lobby_type"] == 0 or match["lobby_type"] == 7:
        match_id = match["match_id"]
        match_detail = api.get_match_details(match_id)
        for player in match["players"]:
            if player["account_id"] == account_id32:
                player_hero = get_hero_name(player["hero_id"], heroes_list)
                if (player["player_slot"]<50 and match_detail["result"]["radiant_win"])\
                   or (player["player_slot"]>50 and (not match_detail["result"]["radiant_win"])):
                    print str(match_id) + " " + player_hero + " Win"
                else:
                    print str(match_id) + " " + player_hero + " Loss"
