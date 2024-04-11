const http = require("http");
const fs = require("fs");

// 創建網頁伺服器(給一個 callback function with 2 parameters.)
const server = http.createServer((req, res) => {
  /* 
    request: HTTP Request object
    response: HTTP Response object
  */
  //   console.log(req.headers);
  //   console.log(res);
  res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
  if (req.url == "/") {
    res.write("歡迎來到我的網頁<br>");
    res.write("Welcome to my web.<br>");
    res.end();
  } else if (req.url == "/anotherPage") {
    res.write("這是另一個頁面<br>");
    res.end();
  } else if (req.url == "/myFile") {
    // 讓 client 可以看見 *.html 的網頁
    fs.readFile("myFile.html", (error, data) => {
      if (error) {
        res.write("存取 html 文件錯誤");
      } else {
        res.write(data);
        res.end();
      }
    });
  } else {
    res.write("不存在的頁面<br>");
    res.end();
  }
  res.write(`req.url: ${req.url}`); // 顯示當前請求的 url
  //   res.end();
});

// server.listen(port_number, callback function)
server.listen(3000, () => {
  console.log("伺服器正在 port 3000 上運行");
});
