function cardnumber(inputtxt)
{
  var cardno = /^(?:3(?:0[0-5]|[68][0-9])[0-9]{11})$/;
  if(inputtxt.value.match(cardno))
        {
      return true;
        }
      else
        {
        alert("Not a valid Dinners Club card number!");
        return false;
        }
}