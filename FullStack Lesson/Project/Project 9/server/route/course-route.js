const router = require("express").Router();
const Course = require("../models").course;
const courseValidation = require("../validation").courseValidation;

router.use((req, res, next) => {
  console.log("course route 正在接受一個 req");
  next();
});

router.get("/", async (req, res) => {
  try {
    let courseFound = await Course.find({})
      .populate("instructor", ["username", "email"]) // 根據 instructor 去對應到和 instructor 的資料
      .exec();
    return res.send(courseFound);
  } catch (e) {
    return res.status(500).send(e);
  }
});

// 使用課程 id 尋找課程
router.get("/:_id", async (req, res) => {
  let { _id } = req.params;
  try {
    let courseFound = await Course.findOne({ _id })
      .populate("instructor", ["email"])
      .exec();
    return res.send(courseFound);
  } catch (e) {
    return res.status(500).send(e);
  }
});

// 新增課程
router.post("/", async (req, res) => {
  let { error } = courseValidation(req.body);
  if (error) return res.status(400).send(error.details[0].message);

  if (req.user.isStudent()) {
    return res.status(400).send("只有講師才能發佈新課程");
  }

  let { title, description, price } = req.body;
  try {
    let newCourse = new Course({
      title,
      description,
      price,
      instructor: req.user._id,
    });
    let savedCourse = await newCourse.save();
    return res.status(200).send("新課程已經保存");
  } catch (e) {
    return res.status(500).send("無法創建課程");
  }
});

// 更改課程
router.patch("/:_id", async (req, res) => {
  let { error } = courseValidation(req.body);
  if (error) return res.status(400).send(error.details[0].message);

  // 確認課程是否存在
  let { _id } = req.params;
  try {
    let courseFound = await Course.findOne({ _id });
    if (!courseFound)
      return res.status(400).send("找不到課程，無法更新課程內容");

    // 使用者必須是此課程講師才能編輯課程
    if (courseFound.instructor.equals(req.user._id)) {
      let updateCourse = await Course.findOneAndUpdate({ _id }, req.body, {
        new: true,
        runValidators: true,
      });
      return res.send({
        msg: "課程已經被更新過了",
        updateCourse,
      });
    } else {
      return res.status(403).send("只有此課程講師才可以編輯課程");
    }
  } catch (e) {
    return res.status(500).send(e);
  }
});

// 刪除課程
router.delete("/:_id", async (req, res) => {
  let { error } = courseValidation(req.body);
  if (error) return res.status(400).send(error.details[0].message);

  // 確認課程是否存在
  let { _id } = req.params;
  try {
    let courseFound = await Course.findOne({ _id });
    if (!courseFound) return res.status(400).send("找不到課程，無法刪除課程");

    // 使用者必須是此課程講師才能編輯課程
    if (courseFound.instructor.equals(req.user._id)) {
      let deleteCourse = await Course.deleteOne({ _id }).exec();
      return res.send(deleteCourse);
    } else {
      return res.status(403).send("只有此課程講師才可以刪除課程");
    }
  } catch (e) {
    return res.status(500).send(e);
  }
});
module.exports = router;
