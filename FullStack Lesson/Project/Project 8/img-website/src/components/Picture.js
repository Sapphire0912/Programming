import React from "react";

const Picture = ({ data }) => {
  return (
    <div className="picture">
      <p>{data.phptographer}</p>
      <div className="imageContainer">
        <img src={data.src.large} alt="" />
      </div>
      <p>
        在此下載圖片：{" "}
        <a href={data.src.large} target="_blank">
          按一下
        </a>
      </p>
    </div>
  );
};

export default Picture;
