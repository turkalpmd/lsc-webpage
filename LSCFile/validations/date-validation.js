var dminyear = 1900;
        var dmaxyear = 2200;
        var chsep= &quot;/&quot;
        function checkinteger(str1){
        var x;
        for (x = 0; x &lt; str1.length; x++){ 
        // verify current character is number or not !
        var cr = str1.charAt(x);
        if (((cr &lt; &quot;0&quot;) || (cr &gt; &quot;9&quot;))) 
        return false;
        }
        return true;
        }
        function getcharacters(s, chsep1){
        var x;
        var Stringreturn = &quot;&quot;;
        for (x = 0; x &lt; s.length; x++){ 
        var cr = s.charAt(x);
        if (chsep.indexOf(cr) == -1) 
        Stringreturn += cr;
        }
        return Stringreturn;
        }
        function februarycheck(cyear)
        {
        return (((cyear % 4 == 0) &amp;&amp; ( (!(cyear % 100 == 0)) || (cyear % 400 == 0))) ? 29 : 28 );
        }
        function finaldays(nr) {
        for (var x = 1; x &lt;= nr; x++) {
        this[x] = 31
        if (x==4 || x==6 || x==9 || x==11)
        {
        this[x] = 30}
        if (x==2)
        {
        this[x] = 29}
        } 
        return this
        } 
        function dtvalid(strdate)
        {
        var monthdays = finaldays(12)
        var cpos1=strdate.indexOf(chsep)
        var cpos2=strdate.indexOf(chsep,cpos1+1)
        var daystr=strdate.substring(0,cpos1)
        var monthstr=strdate.substring(cpos1+1,cpos2)
        var yearstr=strdate.substring(cpos2+1)
        strYr=yearstr
        if (strdate.charAt(0)==&quot;0&quot; &amp;&amp; strdate.length&gt;1) strdate=strdate.substring(1)
        if (monthstr.charAt(0)==&quot;0&quot; &amp;&amp; monthstr.length&gt;1) monthstr=monthstr.substring(1)
        for (var i = 1; i &lt;= 3; i++) {
        if (strYr.charAt(0)==&quot;0&quot; &amp;&amp; strYr.length&gt;1) strYr=strYr.substring(1)
        }
        // The parseInt is used to get a numeric value from a string
        pmonth=parseInt(monthstr)
        pday=parseInt(daystr)
        pyear=parseInt(strYr)
        if (cpos1==-1 || cpos2==-1){
        alert(&quot;The date format must be : dd/mm/yyyy&quot;)
        return false
        }
        if (monthstr.length&lt;1 || pmonth&lt;1 || pmonth&gt;12){
        alert(&quot;Input a valid month&quot;)
        return false
        }
        if (daystr.length&lt;1 || pday&lt;1 || pday&gt;31 || (pmonth==2 &amp;&amp; pday&gt;februarycheck(pyear))|| pday &gt; monthdays[pmonth])
		{
        alert(&quot;Input a valid day&quot;)
        return false
        }
        if (yearstr.length != 4 || pyear==0 || pyear&lt;dminyear || pyear&gt;dmaxyear)
		{
        alert(&quot;Input a valid 4 digit year between &quot;+dminyear+&quot; and &quot;+dmaxyear)
        return false
        }
        if (strdate.indexOf(chsep,cpos2+1)!=-1 || checkinteger(getcharacters(strdate, chsep))==false)
		{
        alert(&quot;Input a valid date&quot;)
        return false
        }
        return true
        }
        function validdate(inputtxt)
        {
        var crdt=inputtxt.value
        if (dtvalid(crdt)==false)
        {
        document.form1.text1.focus()
        return false
        }
        return true
        }