const express = require("express");
const app = express();
const mongoose = require("mongoose");
const Student = require("./Models/students");

app.set("view engine", "ejs");

mongoose
  .connect("mongodb://localhost:27017/restfulAPIDB")
  .then(() => {
    console.log("成功連結到 MongoDB...");
  })
  .catch((e) => {
    console.log(e);
  });

app.get("/students", async (req, res) => {
  try {
    let studentsData = await Student.find({}).exec();
    return res.send(studentsData);
  } catch (e) {
    return res.status(500).send("尋找資料時發生錯誤!");
  }
});

app.post("/students", (req, res) => {
  console.log();
});

app.listen(3000, () => {
  console.log("server 正在 Port 3000 運行...");
});
