// FizzBuzz implementation in JavaScript
// Prints numbers 1-100, but for multiples of 3 prints "Fizz",
// for multiples of 5 prints "Buzz", and for multiples of both prints "FizzBuzz"

function fizzBuzz() {
    for (let i = 1; i <= 100; i++) {
        if (i % 15 === 0) {
            console.log("FizzBuzz");
        } else if (i % 3 === 0) {
            console.log("Fizz");
        } else if (i % 5 === 0) {
            console.log("Buzz");
        } else {
            console.log(i);
        }
    }
}

// Run the function
fizzBuzz();
