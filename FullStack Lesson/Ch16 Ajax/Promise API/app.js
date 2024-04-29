const name = document.querySelector("#name");
const delay = document.querySelector("#delay");
const btn = document.querySelector("#set-alarm");
const output = document.querySelector("#output");

// 原本的功能可以用此方式實現
// function alarm(person, delay) {
//   setTimeout(() => {
//     output.innerHTML = person + " 起床!!";
//   }, delay);
// }

// btn.addEventListener("click", (e) => {
//   alarm(name.value, delay.value);
// });

// 利用 Promise 來設計
// 在 alarm 內部，pending 在 delay 秒之後要變成 fulfilled
// 若 delay < 0 => 則變成 rejected

function alarm(person, delay) {
  return new Promise((resolve, reject) => {
    if (delay < 0) {
      reject("delay 不能小於 0");
    } else {
      setTimeout(() => {
        resolve(person + " 起床!!");
      }, delay);
    }
  });
}

btn.addEventListener("click", async (e) => {
  try {
    let result = await alarm(name.value, delay.value);
    output.innerHTML = result;
  } catch (e) {
    output.innerHTML = e;
  }
});
