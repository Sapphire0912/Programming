const express = require("express");
const app = express(); // 代表是 server 的意思

// HTTP request: GET, POST, PUT, DELETE
app.get("/", (req, res) => {
  res.send("歡迎來到網站首頁");
});

app.get("/anotherPage", (req, res) => {
  res.send("歡迎來到另一個頁面");
});

app.listen(3000, () => {
  console.log("伺服器正在 port 3000 上運行");
});
