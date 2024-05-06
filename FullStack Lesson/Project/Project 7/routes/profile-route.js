const router = require("express").Router();
const authCheck = (req, res, next) => {
  if (req.isAuthenticated()) {
    next();
  } else {
    return res.redirect("/auth/login");
  }
};

router.get("/", authCheck, (req, res) => {
  // 在 deserializeUser() 內部, 已經設定好 req.user 是 user 在 DB 內部的 data
  console.log("進入 /profile ...");
  return res.render("profile", { user: req.user });
});

module.exports = router;
