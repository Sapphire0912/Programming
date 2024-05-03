const express = require("express");
const app = express();
const User = require("./Model/user_info");
const mongoose = require("mongoose");
const bcrypt = require("bcrypt");

app.set("view engine", "ejs");
mongoose
  .connect("mongodb://localhost:27017/loginSystem")
  .then(() => {
    console.log("成功連結到 MongoDB...");
  })
  .catch((e) => {
    console.log(e);
  });

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.get("/Users", async (req, res) => {
  try {
    let allUsers = await User.find({});
    let userNames = [];
    allUsers.forEach((data) => {
      userNames.push(data.username);
    });
    res.send(`以下為該系統的所有用戶:\n ${userNames}`);
  } catch (e) {
    res.send(e);
  }
});
app.post("/newUser", async (req, res) => {
  try {
    let { username, password, salary } = req.body;
    let hashValue = await bcrypt.hash(password, 12);
    let newUser = new User({
      username,
      password: hashValue,
      salary,
    });
    let saveUser = await newUser.save();
    return res.send({ msg: "用戶新增成功", saveUser });
  } catch (e) {
    return res.send(e);
  }
});

app.post("/Userlogin", async (req, res) => {
  try {
    let { username, password } = req.body;
    let foundUser = await User.findOne({ username });
    if (foundUser != null) {
      let result = await bcrypt.compare(password, foundUser.password);
      if (result) {
        return res.send(`登入成功, 該帳戶的薪資為 ${foundUser.salary}`);
      } else {
        return res.send(`登入失敗, 請檢查密碼是否輸入錯誤`);
      }
    } else {
      return res.send(`請檢查信箱 ${username} 是否輸入錯誤`);
    }
  } catch (e) {
    return res.send(e);
  }
});

app.listen(3000, () => {
  console.log("Server 正在運行...");
});
