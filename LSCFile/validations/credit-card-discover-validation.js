function cardnumber(inputtxt)
{
  var cardno = /^(?:6(?:011|5[0-9][0-9])[0-9]{12})$/;
  if(inputtxt.value.match(cardno))
        {
      return true;
        }
      else
        {
        alert("Not a valid Discover card number!");
        return false;
        }
}