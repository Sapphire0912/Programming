const express = require("express");
const app = express();
const cookieParser = require("cookie-parser");
const session = require("express-session");

app.use(cookieParser("sapphire"));
app.use(
  session({
    secret: "Sapphire and Ruby, Which one is correct?",
    resave: false,
    saveUninitialized: false,
    cookie: { secure: false },
  })
);

app.get("/", (req, res) => {
  return res.send("This is a home page");
});

app.get("/setCookie", (req, res) => {
  //   res.cookie("yourCookie", "Oreo");
  res.cookie("yourCookie", "Oreo", { signed: true });
  return res.send("已經設定 cookies");
});

app.get("/seeCookie", (req, res) => {
  console.log(req.signedCookies);
  return res.send("看一下已經設定好的 cookies:" + req.signedCookies.yourCookie);
});

app.get("/setSessionData", (req, res) => {
  // console.log(req.session);
  req.session.example = "something not important...";
  return res.send(
    "在 server 設置 session data, 在 browser 設置簽名後的 session id."
  );
});

app.get("/seeSessionData", (req, res) => {
  console.log(req.session);
  return res.send("看一下已經設定好的 session:" + req.session.example);
});

app.get("/verifyUser", (req, res) => {
  req.session.isVerified = true;
  return res.send("已經被驗證了");
});

app.get("/secret", (req, res) => {
  if (!req.session.isVerified) {
    return res.send("請先登入系統，才能看見內容");
  } else {
    return res.send("Sapphire~!");
  }
});

app.listen(3000, () => {
  console.log("Server running on port 3000....");
});
