let max = 1000000;

function isPrime(n) {
  for (let i = 2; i <= Math.sqrt(n); i++) {
    if (n % i == 0) {
      return false;
    }
  }
  return n > 1;
}

const random = (max) => Math.floor(Math.random() * max);

function generatePrimes(quota) {
  const primes = [];
  while (primes.length < quota) {
    const candidate = random(max);
    if (isPrime(candidate)) {
      primes.push(candidate);
    }
  }
  return primes;
}

const output = document.querySelector("div#output");
const button = document.querySelector("#generate");
button.addEventListener("click", (e) => {
  const quota = document.querySelector("#number");
  const primes = generatePrimes(quota.value);
  output.innerHTML = primes;
});
