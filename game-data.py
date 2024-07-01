import json
import gzip
import sys
import os

result = {}
date = sys.argv[1]

with gzip.open(f"data/cia/{date}.jsonlines.gz") as f:
    for line in f:
        record = json.loads(line)

        if "ART" != record["itemKey"]["itemType"]:
            continue

        if "STO" != record["classUnitKey"]["classUnitType"]:
            continue

        article_id = int(record["itemKey"]["itemNo"])

        if article_id not in result:
            result[article_id] = {}

        store_id = str(record["classUnitKey"]["classUnitCode"])
        available_stock = int(record["buyingOption"].get("cashCarry", {}).get("availability", {}).get("quantity", 0))

        result[article_id][store_id] = available_stock

for (article_id, data) in result.items():
    os.makedirs(f"public/data/{article_id}", exist_ok=True)
    with open(f"public/data/{article_id}/{date}.json", "w") as file:
        file.write(json.dumps(data))

with open(f"public/index.json", "w") as file:
    file.write(
        json.dumps(
            [
                os.path.splitext(filename)[0]
                for filename in sorted(os.listdir("public/data/70277957"))
            ],
            indent=2,
        )
    )
