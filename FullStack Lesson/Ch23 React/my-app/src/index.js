import React from "react"; // 相當於 const React = require('react');
import ReactDOM from "react-dom/client";
import App from "./App";
import "./styles/style.css";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
