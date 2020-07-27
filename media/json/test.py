import json

jsonfile = "./qlash_brawlstars.json"
with open(jsonfile) as json_file:
    qlash_data = json.load(json_file)
    official_clubs = qlash_data["official_clubs"]
    print(official_clubs[1]["name"])
