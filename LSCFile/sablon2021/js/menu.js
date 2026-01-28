$(document).ready(function()
{

	$(".menu_sol div.menu_title").click(function()
    {
		var css_adi=$(this).attr("class");
		//alert(css_adi);
		if( css_adi.indexOf( 'menu_closed' ) != -1 ) {
			//alert('kapali'); 
			$(this).removeClass('menu_closed');
			$(this).addClass('menu_opened');
			} else  { 
			//alert('acik');
			$(this).removeClass('menu_opened');
			$(this).addClass('menu_closed');
			}
    
		$(this).next("div.sub_menu").slideToggle(300).siblings("div.sub_menu").slideUp("slow");
       	$(this).siblings().removeClass('menu_opened').addClass('menu_closed');
	});
	
	$("div.sub_menu_title").click(function()
    {		 
		
		$(this).next("div.sub_menu2").slideToggle(300).siblings("div.sub_menu2").slideUp("slow");
       	//$(this).siblings().removeClass('menu_acik').addClass('menu_kapali');
	});
	
	
});