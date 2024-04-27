const URL =
  "https://mdn.github.io/learning-area/javascript/apis/fetching-data/can-store/products.json";

const WrongURL = "https://learnin/products.json";
let fetchPromise = fetch(WrongURL);

// console.log(fetchPromise);
// fetchPromise.then((response) => {
//   //   console.log(fetchPromise);
//   //   console.log(response);

//   // .json() method is also asynchronous function, 也是一個 Promise Object.
//   response.json().then((data) => {
//     console.log(data);
//   });
// });

fetchPromise
  .then((response) => {
    return response.json();
  })
  .then((data) => {
    console.log(data);
  })
  .catch((e) => {
    console.log(fetchPromise);
    console.log(e);
  });
