//logo
$(window).scroll(function() {
  var position = $( ".site_baslangic" ).position();
  var s_top = position.top;

  if ($(this).scrollTop() > s_top) {
    // $('.logo').fadeOut('slow');
    // $('.logo_mobile').fadeIn('slow');
    $('.ust').addClass('ust-scrolled');
    $('.menu_ust').addClass('menu_ust-scrolled');
    $('.logo').addClass('logo-scrolled');
    $('.menu').addClass('menu-scrolled');
    $('.logo_link').addClass('logo_link-scrolled');
    //$('.resimler').hide();

  } else {
    // $('.logo_mobile').fadeOut('slow');
    // $('.logo').fadeIn('slow');
    $('.ust').removeClass('ust-scrolled');
    $('.menu_ust').removeClass('menu_ust-scrolled');
    $('.logo').removeClass('logo-scrolled');
    $('.menu').removeClass('menu-scrolled');
    $('.logo_link').removeClass('logo_link-scrolled');
    //$('.resimler').show();
  }
});

// Back to top button
$(window).scroll(function() {
  if ($(this).scrollTop() > 100) {
    $('.back-to-top').fadeIn('slow');
  } else {
    $('.back-to-top').fadeOut('slow');
  }
});
$( document ).ready(function() {
  $('.back-to-top').click(function(){
    //alert('dfsdf');
    $('html, body').animate({scrollTop : 0},1500, 'easeInOutExpo');
    return false;
  });


});