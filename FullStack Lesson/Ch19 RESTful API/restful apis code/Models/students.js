const mongoose = require("mongoose");
const { Schema } = mongoose;

// 建立 Schema
const studentSchema = new Schema({
  name: { type: String, minlength: 2, maxlength: 25, required: true },
  age: {
    type: Number,
    min: [14, "年齡不能小於 18"],
    max: [80, "年齡不能超過 80"],
    default: 18,
  },
  major: {
    type: String,
    required: true,
    enum: [
      "Chemistry",
      "Computer Science",
      "Mathematics",
      "Arts",
      "ML/DL",
      "Operating System",
      "Algorithm",
    ],
  },
  scholarship: {
    merit: {
      type: Number,
      min: 0,
      max: [5000, "學生的 merit scholarship 太多了"],
      default: 0,
    },
    other: { type: Number, min: 0, default: 0 },
  },
});

// 創建一個 collection
const Students = mongoose.model("Student", studentSchema);

module.exports = Students; // review: 這是 express.js 的作法
