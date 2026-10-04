# TAIWAN ELECTION MAP

以互動式地圖探索臺灣歷屆選舉結果的資料視覺化網站。

## 目前功能

- 總統副總統歷屆選舉地圖
- 縣市長歷屆選舉地圖
- 直轄市長歷史選舉資料
- 鄉鎮市區層級選舉結果
- 候選人得票數與得票率
- 政黨得票率與歷屆趨勢
- 歷屆政黨執政席次變化
- 互動式臺灣行政區地圖
- 桌面與行動裝置 RWD

## 資料來源

主要資料來源為 **中央選舉委員會公開選舉資料**。

- 中選會選舉資料庫：https://db.cec.gov.tw/
- 歷史資料經欄位標準化、候選人資料整理及行政區名稱對齊後，再提供網站使用。
- 不同選舉年度的行政區名稱與選舉制度可能不同，網站會依資料年度進行對齊與整理。
- 若網站資料與官方公告有差異，請以中央選舉委員會公布資料為準。

## 技術

- HTML / CSS / JavaScript
- D3.js
- ECharts
- TopoJSON
- Taiwan Atlas 行政區圖資
- GitHub Pages
- GitHub Actions

## 資料建置

歷史選舉資料不是手動寫入前端，而是透過 `scripts/build_election_data.py` 從公開資料來源整理產生 `data/elections.json`。

GitHub Actions 在部署前會執行資料完整性檢查，包括：

- 年度資料是否存在
- 候選人資料是否存在
- 得票數是否為有效數值
- 得票率是否介於 0–100%
- 行政區候選人是否重複
- 候選人得票數加總是否與該行政區總票數一致
- 候選人得票率加總是否合理
- 各選舉類型的年度資料是否完整

若驗證失敗，部署流程會停止，避免不完整資料直接上線。

## 專案結構

```text
.
├── index.html
├── data/
│   └── elections.json
├── scripts/
│   └── build_election_data.py
└── .github/
    └── workflows/
        └── pages.yml
```

## 公開網址

GitHub Pages：

https://dylan1211-hub.github.io/TAIWAN-ELECTION-MAP/

## 聲明

本專案為非官方的選舉資料視覺化專案，主要用途為資料查詢、研究與教育。

選舉資料、行政區資料及第三方函式庫均應依其原始來源與授權條款使用。

如果發現資料疑義、行政區對應錯誤或網站功能問題，歡迎提出 Issue。

## License

目前專案未另行宣告自有程式碼授權；若要公開供他人 fork、修改或再利用，建議後續補充適當的 LICENSE。