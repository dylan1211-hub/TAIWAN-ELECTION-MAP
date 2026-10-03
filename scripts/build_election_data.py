import csv
import json
from pathlib import Path
from collections import defaultdict

SRC = Path("/tmp/cec/data/elections/2020-2024")
SRC_2018 = Path("/tmp/cec/data/2018/縣市長.csv")
SRC_2018_CITY = Path("/tmp/cec/data/2018/直轄市長.csv")
SRC_2022 = Path("/tmp/cec/data/2022/縣市長.csv")
SRC_2022_CITY = Path("/tmp/cec/data/2022/直轄市長.csv")
LOCAL_MAYOR = Path("/tmp/local-election-dataset/data/candidate_vote")
OUT = Path("data/elections.json")
OUT.parent.mkdir(parents=True, exist_ok=True)

CANDIDATE_PARTY = {
    "柯文哲": "台灣民眾黨",
    "賴清德": "民主進步黨",
    "侯友宜": "中國國民黨",
}

def normalize_party(party):
    party = str(party or "").strip()
    return "無黨籍及未經政黨推薦" if party in ("", "無") else party

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
            party = normalize_party(item.get("party", "") or CANDIDATE_PARTY.get(name, ""))
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

OFFICIAL_PRESIDENT_HISTORY = {
    2012: {"year":2012,"election":"第13任總統副總統選舉","electors":18086455,"votes":13452016,"validVotes":13354305,"invalidVotes":97711,"turnout":74.38,"candidates":[{"name":"馬英九","party":"中國國民黨","votes":6891139,"share":51.60},{"name":"蔡英文","party":"民主進步黨","votes":6093578,"share":45.63},{"name":"宋楚瑜","party":"親民黨","votes":369588,"share":2.77}]},
    2016: {"year":2016,"election":"第14任總統副總統選舉","electors":18782991,"votes":12448302,"validVotes":12284970,"invalidVotes":163332,"turnout":66.27,"candidates":[{"name":"蔡英文","party":"民主進步黨","votes":6894744,"share":56.12},{"name":"朱立倫","party":"中國國民黨","votes":3813365,"share":31.04},{"name":"宋楚瑜","party":"親民黨","votes":1576861,"share":12.83}]},
    2020: {"year":2020,"election":"第15任總統副總統選舉","electors":19311105,"votes":14464571,"validVotes":14300940,"invalidVotes":163631,"turnout":74.90,"candidates":[{"name":"蔡英文","party":"民主進步黨","votes":8170231,"share":57.13},{"name":"韓國瑜","party":"中國國民黨","votes":5522119,"share":38.61},{"name":"宋楚瑜","party":"親民黨","votes":608590,"share":4.26}]},
    2024: {"year":2024,"election":"第16任總統副總統選舉","electors":19548531,"votes":14048310,"validVotes":13947506,"invalidVotes":100804,"turnout":71.86,"candidates":[{"name":"賴清德","party":"民主進步黨","votes":5586019,"share":40.05},{"name":"侯友宜","party":"中國國民黨","votes":4671021,"share":33.49},{"name":"柯文哲","party":"台灣民眾黨","votes":3690466,"share":26.46}]}
}

OFFICIAL_PARTYLIST_2024 = [
    {"name":"民主進步黨","party":"民主進步黨","votes":4981060,"share":36.16},
    {"name":"中國國民黨","party":"中國國民黨","votes":4764293,"share":34.58},
    {"name":"台灣民眾黨","party":"台灣民眾黨","votes":3040334,"share":22.07},
    {"name":"時代力量","party":"時代力量","votes":353670,"share":2.57},
    {"name":"小民參政歐巴桑聯盟","party":"小民參政歐巴桑聯盟","votes":128613,"share":0.93},
    {"name":"台灣綠黨","party":"台灣綠黨","votes":117298,"share":0.85},
    {"name":"台灣基進","party":"台灣基進","votes":95078,"share":0.69},
    {"name":"親民黨","party":"親民黨","votes":69818,"share":0.51}
]

def aggregate_mayor_towns():
    """Build complete 2022 county/city mayor results at township/district scale from CEC raw vote data."""
    root_base = Path("/tmp/cec/voteData/2022-111年地方公職人員選舉/C1")
    roots = [root_base / "city", root_base / "prv"]
    if not all((root / "elcand.csv").exists() and (root / "elbase.csv").exists() and (root / "elctks.csv").exists() for root in roots):
        return {}

    county_by_codes = {
        ("63", "000"): "臺北市",
        ("65", "000"): "新北市",
        ("68", "000"): "桃園市",
        ("66", "000"): "臺中市",
        ("67", "000"): "臺南市",
        ("64", "000"): "高雄市",
        ("10", "002"): "宜蘭縣",
        ("10", "004"): "新竹縣",
        ("10", "005"): "苗栗縣",
        ("10", "007"): "彰化縣",
        ("10", "008"): "南投縣",
        ("10", "009"): "雲林縣",
        ("10", "010"): "嘉義縣",
        ("10", "013"): "屏東縣",
        ("10", "014"): "臺東縣",
        ("10", "015"): "花蓮縣",
        ("10", "016"): "澎湖縣",
        ("10", "017"): "基隆市",
        ("10", "018"): "新竹市",
        ("10", "020"): "嘉義市",
        ("09", "007"): "連江縣",
        ("09", "020"): "金門縣",
    }

    party_by_candidate = {}
    for party_source in (SRC_2022, SRC_2022_CITY):
        if not party_source.exists():
            continue
        with party_source.open("r", encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                name = (row.get("cand_name") or "").strip()
                party = normalize_party(row.get("party", ""))
                if name:
                    party_by_candidate[name] = party

    towns = {}

    for root in roots:
        place_lookup = {}
        with (root / "elbase.csv").open("r", encoding="utf-8-sig", newline="") as f:
            for row in csv.reader(f):
                if len(row) < 6:
                    continue
                prv, city, level, area, li, name = [x.strip() for x in row[:6]]
                # li_code=0000 is the parent township/district row.
                if li == "0000" and area != "000":
                    place_lookup[(prv, city, level, area)] = name

        candidate_lookup = {}
        with (root / "elcand.csv").open("r", encoding="utf-8-sig", newline="") as f:
            for row in csv.reader(f):
                if len(row) < 7:
                    continue
                prv, city, level, area, li, cand_no, name = [x.strip() for x in row[:7]]
                if cand_no.isdigit():
                    candidate_lookup[(prv, city, cand_no)] = (
                        name,
                        party_by_candidate.get(name, normalize_party(""))
                    )

        with (root / "elctks.csv").open("r", encoding="utf-8-sig", newline="") as f:
            for row in csv.reader(f):
                if len(row) < 8:
                    continue
                prv, city, level, area, li, dept, cand_no = [x.strip() for x in row[:7]]
                if not cand_no.isdigit():
                    continue
                place = place_lookup.get((prv, city, level, area))
                candidate = candidate_lookup.get((prv, city, cand_no))
                if not place or not candidate:
                    continue
                try:
                    votes = int(str(row[7]).replace(",", "") or 0)
                except ValueError:
                    votes = 0
                if votes <= 0:
                    continue

                county = county_by_codes.get((prv, city))
                if not county:
                    continue

                code = f"mayor-{county}-{place}"
                bucket = towns.setdefault(
                    code,
                    {
                        "county": county,
                        "town": place,
                        "candidates": defaultdict(lambda: {"party": "", "votes": 0})
                    }
                )
                name, party = candidate
                bucket["candidates"][name]["party"] = party
                bucket["candidates"][name]["votes"] += votes

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

    return output

def aggregate_mayor_csv(source_paths):
    national = defaultdict(lambda: {"party": "", "votes": 0})
    counties = {}

    if isinstance(source_paths, (str, Path)):
        source_paths = [source_paths]

    for source_path in source_paths:
        if not source_path.exists():
            continue
        with source_path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                county = (row.get("area") or "").strip()
                name = (row.get("cand_name") or "").strip()
                if not county or not name:
                    continue
                party = normalize_party(row.get("party", ""))
                votes = int((row.get("ticket_num") or "0").replace(",", "") or 0)
                bucket = counties.setdefault(county, {"totalVotes": 0, "candidates": []})
                bucket["totalVotes"] += votes
                bucket["candidates"].append({"name": name, "party": party, "votes": votes})
                national[name]["party"] = party
                national[name]["votes"] += votes

    for bucket in counties.values():
        total = bucket["totalVotes"]
        bucket["candidates"].sort(key=lambda x: -x["votes"])
        for x in bucket["candidates"]:
            x["share"] = round(x["votes"] / total * 100, 2) if total else 0

    total = sum(x["votes"] for x in national.values())
    national_rows = [
        {"name": name, "party": val["party"], "votes": val["votes"],
         "share": round(val["votes"] / total * 100, 2) if total else 0}
        for name, val in sorted(national.items(), key=lambda x: -x[1]["votes"])
    ]
    return {"national": {"totalVotes": total, "candidates": national_rows}, "counties": counties}

president_2024 = aggregate_village_results("2024總統")
president_2020 = aggregate_village_results("2020總統")
mayor_towns_2022 = aggregate_mayor_towns()
partylist_2024 = aggregate_partylist()
president_2024["national"] = {"totalVotes": OFFICIAL_PRESIDENT_HISTORY[2024]["validVotes"], "candidates": OFFICIAL_PRESIDENT_HISTORY[2024]["candidates"]}
president_2020["national"] = {"totalVotes": OFFICIAL_PRESIDENT_HISTORY[2020]["validVotes"], "candidates": OFFICIAL_PRESIDENT_HISTORY[2020]["candidates"]}
partylist_2024["national"] = {"totalVotes": sum(x["votes"] for x in OFFICIAL_PARTYLIST_2024), "parties": OFFICIAL_PARTYLIST_2024}

payload = {
    "meta": {
        "source": "中央選舉委員會公開選舉資料",
        "aggregation": "總統與不分區資料彙整至鄉鎮市區；縣市長資料彙整至縣市及鄉鎮市區層級"
    },
    "president": {
        "year": 2024,
        "election": "第16任總統副總統選舉",
        **president_2024,
        "stats": OFFICIAL_PRESIDENT_HISTORY[2024]
    },
    "president2020": {
        "year": 2020,
        "election": "第15任總統副總統選舉",
        **president_2020,
        "stats": OFFICIAL_PRESIDENT_HISTORY[2020]
    },
    "presidentHistory": OFFICIAL_PRESIDENT_HISTORY,
    "partylist": {
        "year": 2024,
        "election": "第11屆立法委員全國不分區及僑居國外國民選舉",
        **partylist_2024
    },
    "mayor": {
        "year": 2022,
        "election": "111年直轄市長、縣市長選舉",
        **aggregate_mayor_csv((SRC_2022, SRC_2022_CITY)),
        "towns": mayor_towns_2022
    },
    "mayor2018": {
        "year": 2018,
        "election": "107年直轄市長、縣市長選舉",
        **aggregate_mayor_csv((SRC_2018, SRC_2018_CITY))
    }
}

OUT.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(f"Generated {OUT}: president={len(payload['president']['towns'])}, mayor_counties={len(payload['mayor']['counties'])}, mayor_towns={len(payload['mayor']['towns'])}, chiayi_districts={sum(1 for x in payload['mayor']['towns'].values() if x.get('county')=='嘉義市')}, mayor2018_counties={len(payload['mayor2018']['counties'])}")
