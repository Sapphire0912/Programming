const passport = require("passport");
const GoogleStrategy = require("passport-google-oauth20");
const User = require("../models/user_model");

passport.serializeUser((user, done) => {
  console.log("serialize 使用者...");
  //   console.log(user);
  done(null, user._id);
  // 將 database 的 _id 儲存在 session 內部;
  // 並且將 _id 簽名後, 以 cookie 的形式給 user
});

passport.deserializeUser(async (_id, done) => {
  // _id: 是 done() 執行之後會得到 serializeUser() 中的 done() -> user._id 的部分
  console.log(
    "deserialize 使用者... 使用 serializeUser 儲存的 _id, 去找到 database 內的 data"
  );
  let foundUser = await User.findOne({ _id }).exec();
  done(null, foundUser); // 將 req.user 屬性設定為 foundUser
});

passport.use(
  new GoogleStrategy(
    {
      clientID: process.env.GOOGLE_CLIENT_ID,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET,
      callbackURL: "http://localhost:8080/auth/google/redirect",
    },
    async (accessToken, refreshToken, profile, done) => {
      console.log("進入 Google Strategy 的區域");
      //   console.log(profile);
      console.log("===========================");
      let foundUser = await User.findOne({ googleID: profile.id }).exec();
      if (foundUser) {
        console.log("使用者已經註冊過了, 無須再存入 Database");
        done(null, foundUser);
      } else {
        console.log("偵測到新用戶，需要存到 Database");
        let newUser = new User({
          name: profile.displayName,
          googleID: profile.id,
          thumbnail: profile.photos[0].value,
          email: profile.emails[0].value,
        });
        let saveUser = await newUser.save();
        console.log("成功創建新用戶");
        done(null, saveUser);
      }
    }
  )
);
