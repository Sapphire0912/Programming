function Add(){
    var x = parseInt(prompt("Number1: "));
    var y = parseInt(prompt("Number2: "));
    document.write(x + " + " + y + " = " + (x + y));
}

function Subtract(){
    var x = parseInt(prompt("Number1: "));
    var y = parseInt(prompt("Number2: "));
    document.write(x + " - " + y + " = " + (x - y));
}

function Multiply(){
    var x = parseInt(prompt("Number1: "));
    var y = parseInt(prompt("Number2: "));
    document.write(x + " * " + y + " = " + (x * y));
}

function Divide(){
    var x = parseInt(prompt("Number1: "));
    var y = parseInt(prompt("Number2: "));
    document.write(x + " / " + y + " = " + (x / y));
}

function mathProb(){
    var x = parseInt(prompt("Number1: "));
    var y = parseInt(prompt("Number2: "));
    var symbol = prompt("Math Symbol (+, -, *, /): ");

    switch(symbol){
        case '+':
            document.write(x + " + " + y + " = " + (x + y));
            break;
        
        case '-':
            document.write(x + " - " + y + " = " + (x - y));
            break;
        
        case '*':
            document.write(x + " * " + y + " = " + (x * y));
            break;
        
        case '/':
            document.write(x + " / " + y + " = " + (x / y));
    }
}
