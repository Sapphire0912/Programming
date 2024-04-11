let app1 = require("./app1");
let app2 = require("./app2");
let app3 = require("./app3");

exports.morning = app2.morning;
exports.lunch = app1.lunch;
exports.evening = app3.evening;
