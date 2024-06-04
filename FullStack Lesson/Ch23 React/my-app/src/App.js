import Nav from "./Nav";
import Info from "./info";

function App() {
  const buttonHandler = (msg) => {
    alert(msg);
  };

  let gem = ["Sapphire", "Ruby"];
  let gem_info = [
    { gem_name: "Sapphire", price: "160K" },
    { gem_name: "Ruby", price: "200K" },
  ];

  return (
    <div>
      <h1>這是 App.js 的 h1 Tag.</h1>
      <Nav />
      {/* <Info name={gem[0]} price={"160K"} />
      <Info name={gem[1]} price={"200K"} /> */}
      {gem_info.map((obj) => {
        return <Info name={obj.gem_name} price={obj.price} />;
      })}

      <button
        onClick={() => {
          buttonHandler("今天天氣不錯");
        }}
      >
        Click me!
      </button>
    </div>
  );
}

export default App;
