import React from "react";

const Nav = () => {
  return (
    <nav style={{ backgroundColor: "lightblue" }}>
      <ul>
        <li>
          <a style={{ color: "red" }} href="#">
            首頁
          </a>
        </li>
        <li>
          <a style={{ color: "red" }} href="#">
            另一個頁面
          </a>
        </li>
      </ul>
    </nav>
  );
};

export default Nav;
