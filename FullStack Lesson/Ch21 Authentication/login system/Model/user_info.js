const mongoose = require("mongoose");
const { Schema } = mongoose;

mongoose
  .connect("mongodb://localhost:27017/loginSystem")
  .then(() => {
    console.log("成功連結到 loginSystem 資料庫");
  })
  .catch((e) => {
    console.log(e);
  });

const usersSchema = new Schema({
  username: { type: String, required: true, maxlength: 25 },
  password: { type: String, required: true, minlength: 6 },
  salary: {
    type: Number,
    default: 20000,
    min: [0, "薪資不能是負數"],
    required: true,
  },
});

const User = mongoose.model("LoginPrac", usersSchema);
module.exports = User;
