import React, { useState } from "react";

const Info = () => {
  let [name, setName] = useState("Sapphire");
  let age = 24;
  const changeNameHandler = () => {
    setName("Sapphire Yuki.");
  };

  return (
    <div className="info">
      <h2>姓名：{name}</h2>
      <h2>年齡：{age}</h2>
      <button onClick={changeNameHandler}>改名按鈕</button>
    </div>
  );
};

export default Info;
