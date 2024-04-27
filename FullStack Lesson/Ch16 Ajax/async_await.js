async function fetchProduct() {
  try {
    const URL =
      "https://mdn.github.io/learning-area/javascript/apis/fetching-data/can-store/products.json";

    const WrongURL = "https://sdfiodshffsdfjl.com";

    // 使用 await 就像是 block, 要等到此行執行結束, 才會執行後面的程式, 並且回傳的不是 Promise Obj. 而是 Response Obj.
    const response = await fetch(WrongURL);
    const data = await response.json();
    console.log(data);
  } catch (e) {
    console.log(e);
  }
}

fetchProduct();

// async function F() {
//   return 100;
// }
// let myPromise = F();
// myPromise.then((data) => console.log(data));
