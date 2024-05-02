const express = require("express");
const router = express.Router();

router.get("/", (req, res) => {
  res.send("Birds home page");
});
router.get("/new", (req, res) => {
  res.send("Birds new Page");
});

module.exports = router;
