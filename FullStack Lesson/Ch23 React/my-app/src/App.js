import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Car from "./Car";
import Layout from "./Layout";
import HomePage from "./HomePage";
import About from "./About";
import Page404 from "./Page404";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<HomePage />}></Route>
          <Route path="about" element={<About />}></Route>
          <Route path="car" element={<Car />}></Route>
          <Route path="*" element={<Page404 />}></Route>
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
