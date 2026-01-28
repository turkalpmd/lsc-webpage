//document.getElementById("count").innerText = 5

//variable to store visitors
//initialize the counter to cero
let count = 0
//asking for the HTML element and store into a variable
let countEl = document.getElementById("count-el")
 //verify that we are actually gettinh the HTML element
 console.log(countEl)

//increment the count variable when the button INCREMENT is clicked
function increment (){
    console.log ("increment clicked")
    count = count + 1
    //reflect the change in the UI (HTML-H2-Tag called count-el)
    countEl.innerText = count
   
    //check the output to check the value of count
    console.log(count) 
}