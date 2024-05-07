const router = require("express").Router();
const passport = require("passport");
const User = require("../models/user_model");
const bcrypt = require("bcrypt");

router.get("/login", (req, res) => {
  return res.render("login", { user: req.user });
});

router.get("/logout", (req, res) => {
  req.logOut((err) => {
    if (err) return res.send(err);
    return res.redirect("/");
  });
});

router.get("/signup", (req, res) => {
  return res.render("signup", { user: req.user });
});

router.get(
  "/google",
  passport.authenticate("google", {
    scope: ["profile", "email"],
    prompt: "select_account",
  })
);

router.post("/signup", async (req, res) => {
  let { name, email, password } = req.body;
  if (password.length < 8) {
    req.flash("error_msg", "密碼長度過短, 至少需要 8 個數字或英文");
    return res.redirect("/auth/signup");
  }

  const foundEmail = await User.findOne({ email }).exec();
  if (foundEmail) {
    req.flash(
      "error_msg",
      "信箱已經被註冊過了, 請使用另一個信箱或使用此信箱登入系統"
    );
    return res.redirect("/auth/signup");
  }

  let hashedPassword = await bcrypt.hash(password, 12);
  let newUser = new User({
    name,
    email,
    password: hashedPassword,
  });
  await newUser.save();
  req.flash("success_msg", "註冊成功, 現在可以使用此帳號登入系統");
  return res.redirect("/auth/login");
});

router.post(
  "/login",
  passport.authenticate("local", {
    failureRedirect: "/auth/login",
    failureFlash: "登入失敗, 帳號或密碼不正確",
  }),
  (req, res) => {
    return res.redirect("/profile");
  }
);

// 要通過 google 驗證才能使用的 route, 需要先用 passport 的 middle 來驗證
router.get("/google/redirect", passport.authenticate("google"), (req, res) => {
  console.log("進入 redirect 區域...");
  return res.redirect("/profile");
});

module.exports = router;
