let balance = 0; // shared resource
let mutex = Promise.resolve(); // return a fulfilled promise

// 使用 mutex 方法可以處理, Race Condition.

const randomDelay = () => {
  return new Promise((resolve) => setTimeout(resolve, Math.random() * 100));
};

async function loadBalance() {
  await randomDelay(); // 等待隨機 0s ~ 0.1s
  return balance;
}

async function saveBalance(value) {
  await randomDelay();
  balance = value;
}

async function sell1() {
  mutex = mutex.then(async () => {
    const balance = await loadBalance();
    console.log(`sell1 before:${balance}`);
    const newBalance = balance + 50;
    await saveBalance(newBalance);
    console.log(`sell1 after:${newBalance}`);
  });
  return mutex;
}

async function sell2() {
  mutex = mutex.then(async () => {
    const balance = await loadBalance();
    console.log(`sell2 before:${balance}`);
    const newBalance = balance + 70;
    await saveBalance(newBalance);
    console.log(`sell2 after:${newBalance}`);
  });
  return mutex;
}

async function main() {
  //   await Promise.all([sell1(), sell2()]);
  //   const balance = await loadBalance();
  //   console.log(`after sell1 and sell2: ${balance}`);
  sell1();
  sell2();
  sell1();
  sell2();
  sell2();
  sell1();
  sell2();
  sell1();

  console.log("do anything...");
}
main();
