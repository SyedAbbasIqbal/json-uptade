import json
from pathlib import Path

data_file = Path(__file__).with_name("eg5.json")

try:
    with open(data_file, "r", encoding="utf-8") as file:
        donut_data = json.load(file)

    for donut in donut_data:
        if donut.get("name") == "Old Fashioned":
            batters = donut["batters"]["batter"]
            if not any(b.get("type") == "Tea" for b in batters):
                batters.append({"id": "1009", "type": "Tea"})
            break

    with open(data_file, "w", encoding="utf-8") as file:
        json.dump(donut_data, file, indent=2, ensure_ascii=False)

    print('Tea batter added to "Old Fashioned" and file updated.')

except FileNotFoundError:
    print(f"Error: {data_file.name} not found.")
except json.JSONDecodeError:
    print("Error: Invalid JSON format.")
except Exception as e:
    print(f"Unexpected error: {e}")
