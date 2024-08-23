const mongoose = require("mongoose");
const { Schema } = mongoose;
const bcrypt = require("bcrypt");

const userSchema = new Schema({
  username: {
    type: String,
    required: true,
    minlength: 3,
    maxlength: 10,
  },
  email: {
    type: String,
    required: true,
    minlength: 6,
    maxlength: 50,
  },
  password: {
    type: String,
    required: true,
  },
  role: {
    type: String,
    enum: ["student", "instructor"],
  },
  date: {
    type: Date,
    default: Date.now(),
  },
});

// instance methods
userSchema.methods.isStudent = function () {
  return this.role == "student";
};

userSchema.methods.isInstructor = function () {
  return this.role == "instructor";
};

userSchema.methods.comparePassword = async function (password, callbackFn) {
  let result;
  try {
    result = await bcrypt.compare(password, this.password);
    return callbackFn(null, result);
  } catch (error) {
    return callbackFn(error, result);
  }
};

// mongoose middlewares
// 若使用者是新用戶，或正在更改密碼，則將密碼進行雜湊處理
userSchema.pre("save", async function (next) {
  // this 代表 mongoDB 內的 document
  if (this.isNew || this.isModified("password")) {
    const hashValue = await bcrypt.hash(this.password, 10);
    this.password = hashValue;
  }
  next();
});

module.exports = mongoose.model("User", userSchema);
