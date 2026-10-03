import json
from pathlib import Path
from collections import defaultdict

SRC = Path("/tmp/cec/data/elections/2020-2024")
OUT = Path("data/elections.json")
OUT.parent.mkdir(parents=True, exist_ok=True)

CANDIDATE_PARTY = {
    "柯文哲": "台灣民眾黨",
    "賴清德": "民主進步黨",
    "侯友宜": "中國國民黨",
}

def aggregate_village_results(section_name):
    towns = {}
    national = defaultdict(lambda: {"party": "", "votes": 0})

    for p in SRC.glob("*.json"):
        try:
            obj = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue

        result = obj.get(section_name)
        if not isinstance(result, dict):
            continue

        code = p.stem
        bucket = towns.setdefault(code, {
            "county": obj.get("county", ""),
            "town": obj.get("town", ""),
            "candidates": defaultdict(lambda: {"party": "", "votes": 0})
        })

        for name, item in result.items():
            if not isinstance(item, dict):
                continue
            votes = int(item.get("votes", 0) or 0)
            party = item.get("party", "") or CANDIDATE_PARTY.get(name, "")
            bucket["candidates"][name]["party"] = party
            bucket["candidates"][name]["votes"] += votes
            national[name]["party"] = party
            national[name]["votes"] += votes

    output = {}
    for code, item in towns.items():
        rows = sorted(item["candidates"].items(), key=lambda x: -x[1]["votes"])
        total = sum(v["votes"] for _, v in rows)
        output[code] = {
            "county": item["county"],
            "town": item["town"],
            "totalVotes": total,
            "candidates": [
                {
                    "name": name,
                    "party": val["party"],
                    "votes": val["votes"],
                    "share": round(val["votes"] / total * 100, 2) if total else 0
                }
                for name, val in rows
            ]
        }

    national_total = sum(x["votes"] for x in national.values())
    national_rows = [
        {
            "name": name,
            "party": val["party"],
            "votes": val["votes"],
            "share": round(val["votes"] / national_total * 100, 2) if national_total else 0
        }
        for name, val in sorted(national.items(), key=lambda x: -x[1]["votes"])
    ]

    return {
        "national": {"totalVotes": national_total, "candidates": national_rows},
        "towns": output
    }

def aggregate_partylist():
    towns = {}
    national = defaultdict(lambda: {"party": "", "votes": 0})

    for p in SRC.glob("*.json"):
        try:
            obj = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue

        result = obj.get("2024不分區")
        if not isinstance(result, dict):
            continue

        code = p.stem
        bucket = towns.setdefault(code, {
            "county": obj.get("county", ""),
            "town": obj.get("town", ""),
            "parties": defaultdict(int)
        })

        for name, item in result.items():
            if not isinstance(item, dict):
                continue
            votes = int(item.get("votes", 0) or 0)
            party = item.get("party", "") or name
            bucket["parties"][party] += votes
            national[party]["party"] = party
            national[party]["votes"] += votes

    output = {}
    for code, item in towns.items():
        total = sum(item["parties"].values())
        rows = sorted(item["parties"].items(), key=lambda x: -x[1])
        output[code] = {
            "county": item["county"],
            "town": item["town"],
            "totalVotes": total,
            "parties": [
                {"name": name, "party": name, "votes": votes,
                 "share": round(votes / total * 100, 2) if total else 0}
                for name, votes in rows
            ]
        }

    national_total = sum(x["votes"] for x in national.values())
    national_rows = [
        {"name": name, "party": name, "votes": val["votes"],
         "share": round(val["votes"] / national_total * 100, 2) if national_total else 0}
        for name, val in sorted(national.items(), key=lambda x: -x[1]["votes"])
    ]
    return {"national": {"totalVotes": national_total, "parties": national_rows}, "towns": output}

payload = {
    "meta": {
        "source": "中央選舉委員會公開選舉資料",
        "aggregation": "村里層級票數彙整至鄉鎮市區"
    },
    "president": {
        "year": 2024,
        "election": "第16任總統副總統選舉",
        **aggregate_village_results("2024總統")
    },
    "partylist": {
        "year": 2024,
        "election": "第11屆立法委員全國不分區及僑居國外國民選舉",
        **aggregate_partylist()
    },
    "mayor": {
        "year": 2022,
        "election": "111年直轄市長、縣市長選舉",
        **aggregate_village_results("2022縣市長")
    }
}

OUT.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(f"Generated {OUT}: president={len(payload['president']['towns'])}, mayor={len(payload['mayor']['towns'])}, partylist={len(payload['partylist']['towns'])}")
