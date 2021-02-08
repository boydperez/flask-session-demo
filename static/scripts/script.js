$(document).ready(function() {
    $("#greetings").text(greet);
}); 

let date = new Date();
let hour = date.getHours();
let greet;

if (hour < 12) {
    greet = "Morning";
} else if (hour < 18) {
    greet = "Afternoon";
} else {
    greet = "Evening";
}