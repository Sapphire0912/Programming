// In Javascript, we have two ways to create the array.
// 1. let students = [];
// 2. let teacher = new Array();

let students = ["Eric", "Candy", "Iris", "Bob", "Brain", "Lily"];
// document.getElementById("output").innerHTML = students; // output: Eric,Aurora,Iris,Bob,Brain,Lily

students[1] = "Aurora";  // resign the index 1 of array value
// document.getElementById("output").innerHTML = students[1]; // output: Aurora

// we want to remove the last element in the array
// students.pop();

// we want to remove an element from the beginning of an array.
students.shift();
console.log(students);


console.log(students.length);  // show me how many members the array has.



let loopCounter = 0;
while (loopCounter < students.length){
    document.getElementById("output").innerHTML += students[loopCounter] + "<br/>";
    loopCounter++;
}

let grades = [75, 88, 91, 100, 67, 85];
let total = 0;
grades.push(90); // add an element to the end of 'grades' array
console.log(grades);

for (let x = 0; x < grades.length; x++){
    total = total + grades[x];
}
document.getElementById("output").innerHTML += "avg: " + Math.round(total / grades.length);