// let myHeading = document.getElementById("myHeading1");
// // console.log(myHeading);

// let myParagraphs = document.getElementsByClassName("my-P");
// // console.log(myParagraphs);

// let first_found = document.querySelector("a.my-P");
// // console.log(first_found);

// let selectorAll = document.querySelectorAll(".my-P"); // return 長度為 3 的 node list
// console.log(selectorAll);

// HTMLCollection 動態(dynamic)
// NodeList 靜態 static
// HTMLCollection 和 NodeList 的差別
// let hellos = document.getElementsByClassName("hello");
// let helloss = document.querySelectorAll(".hello");

// // 模擬使用者改變網頁內容
// let body = document.querySelector("body");
// let p = document.createElement("p");
// p.innerText = "this is a new p";
// p.classList.add("hello");
// body.appendChild(p);

// console.log(hellos, hellos.length);
// helloss = document.querySelectorAll(".hello"); // 通常都會再重新執行一次 querySelectorAll 去更新資料
// console.log(helloss, helloss.length); // static 不會隨著網頁改變而改變資料

// 展示 childnode attribute
let body = document.querySelector("body"); // return element object
console.log(body);
console.log(body.childNodes);
console.log(body.children);
