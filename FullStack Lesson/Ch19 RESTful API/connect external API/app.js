async function getData() {
  let response = await fetch("http://localhost:3000/students");
  let data = await response.json();
  console.log(data);
}

// 已封鎖跨來源請求: 同源政策不允許讀取 http://localhost:3000/students 的遠端資源。（原因: CORS 請求未成功）。狀態代碼: (null)。
getData();
