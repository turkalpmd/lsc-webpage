(function ($) {
  "use strict";

  $(document).on('click', '.main-nav .drop-down > a', function(e) {
    e.preventDefault();
    var liClass = $(this).parent('li').attr("class");
    $('.drop-down').removeClass('active');
    if(liClass!='drop-down active'){
      $(".drop-down > ul").slideUp();
      //alert('burada');
    }
    $(this).parent().toggleClass('active');
    $(this).next().slideToggle(300);
    if(liClass=='drop-down active'){
      $(this).parent().removeClass('active');
    }


  });

  // Mobile Navigation
  if ($('.main-nav').length) {
    var $mobile_nav = $('.main-nav').clone().prop({
      class: 'mobile-nav d-lg-none'
    });
    $('body').append($mobile_nav);
    $('body').prepend('<button type="button" class="mobile-nav-toggle d-lg-none"><i class="fas fa-bars"></i></button>');
    $('body').append('<div class="mobile-nav-overly"></div>');

    $(document).on('click', '.mobile-nav-toggle', function(e) {
      $('body').toggleClass('mobile-nav-active');
      $('.mobile-nav-toggle i').toggleClass('fa-times fa-bars');
      $('.mobile-nav-overly').toggle();
    });

    $(document).on('click', '.mobile-nav .drop-down > a', function(e) {
      e.preventDefault();
      var liClass = $(this).parent('li').attr("class");
      $('.drop-down').removeClass('active');
      if(liClass!='drop-down active'){
        $(".drop-down > ul").slideUp();
        //alert('burada');
      }
      $(this).parent().toggleClass('active');
      $(this).next().slideToggle(300);
      if(liClass=='drop-down active'){
        $(this).parent().removeClass('active');
      }
    });

    $(document).click(function(e) {
      var container = $(".mobile-nav, .mobile-nav-toggle");
      if (!container.is(e.target) && container.has(e.target).length === 0) {
        if ($('body').hasClass('mobile-nav-active')) {
          $('body').removeClass('mobile-nav-active');
          $('.mobile-nav-toggle i').toggleClass('fa-times fa-bars');
          $('.mobile-nav-overly').fadeOut();
        }
      }
    });
  } else if ($(".mobile-nav, .mobile-nav-toggle").length) {
    $(".mobile-nav, .mobile-nav-toggle").hide();
  }

})(jQuery);
