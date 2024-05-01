const express = require("express");
const app = express();
// const cors = require("cors");
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

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
// app.use(cors());

app.get("/students", async (req, res) => {
  try {
    let studentsData = await Student.find({}).exec();
    // 利用 API 來串接資料庫
    // return res.send(studentsData);
    // 利用網頁來回傳資訊
    return res.render("students", { studentsData });
  } catch (e) {
    return res.status(500).send("尋找資料時發生錯誤!");
  }
});

app.get("/students/:_id", async (req, res) => {
  let { _id } = req.params;
  try {
    let foundStudent = await Student.findOne({ _id }).exec();
    // console.log(foundStudent == null);
    if (foundStudent != null) {
      // 利用 API 來串接資料庫
      // return res.send(foundStudent);
      // 利用網頁來回傳資訊
      return res.render("students-page", { foundStudent });
    } else {
      // return res.send(
      //   "沒有名為 " + _id + " 學生的資料, 請確認名稱是否輸入正確"
      // );
      return res.render("student-not-found", {
        msg: "沒有名為 " + _id + " 學生的資料, 請確認名稱是否輸入正確",
      });
    }
  } catch (e) {
    // return res.status(500).send("尋找資料時發生錯誤!");
    return res
      .status(400)
      .render("student-not-found", { msg: "尋找資料時發生錯誤!" });
  }
});

app.post("/students", async (req, res) => {
  try {
    let { name, age, major, merit, other } = req.body;
    //   console.log(name, age, major, merit, other);
    let newStudent = new Student({
      name,
      age,
      major,
      scholarship: { merit, other },
    });
    let savedStudent = await newStudent.save();
    return res.send({
      msg: "資料儲存成功",
      saveObject: savedStudent,
    });
  } catch (e) {
    return res
      .status(400)
      .send("儲存資料時發生錯誤! " + "錯誤訊息如下: " + e.message);
  }
});

app.put("/students/:_id", async (req, res) => {
  try {
    let { _id } = req.params;
    let { name, age, major, merit, other } = req.body;
    let updateData = await Student.findOneAndUpdate(
      { _id },
      { name, age, major, scholarship: { merit, other } },
      { runValidators: true, new: true, overwrite: true }
      // overwrite 會覆蓋所有的數據, 因為 HTTP put request 要求客戶端提供所有數據,
      // 所以我們要根據客戶端提供的數據來更新資料庫內的資料
    );
    return res.send({ msg: "成功更新學生資料", updateData });
  } catch (e) {
    return res
      .status(400)
      .send("更新資料時發生錯誤! " + "錯誤訊息如下: " + e.message);
  }
});

app.patch("/students/:_id", async (req, res) => {
  try {
    let { _id } = req.params;
    let { name, age, major, merit, other } = req.body;

    let updateData = await Student.findOneAndUpdate(
      { _id },
      {
        name,
        age,
        major,
        "scholarship.merit": merit,
        "scholarship.other": other,
      },
      {
        new: true,
        runValidator: true,
      }
    );
    return res.send({ msg: "成功更新學生資料", updateData });
  } catch (e) {
    return res
      .status(400)
      .send("更新資料時發生錯誤! " + "錯誤訊息如下: " + e.message);
  }
});

app.delete("/students/:_id", async (req, res) => {
  try {
    let { _id } = req.params;
    let deleteData = await Student.deleteOne({ _id });
    if (deleteData.deletedCount == 0) {
      return res
        .status(200)
        .send(`沒有 id = ${_id}的資料!, 請檢查是否輸入正確`);
    } else {
      return res.send({ msg: "成功刪除資料", _id });
    }
  } catch (e) {
    return res
      .status(500)
      .send("刪除資料時發生錯誤! " + "錯誤訊息如下: " + e.message);
  }
});

app.listen(3000, () => {
  console.log("server 正在 Port 3000 運行...");
});
