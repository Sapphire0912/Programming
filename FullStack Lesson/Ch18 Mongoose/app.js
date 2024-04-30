const express = require("express");
const app = express();
const mongoose = require("mongoose");
const { Schema } = mongoose;

app.set("view engine", "ejs");

mongoose
  .connect("mongodb://localhost:27017/mongoDBPrac")
  .then(() => {
    console.log("成功連結 mongoDB");
  })
  .catch((e) => {
    console.log(e);
  });

// 連結 mongodb 的 collection 操作
const studentSchema = new Schema(
  {
    name: { type: String, required: true, maxlength: 25 },
    age: { type: Number, min: [0, "age is not less than 0."], default: 18 },
    //   major: { type: String, required: [true, "每個學生都至少要選一個主修"] },
    major: {
      type: String,
      required: function () {
        return this.age >= 20;
      },
      enum: ["Chemistry", "Computer Science", "Mathematics", "Arts"],
    },
  },
  {
    methods: {
      printMajor() {
        return this.major;
      },
    },
    statics: {
      findMajor(major) {
        return this.find({ major: major }).exec();
      },
    },
  }
);

// 第二種方式
studentSchema.methods.studentAge = function () {
  return this.age;
};

const Student = mongoose.model("Student", studentSchema);
Student.findMajor("Chemistry")
  .then((data) => {
    console.log(data);
  })
  .catch((e) => {
    console.log(e);
  });

// Student.find({})
//   .exec()
//   .then((arr) => {
//     arr.forEach((student) => {
//       console.log(student.name + " 的主修科目為: " + student.printMajor());
//       console.log(student.name + " 的年紀為: " + student.studentAge());
//     });
//   });

// Student.deleteOne({ age: { $lt: 24 } })
//   .exec()
//   .then((msg) => {
//     console.log(msg);
//   })
//   .catch((e) => {
//     console.log(e);
//   });

// 使用 findOneAndUpdate()
// Student.findOneAndUpdate(
//   { name: "Iris" },
//   { age: 24 },
//   { runValidator: true, new: true }
// )
//   .then((doc) => {
//     console.log("new: true, the doc is after update data");
//     console.log(doc);
//   })
//   .catch((e) => {
//     console.log(e);
//   });

// const newStudent = new Student({
//   name: "Mary",
//   age: 30,
//   major: "Computer Science",
// });
// newStudent
//   .save()
//   .then((data) => {
//     console.log("successful. save new student information.");
//   })
//   .catch((e) => {
//     console.log(e);
//   });

// 在 DB 中更新一筆數據，如下：
// new: true 對於 updateOne() 是沒有作用的
// Student.updateOne({ age: 25 }, { age: 24 }, { runValidators: true, new: true })
//   .exec()
//   .then((message) => {
//     console.log(message);
//   })
//   .catch((e) => {
//     console.log(e);
//   });

// 在 DB 新增數據，如下：
// const newObject = new Student({
//   name: "Aurora",
//   age: 23,
//   major: "Mathematics",
// });

// newObject
//   .save()
//   .then((savedDoc) => {
//     console.log("Data 已經儲存完畢，儲存成功");
//     console.log("儲存的資料是：", savedDoc);
//   })
//   .catch((e) => {
//     console.log("Data 儲存失敗, ", e);
//   });

// 在 DB 中查詢資料
// Student.find({})
//   .exec()
//   .then((data) => {
//     console.log(data);
//   });

// 結合 Web Server 的寫法
app.get("/", async (req, res) => {
  try {
    let data = await Student.find({}).exec(); // return Promise Object
    // let data = await Student.findOne({ name: "Sapphire" }).exec();
    res.send(data);
  } catch (e) {
    res.send(e);
  }
});

app.listen(3000, () => {
  console.log("server 正在聆聽 server 3000...");
});
