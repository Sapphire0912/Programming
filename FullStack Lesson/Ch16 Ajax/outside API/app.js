async function hello() {
  try {
    let resource = await fetch(
      "https://v2.jokeapi.dev/joke/Programming?type=single"
    );
    let data = await resource.json();
    output.innerHTML += data.joke + "<br>";
  } catch (e) {
    console.log(e);
  }
}

const btn = document.querySelector("#new-joke");
const output = document.querySelector("#output");
btn.addEventListener("click", (e) => {
  hello();
});
