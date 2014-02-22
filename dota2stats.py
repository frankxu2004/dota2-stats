import api

def get_hero_name(hero_id, heroes_list):
    for hero in heroes_list:
        if hero_id == hero["id"]:
            return hero["localized_name"]

def get_account_id():
    user_input = raw_input("Enter SteamID/VanityURL:")
    if user_input.isdigit() and len(user_input) == 17:
        return int(user_input), int(user_input)%(2**32)
    elif user_input.isdigit() and len(user_input) == 9:
        return int(user_input)+76561197960265728, int(user_input)
    else:
        response = api.get_steam_id(user_input)
        if response["response"]["success"] == 1:
            return int(response["response"]["steamid"]), int(response["response"]["steamid"])%(2**32)
        else:
            print "User not found"
def get_match_history(account_id64):
    response = api.get_match_history(account_id=account_id64)
    if response["result"]["status"] == 1:
        return response["result"]["matches"]
    else:
        print response["result"]["statusDetail"]

def match_stats(account_id64, account_id32):
    win, loss = 0, 0
    matches = get_match_history(account_id64)
    for match in matches:
        if match["lobby_type"] == 0 or match["lobby_type"] == 7:
            match_id = match["match_id"]
            match_detail = api.get_match_details(match_id)["result"]
            for player in match_detail["players"]:
                if player["account_id"]== account_id32 and get_hero_name(player["hero_id"],heroes_list)!=None:
                    player_hero = get_hero_name(player["hero_id"],heroes_list)
                    if ((player["player_slot"]<50 and match_detail["radiant_win"])\
                       or (player["player_slot"]>50 and (not match_detail["radiant_win"])))\
                       and (player["leaver_status"]!=2):
                        win=win+1
                        print str(match_id) + " " + player_hero + " Win"
                    else:
                        loss=loss+1
                        print str(match_id) + " " + player_hero + " Loss"
    return win, loss

if __name__ == '__main__':
    heroes_list = api.get_heroes()["result"]["heroes"]
    while True:
        #try:
            account_id64, account_id32 = get_account_id()
            win, loss = match_stats(account_id64, account_id32)
            winrate = float(win)/float(win+loss)
            print "Win: " + str(win) + " Loss: " + str(loss)
            print "Win Rate: " + str(winrate*100)+"%"
        #except:
            pass
