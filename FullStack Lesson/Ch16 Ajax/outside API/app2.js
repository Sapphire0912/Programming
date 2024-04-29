let myKey = "c128cf079681fd51870532e7610c426d";
let city_name = "Taichung";
let URL = `https://api.openweathermap.org/data/2.5/weather?q=${city_name}&appid=${myKey}`;

async function weather() {
  try {
    let resource = await fetch(URL);
    let data = await resource.json();
    console.log(data);
  } catch (e) {
    console.log(e);
  }
}

weather();
