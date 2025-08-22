import json

with open("E:/Skill Rank/task/eg5.json", "r", encoding="utf-8") as f:
    eg5 = json.load(f)

for donut in eg5:
    if donut.get("name") == "Old Fashioned":
        batters_list = donut["batters"]["batter"]

        if not any(b["type"] == "Tea" for b in batters_list):
            batters_list.append({"id": "1003", "type": "Tea"})  
        break


with open("E:/Skill Rank/task/eg5.json", "w", encoding="utf-8") as f:
    json.dump(eg5, f, indent=2, ensure_ascii=False)

print('"Tea" batter added to Old Fashioned donut!')
