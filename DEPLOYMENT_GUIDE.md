# 網站雲端部署指南 (Deployment Guide)

本文件紀錄了如何將「張天春詩文彙編網站」部署到免費的雲端主機上。
目前您的原始碼已上傳至 GitHub 儲存庫：[https://github.com/LoYinHao/Poetry](https://github.com/LoYinHao/Poetry)

由於本網站為純前端的靜態網站（由 HTML, CSS, JS 構成，無後端伺服器需求），我們強烈建議使用完全免費且整合度最高的 **GitHub Pages** 來進行部署。

---

## 推薦方案：使用 GitHub Pages 部署

GitHub Pages 是 GitHub 官方提供的免費靜態網頁託管服務，只要幾個點擊就能將您的專案轉換為公開的網站。

### 部署步驟

1. **前往專案設定頁面**
   打開瀏覽器，前往您的專案網址：
   [https://github.com/LoYinHao/Poetry/settings](https://github.com/LoYinHao/Poetry/settings)
   *(請確認您已經登入 GitHub)*

2. **進入 Pages 設定**
   在左側邊欄選單中，向下捲動找到並點擊 **Pages**。

3. **設定資料來源 (Source)**
   在 "Build and deployment" 區塊下：
   - **Source** 選單請保持選擇：**Deploy from a branch**
   - 在 **Branch** 的下拉式選單中：
     - 左邊選擇 **`main`** 分支
     - 右邊選擇資料夾 **`/(root)`**
   - 點擊右側的 **Save** (儲存) 按鈕。

4. **等待部署完成**
   - 儲存後，GitHub 會在背景自動開始建立您的網站。
   - 大約等待 1~3 分鐘。您可以在專案首頁點擊上方的 **Actions** 頁籤查看進度。
   - 當部署完成後，回到 **Pages** 設定頁面，上方會出現一段綠色提示，並提供您的網站專屬網址。

5. **您的專屬網址**
   部署成功後，您的網站網址通常會是：
   👉 **`https://LoYinHao.github.io/Poetry/`**

---

## 後續維護與更新

未來如果您修改了電腦上的程式碼（例如新增了詩詞、修改了外觀），只需要**將最新的進度推送到 GitHub**，GitHub Pages 就會**自動**幫您更新線上的網站！

**更新網站的指令 (在終端機執行)：**

```bash
# 1. 將所有變更加入追蹤
git add .

# 2. 存檔並輸入更新訊息
git commit -m "更新網站內容"

# 3. 推送到 GitHub (推上去後線上網站就會自動更新)
git push
```

---

## 其他備選方案

如果您未來需要更進階的功能，也可以考慮以下兩個對新手非常友善且免費的平台。它們都可以直接連動您的 GitHub 帳號並自動部署：

- **Vercel** (https://vercel.com) - 載入速度極快，前端開發者首選。
- **Netlify** (https://www.netlify.com) - 介面簡單直覺，支援直接拖曳資料夾上傳。
