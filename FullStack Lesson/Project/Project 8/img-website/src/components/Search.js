import axios from "axios";
import React from "react";

const Search = () => {
  const auth = "owsD18CliK4S55XzH8dzGGWILlLjHORPoQuldwigWE4j4e94JnCmzEiz";
  const initialURL = "https://api.pexels.com/v1/curated?page=1&per_page=15";
  const search = async () => {
    let result = await axios.get(initialURL, {
      headers: { Authorization: auth },
    });
    console.log(result);
  };
  return (
    <div className="search">
      <input className="input" type="text" />
      <button onClick={search}>Search</button>
    </div>
  );
};

export default Search;
