from pathlib import Path
import re

p = Path("index.html")
s = p.read_text(encoding="utf-8")

if "UI-POLISH-V1" in s:
    print("UI polish already applied")
    raise SystemExit(0)

new_sidebar = r'''<aside class="side">
  <div class="brand">
    <div class="brand-mark">TEM</div>
    <div>
      <h1>TAIWAN ELECTION MAP</h1>
      <div class="sub">臺灣歷年選舉地圖資料平台</div>
    </div>
  </div>

  <div class="side-section-label">資料選擇</div>
  <div class="filter-current" id="filterCurrent">2024 · 總統副總統</div>
  <details class="filter-panel" open>
    <summary>
      <span><strong>選舉與區域</strong><small>依序選擇即可更新地圖</small></span>
      <span class="chevron">⌄</span>
    </summary>
    <div class="filter-body">
      <label class="field">
        <span>選舉類型</span>
        <div class="select-wrap">
          <select class="select" id="electionType">
            <option value="president">總統副總統</option>
            <option value="mayor">縣市長</option>
          </select>
        </div>
      </label>
      <label class="field">
        <span>年份</span>
        <div class="select-wrap">
          <select class="select" id="year"><option value="2024">2024</option></select>
        </div>
      </label>
      <div class="filter-divider"></div>
      <label class="field">
        <span>縣市 <em>可選</em></span>
        <div class="select-wrap">
          <select class="select" id="county"><option value="">全臺</option></select>
        </div>
      </label>
      <label class="field">
        <span>鄉鎮市區 <em>先選縣市</em></span>
        <div class="select-wrap">
          <select class="select" id="town"><option value="">選擇鄉鎮市區…</option></select>
        </div>
      </label>
      <button class="clear-filter" id="clearSelectionUi" type="button">↺　清除區域選擇</button>
    </div>
  </details>

  <div class="selection-guide">
    <div class="guide-dot"></div>
    <div>
      <strong>也可以直接點地圖</strong>
      <span>點選行政區查看詳細結果</span>
    </div>
  </div>

  <div class="side-legend">
    <div class="side-legend-title">政黨色彩</div>
    <div class="party-key"><i class="party-dot dpp"></i><span>民主進步黨</span></div>
    <div class="party-key"><i class="party-dot kmt"></i><span>中國國民黨</span></div>
    <div class="party-key"><i class="party-dot tpp"></i><span>台灣民眾黨</span></div>
  </div>
</aside>'''

m = re.search(r'<aside class="side">.*?</aside>', s, re.S)
if not m:
    raise SystemExit("sidebar block not found")
s = s[:m.start()] + new_sidebar + s[m.end():]

css = r'''
/* UI-POLISH-V1 */
:root{--bg:#070b12;--panel:#0c131d;--panel2:#101a27;--line:#263548;--line2:#314156;--text:#edf3f9;--muted:#8291a6;--cyan:#67d5ff;--green:#1b9e3f;--blue:#2f6fd6;--tpp:#19a7ce}
body{scrollbar-color:#33445a #0b121c;scrollbar-width:thin}
body::-webkit-scrollbar,.side::-webkit-scrollbar,.right::-webkit-scrollbar,.mayor-analysis-scroll::-webkit-scrollbar{width:7px;height:7px}
body::-webkit-scrollbar-track,.side::-webkit-scrollbar-track,.right::-webkit-scrollbar-track,.mayor-analysis-scroll::-webkit-scrollbar-track{background:#0a111a}
body::-webkit-scrollbar-thumb,.side::-webkit-scrollbar-thumb,.right::-webkit-scrollbar-thumb,.mayor-analysis-scroll::-webkit-scrollbar-thumb{background:#33445a;border-radius:99px;border:1px solid #0a111a}
body::-webkit-scrollbar-thumb:hover,.side::-webkit-scrollbar-thumb:hover,.right::-webkit-scrollbar-thumb:hover,.mayor-analysis-scroll::-webkit-scrollbar-thumb:hover{background:#4a5e78}
.app{grid-template-columns:246px minmax(0,1fr) 350px;grid-template-rows:minmax(0,1fr) 292px}
.side,.right{padding:16px 17px}.side{background:linear-gradient(180deg,#0c131d,#0a111a);border-right:1px solid #202d3d;overflow-y:auto}.right{background:#0b121b;border-left:1px solid #202d3d;overflow-y:auto}
.map{background:#060b12}.mapbar{left:16px;top:14px;padding:8px 11px;background:#0a111ae0;border-color:#314156;border-radius:10px;box-shadow:0 8px 24px #0005;color:#b3c0cf}.map-legend{left:16px;bottom:16px;width:215px;padding:11px 12px;background:#0a111ae8;border-color:#314156}
.zoom-controls{right:16px;bottom:16px}.zoom-controls button{width:32px;height:32px;border-radius:9px;background:#0d1722;border-color:#314156;box-shadow:0 5px 15px #0005;cursor:pointer}.zoom-controls button:hover{background:#172535;border-color:#48617e}
.brand{display:flex;align-items:flex-start;gap:10px;padding:3px 2px 11px}.brand-mark{width:30px;height:30px;border:1px solid #38516a;border-radius:9px;display:grid;place-items:center;font-size:9px;font-weight:800;letter-spacing:.08em;color:#bfeaff;background:#0d1c29}.brand h1{font-size:15px;letter-spacing:.075em;line-height:1.1;margin:2px 0 4px}.brand .sub{font-size:10px;margin:0;color:#718198}
.side-section-label{font-size:9px;color:#5f7085;letter-spacing:.14em;margin:4px 2px 5px}.filter-current{font-size:9px;color:#9eb0c3;background:#0d1824;border:1px solid #223449;border-radius:7px;padding:6px 8px;margin-bottom:7px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.filter-panel{border:1px solid #2a3a4e;border-radius:12px;background:#0f1824;overflow:hidden}.filter-panel summary{list-style:none;cursor:pointer;padding:10px 12px;display:flex;align-items:center;justify-content:space-between;gap:8px}.filter-panel summary::-webkit-details-marker{display:none}.filter-panel summary strong{display:block;font-size:12px;color:#e7edf5}.filter-panel summary small{display:block;margin-top:3px;color:#718198;font-size:9px}.chevron{color:#718198;font-size:16px;line-height:1;transition:transform .18s}.filter-panel[open] .chevron{transform:rotate(180deg)}.filter-body{padding:0 11px 10px}
.field{display:block;margin:0 0 8px}.field>span{display:flex;justify-content:space-between;align-items:center;color:#8494a9;font-size:9px;margin:0 1px 5px}.field em{font-style:normal;color:#56687d;font-size:8px}.select-wrap{position:relative}.select-wrap:after{content:"⌄";position:absolute;right:10px;top:50%;transform:translateY(-55%);pointer-events:none;color:#6f8196;font-size:13px}.select{appearance:none;-webkit-appearance:none;width:100%;height:35px;padding:0 30px 0 10px;background:#111d2a;color:#e8eef5;border:1px solid #2c3c50;border-radius:8px;font-size:11px;outline:none;cursor:pointer}.select:hover{background:#142233;border-color:#3c526b}.select:focus{border-color:#4e6b88;box-shadow:0 0 0 3px #67d5ff12}.filter-divider{height:1px;background:#223044;margin:10px 0}.clear-filter{width:100%;height:30px;background:#0c1520;color:#91a0b2;border:1px solid #29394d;border-radius:8px;font-size:10px;cursor:pointer}.clear-filter:hover{background:#142131;color:#dbe5ef;border-color:#40546b}
.selection-guide{display:flex;align-items:center;gap:9px;margin:11px 1px 9px;padding:9px 10px;border:1px solid #1f3042;border-radius:10px;background:#0c1621}.guide-dot{width:7px;height:7px;flex:0 0 7px;border-radius:50%;background:#67d5ff;box-shadow:0 0 0 4px #67d5ff12}.selection-guide strong,.selection-guide span{display:block}.selection-guide strong{font-size:9px;color:#b9c6d4}.selection-guide span{font-size:8px;color:#66778c;margin-top:2px}.side-legend{border-top:1px solid #1e2c3d;padding:9px 1px 0}.side-legend-title{font-size:8px;color:#5f7085;letter-spacing:.1em;margin-bottom:6px}.party-key{display:flex;align-items:center;gap:7px;font-size:9px;color:#8797aa;margin:5px 0}.party-dot{width:7px;height:7px;border-radius:50%;display:block}.party-dot.dpp{background:var(--green)}.party-dot.kmt{background:var(--blue)}.party-dot.tpp{background:var(--tpp)}
.right .title{font-size:9px;letter-spacing:.08em;color:#627389;margin-bottom:3px}.place{font-size:23px;line-height:1.15;margin-bottom:7px;font-weight:750}.badge{padding:4px 8px;margin-bottom:8px;border-radius:999px;background:#101c29;border-color:#2c3e53;color:#8fa0b4;font-size:8px}.winner-card{margin:7px 0 9px;padding:11px 12px;background:#111c28;border:1px solid #32455a;border-radius:11px;box-shadow:0 8px 22px #0003}.winner-label{font-size:8px;color:#72849a;letter-spacing:.08em}.winner-name{font-size:20px;line-height:1.15;margin-top:3px}.winner-party{font-size:10px;font-weight:700;margin-top:4px}.winner-share{font-size:9px;margin-top:5px;color:#9caabd}.winner-note{font-size:9px;line-height:1.45;color:#718198;margin-top:5px}.metric{padding:7px 0;font-size:10px;border-bottom-color:#263548}.data-level{font-size:8px;margin:5px 0 8px;color:#61738a}.right-summary{gap:6px;margin:6px 0 2px}.right-summary .kpi-card{padding:8px;border-radius:9px;background:#101a27;border-color:#26384c}.kpi-label{font-size:8px}.kpi-value{font-size:14px;margin-top:3px}.section-title{font-size:9px;letter-spacing:.05em;margin:12px 0 6px;color:#74869b}.pie-wrap{height:175px}.pie-wrap #voteShareChart{height:175px}.mini-chart{height:115px}.source{margin-top:9px;padding-top:8px;border-top:1px solid #1d2b3b;font-size:8px;line-height:1.5;color:#596b81}
.history-panel{padding:10px 14px;gap:10px;background:#0a111a;border-top:1px solid #202e3e;grid-template-columns:1.05fr 1fr 1.3fr;align-items:stretch}.history-card{padding:10px;border-radius:11px;background:#101a27;border-color:#293b50;display:flex;flex-direction:column;min-height:0}.history-head{margin-bottom:7px}.history-title{font-size:11px}.history-sub{font-size:8px;margin-top:3px}.history-chart{height:225px;min-height:0;flex:1}.history-cards{grid-template-columns:repeat(4,1fr);gap:6px}.history-year-card{padding:7px;border-radius:8px;background:#0d1722;border-color:#24364a}.history-year{font-size:8px}.history-winner{font-size:13px;margin-top:3px}.history-meta{font-size:8px;margin-top:2px}.history-stat{font-size:8px;margin-top:3px}.mayor-analysis-scroll{height:230px;min-height:0;flex:1;position:relative;padding-right:6px}.mayor-analysis-scroll:after{content:"向下查看更多";position:sticky;bottom:2px;display:block;width:max-content;margin:0 auto;padding:3px 7px;border:1px solid #304257;border-radius:99px;background:#0c1621e8;color:#72859b;font-size:7px;pointer-events:none}.mayor-only{height:430px}.mayor-seat-chart{height:230px;min-height:0;flex:1}.history-panel.mayor-layout{grid-template-columns:1.15fr 1fr}.history-panel.mayor-layout .history-card{min-width:0}.history-panel.mayor-layout .mayor-seat-card,.history-panel.mayor-layout .mayor-seat-card[style]{display:flex!important}.history-panel .echarts{overflow:hidden}
.party-text.dpp{color:var(--green)!important}.party-text.kmt{color:var(--blue)!important}.party-text.tpp{color:var(--tpp)!important}.party-text.other{color:#93a0b1!important}.winner-card.party-dpp{border-color:#1b9e3f66;box-shadow:inset 3px 0 0 var(--green),0 8px 22px #0003}.winner-card.party-kmt{border-color:#2f6fd666;box-shadow:inset 3px 0 0 var(--blue),0 8px 22px #0003}.winner-card.party-tpp{border-color:#19a7ce66;box-shadow:inset 3px 0 0 var(--tpp),0 8px 22px #0003}
@media (max-width:1200px){.app{grid-template-columns:220px minmax(0,1fr) 320px;grid-template-rows:minmax(0,1fr) 300px}.history-panel{grid-template-columns:1fr 1fr}.history-card#historyCardShare{display:none}}
@media (max-width:900px){body{overflow:auto}.app{height:auto;min-height:100vh;display:grid;grid-template-columns:1fr;grid-template-rows:auto 55vh auto auto}.side{border-right:0;border-bottom:1px solid #202d3d;overflow:visible}.right{border-left:0;border-top:1px solid #202d3d;overflow:visible}.map{min-height:55vh}.history-panel{grid-row:auto;grid-template-columns:1fr!important;height:auto;overflow:visible}.history-card{min-height:260px}.mayor-seat-card{display:flex}}
'''
s = s.replace("</style>", css + "</style>", 1)

js = r'''
/* UI-POLISH-V1 behavior */
(function(){
  const partyClass=p=>{const v=String(p||"");if(v.includes("民主進步黨"))return "dpp";if(v.includes("中國國民黨"))return "kmt";if(v.includes("台灣民眾黨"))return "tpp";return "other"};
  const decorate=()=>{
    document.querySelectorAll(".history-meta").forEach(el=>{const t=el.textContent||"";const p=["民主進步黨","中國國民黨","台灣民眾黨","親民黨"].find(x=>t.includes(x));el.classList.add("party-text",partyClass(p))});
    const wp=document.querySelector(".winner-party");if(wp)wp.classList.add("party-text",partyClass(wp.textContent));
    const card=document.getElementById("winnerCard");const party=wp?.textContent||"";card?.classList.remove("party-dpp","party-kmt","party-tpp","party-other");if(party)card.classList.add("party-"+partyClass(party));
  };
  const updateFilterCurrent=()=>{const el=document.getElementById("filterCurrent");if(!el)return;const type=document.getElementById("electionType")?.selectedOptions?.[0]?.textContent||"";const year=document.getElementById("year")?.selectedOptions?.[0]?.textContent||"";const county=document.getElementById("county")?.selectedOptions?.[0]?.textContent||"全臺";const town=document.getElementById("town")?.selectedOptions?.[0]?.textContent||"";el.textContent=year+" · "+type+(county&&county!=="全臺"?" · "+county:"")+(town&&town!=="選擇鄉鎮市區…"?" · "+town:"")};
  const oldUpdate=window.updatePanel;if(typeof oldUpdate==="function"){window.updatePanel=function(name,data){oldUpdate(name,data);decorate();updateFilterCurrent()}};
  const clear=document.getElementById("clearSelectionUi");clear?.addEventListener("click",()=>{const county=document.getElementById("county"),town=document.getElementById("town");if(county){county.value="";county.dispatchEvent(new Event("change"))}if(town)town.value="";updateFilterCurrent()});
  ["electionType","year","county","town"].forEach(id=>document.getElementById(id)?.addEventListener("change",updateFilterCurrent));
  updateFilterCurrent();decorate();
})();
'''
s = s.replace("</script>", js + "</script>", 1)
p.write_text(s, encoding="utf-8")
print("UI polish applied")
