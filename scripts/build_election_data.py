import json
from pathlib import Path
from collections import defaultdict

SRC = Path("/tmp/cec/data/elections/2020-2024")
OUT = Path("data/2024_presidential_town.json")
OUT.parent.mkdir(parents=True, exist_ok=True)

towns = {}

for p in SRC.glob("*.json"):
    try:
        obj = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        continue
    result = obj.get("2024總統")
    if not isinstance(result, dict):
        continue

    code = p.stem
    bucket = towns.setdefault(code, {
        "county": obj.get("county", ""),
        "town": obj.get("town", ""),
        "votes": defaultdict(int)
    })

    for name, item in result.items():
        if not isinstance(item, dict):
            continue
        bucket["votes"][name] += int(item.get("votes", 0) or 0)

output = {}
national = defaultdict(int)

for code, item in towns.items():
    total = sum(item["votes"].values())
    candidates = []
    for name, votes in sorted(item["votes"].items(), key=lambda x: -x[1]):
        party = {
            "柯文哲": "台灣民眾黨",
            "賴清德": "民主進步黨",
            "侯友宜": "中國國民黨"
        }.get(name, "")
        national[name] += votes
        candidates.append({
            "name": name,
            "party": party,
            "votes": votes,
            "share": round(votes / total * 100, 2) if total else 0
        })

    output[code] = {
        "county": item["county"],
        "town": item["town"],
        "totalVotes": total,
        "candidates": candidates
    }

national_total = sum(national.values())
national_rows = []
for name, votes in sorted(national.items(), key=lambda x: -x[1]):
    party = {
        "柯文哲": "台灣民眾黨",
        "賴清德": "民主進步黨",
        "侯友宜": "中國國民黨"
    }.get(name, "")
    national_rows.append({
        "name": name,
        "party": party,
        "votes": votes,
        "share": round(votes / national_total * 100, 2) if national_total else 0
    })

payload = {
    "meta": {
        "election": "第16任總統副總統選舉",
        "year": 2024,
        "source": "中央選舉委員會公開選舉資料",
        "aggregation": "村里層級票數彙整至鄉鎮市區"
    },
    "national": {
        "totalVotes": national_total,
        "candidates": national_rows
    },
    "towns": output
}

OUT.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(f"Generated {OUT}: {len(output)} towns")
