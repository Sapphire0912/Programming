// // console.log("this is app1.js file");

// (function (exports, require, module, __filename, __dirname) {
//   console.log("this is app1.js file");
// })(); // IIFE 的寫法

// require("./app2");

// let name = 30;
// console.log(name);

// console.log(__filename);
// console.log(__dirname);

// console.log(module);

// let app2 = require("./app2");
// let app3 = require("./app3");
// app2.morning();
// app3.evening();

function lunch() {
  console.log("lunch");
}

exports.lunch = lunch;
