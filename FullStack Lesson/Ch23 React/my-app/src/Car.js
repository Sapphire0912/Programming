import React from "react";
class Car extends React.Component {
  constructor(props) {
    super(props);
    this.state = { color: "blue" };
    this.colorChange = this.colorChange.bind(this);
  }

  colorChange() {
    this.setState({ color: "white" });
  }

  componentDidMount() {
    console.log("Car is rending...");
  }

  componentDidUpdate() {
    console.log("Car color is updated.");
  }

  render() {
    return (
      <div>
        <h2>
          This is a {this.state.color} car, another is {this.props.anotherColor}
        </h2>
        <button onClick={this.colorChange}>改變第一台車的顏色</button>
      </div>
    );
  }
}

export default Car;
