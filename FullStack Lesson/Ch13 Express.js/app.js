const express = require("express");
const app = express(); // 代表是 server 的意思

// HTTP request: GET, POST, PUT, DELETE
app.get("/", (req, res) => {
  res.send("歡迎來到網站首頁");
});

app.get("/anotherPage", (req, res) => {
  res.send("歡迎來到另一個頁面");
});

app.get("/example", (req, res) => {
  res.send("<h1>this is a h1 tag example.");
  //   res.send("<p>this is a `<p>` tag.</p>");
  // Error [ERR_HTTP_HEADERS_SENT]: Cannot set headers after they are sent to the client
});

app.get("/sendFile", (req, res) => {
  // sendFile(path) 必須是絕對路徑
  res.sendFile(__dirname + "/example.html");
});

app.get("/json", (req, res) => {
  let object = {
    title: "Web Design",
    website: "PersonalPC",
  };
  res.json(object);
});

app.get("/redirect", (req, res) => {
  res.redirect("/actualExample");
});

app.get("/actualExample", (req, res) => {
  res.send("真正的 resourse 在這裡");
});

app.listen(3000, () => {
  console.log("伺服器正在 port 3000 上運行");
});
