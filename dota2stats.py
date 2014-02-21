import api

account_id = int(api.get_steam_id("frankxu2004")["response"]["steamid"])
matches = api.get_match_history(account_id=account_id)["result"]["matches"]
account_id = account_id%(2**32)

for match in matches:
    if match["lobby_type"] == 0:
        match_detail = api.get_match_details(match["match_id"])
        for player in match["players"]:
            if player["account_id"] == account_id:
                if (player["player_slot"]<50 and match_detail["result"]["radiant_win"]) or (player["player_slot"]>50 and (not match_detail["result"]["radiant_win"])):
                    print "Win"
                else:
                    print "Loss"
