const express = require("express");
const app = express();
const mongoose = require("mongoose");
const dotenv = require("dotenv");
dotenv.config();

const authRoute = require("./route").auth;
const courseRoute = require("./route").course;
const passport = require("passport");
require("./config/passport")(passport);

mongoose
  .connect("mongodb://localhost:27017/mernDB")
  .then(() => {
    console.log("連結到 to mongodb...");
  })
  .catch((e) => {
    console.log(e);
  });

// middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use("/api/user", authRoute);

// 只有登入系統的人才能夠新增課程或註冊課程 (JWT)
app.use(
  "/api/courses",
  passport.authenticate("jwt", { session: false }),
  courseRoute
);

app.listen(8080, () => {
  console.log("Server is running in port 8080.");
});
