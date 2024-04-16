const express = require("express");
const app = express(); // 代表是 server 的意思

// middleware
app.use(express.json());
app.use(express.urlencoded({ extends: true }));
app.use(express.static("public"));

// app.use((req, res, next) => {
//   console.log("正在經過 middleware");
//   next();
// });

// app.use((req, res, next) => {
//   console.log("正在經過第二個 middleware");
//   next();
// });

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

app.get("/middlewareUse", (req, res) => {
  res.sendFile(__dirname + "/index.html");
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

app.get("/fruit", (req, res) => {
  res.send("歡迎來到水果頁面");
});

app.get("/fruit/:someFruit", (req, res) => {
  // console.log(req.params.someFruit);
  res.send("歡迎來到" + req.params.someFruit + "頁面");
});

app.get("/actualExample", (req, res) => {
  res.send("真正的 resourse 在這裡");
});

// app.get("/formHandling", (req, res) => {
//   // console.log(req.query); // 會得到使用者表單的內容
//   res.send(
//     "伺服器已經收到表單。你所提交的資料為。名稱: " +
//       req.query.name +
//       ". 以及年齡為: " +
//       req.query.age
//   );
// });

app.post("/formHandling", (req, res) => {
  // console.log(req.body); // 獲取被 middleware 處理過的 form 內容
  let { email, password } = req.body;
  res.send("Your email: " + email + ". your password: " + password);
});

// app.get("*", (req, res) => {
//   res.send("你找的頁面不存在");
// });

app.get("*", (req, res) => {
  // res.status(404); // return res object, 它屬於 method chaining
  // res.send("錯誤頁面");
  res.status(404).send("錯誤頁面");
});

app.listen(3000, () => {
  console.log("伺服器正在 port 3000 上運行");
});
