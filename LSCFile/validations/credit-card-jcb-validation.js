function cardnumber(inputtxt)
{
  var cardno = /^(?:(?:2131|1800|35\d{3})\d{11})$/;
  if(inputtxt.value.match(cardno))
        {
      return true;
        }
      else
        {
        alert("Not a valid JCB card number!");
        return false;
        }
}