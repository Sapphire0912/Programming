const express = require("express");
const app = express();
const birds = require("./birds");

app.use("/birds", birds);

app.get("/", (req, res) => {
  res.send("main app home page");
});

app.get("/new", (req, res) => {
  res.send("main app new page");
});

app.listen(3000, (req, res) => {
  console.log("server...");
});
