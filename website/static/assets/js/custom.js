/*
 
------------------------------------------------------------------

-------------------------------------------------------------------*/
(function ($) {
  "use strict";
  var HandMade = {
    initialised: false,
    version: 1.0,
    mobile: false,
    init: function () {
      if (!this.initialised) {
        this.initialised = true;
      } else {
        return;
      }

      /*-------------- Hand Made Functions Calling ---------------------------------------------------
            ------------------------------------------------------------------------------------------------*/
      this.RTL();
      this.Slider();
      this.Scroll_to_bottom();
      this.Menu_toggle();
      this.Search();
      this.Login_form();
      this.Signup_form();
      this.Testimonial();
      this.Related_pro();
      this.Related_pro_item();
      this.Gallery();
      this.Sorting();
      this.Wow();
      this.Spiner();
      this.Range_slider();
      this.MailFunction();
    },

    /*-------------- Hand Made Functions definition ---------------------------------------------------
        ---------------------------------------------------------------------------------------------------*/
    RTL: function () {
      // On Right-to-left(RTL) add class
      var rtl_attr = $("html").attr("dir");
      if (rtl_attr) {
        $("html").find("body").addClass("rtl");
      }
    },
    //Main slider
    Slider: function () {
      if ($(".rev_slider_wrapper").length) {
        var tpj = jQuery;

        var revapi1068;
        tpj(document).ready(function () {
          if (tpj("#rev_slider_1068_1").revolution == undefined) {
            revslider_showDoubleJqueryError("#rev_slider_1068_1");
          } else {
            revapi1068 = tpj("#rev_slider_1068_1")
              .show()
              .revolution({
                sliderType: "standard",
                jsFileLocation: "plugin/revolution/js",
                sliderLayout: "fullwidth",
                dottedOverlay: "none",
                delay: 9000,
                navigation: {
                  keyboardNavigation: "off",
                  keyboard_direction: "horizontal",
                  mouseScrollNavigation: "off",
                  mouseScrollReverse: "default",
                  onHoverStop: "off",
                  touch: {
                    touchenabled: "on",
                    swipe_threshold: 75,
                    swipe_min_touches: 1,
                    swipe_direction: "vertical",
                    drag_block_vertical: false,
                  },
                  bullets: {
                    enable: true,
                    hide_onmobile: true,
                    hide_under: 1024,
                    style: "uranus",
                    hide_onleave: false,
                    direction: "vertical",
                    h_align: "right",
                    v_align: "center",
                    h_offset: 30,
                    v_offset: 0,
                    space: 5,
                    tmp: '<span class="tp-bullet-inner"></span>',
                  },
                },
                viewPort: {
                  enable: true,
                  outof: "wait",
                  visible_area: "80%",
                  presize: false,
                },
                responsiveLevels: [1240, 1024, 778, 480],
                visibilityLevels: [1240, 1024, 778, 480],
                gridwidth: [1240, 1024, 778, 480],
                gridheight: [868, 768, 960, 720],
                lazyType: "single",
                shadow: 0,
                spinner: "off",
                stopLoop: "off",
                stopAfterLoops: -1,
                stopAtSlide: -1,
                shuffle: "off",
                autoHeight: "off",
                autoPlay: "true",
                fullScreenAutoWidth: "off",
                fullScreenAlignForce: "off",
                fullScreenOffsetContainer: ".header",
                fullScreenOffset: "",
                disableProgressBar: "on",
                hideThumbsOnMobile: "off",
                hideSliderAtLimit: 0,
                hideCaptionAtLimit: 0,
                hideAllCaptionAtLilmit: 0,
                debugMode: false,
                fallbacks: {
                  simplifyAll: "off",
                  nextSlideOnWindowFocus: "off",
                  disableFocusListener: false,
                },
              });
          }
        }); /*ready*/
      }

      //Slider for full screen layout
      if ($(".hm_home_style3 .rev_slider_wrapper").length) {
        var tpj = jQuery;

        var revapi1068;
        tpj(document).ready(function () {
          if (tpj("#rev_slider_1068_2").revolution == undefined) {
            revslider_showDoubleJqueryError("#rev_slider_1068_2");
          } else {
            revapi1068 = tpj("#rev_slider_1068_2")
              .show()
              .revolution({
                sliderType: "standard",
                jsFileLocation: "plugin/revolution/js",
                sliderLayout: "fullscreen",
                dottedOverlay: "none",
                delay: 9000,
                navigation: {
                  keyboardNavigation: "off",
                  keyboard_direction: "horizontal",
                  mouseScrollNavigation: "off",
                  mouseScrollReverse: "default",
                  onHoverStop: "off",
                  touch: {
                    touchenabled: "on",
                    swipe_threshold: 75,
                    swipe_min_touches: 1,
                    swipe_direction: "vertical",
                    drag_block_vertical: false,
                  },
                  bullets: {
                    enable: true,
                    hide_onmobile: true,
                    hide_under: 1024,
                    style: "uranus",
                    hide_onleave: false,
                    direction: "vertical",
                    h_align: "right",
                    v_align: "center",
                    h_offset: 30,
                    v_offset: 0,
                    space: 5,
                    tmp: '<span class="tp-bullet-inner"></span>',
                  },
                },
                viewPort: {
                  enable: true,
                  outof: "wait",
                  visible_area: "80%",
                  presize: false,
                },
                responsiveLevels: [1240, 1024, 778, 480],
                visibilityLevels: [1240, 1024, 778, 480],
                gridwidth: [1240, 1024, 778, 480],
                gridheight: [868, 768, 960, 720],
                lazyType: "single",
                shadow: 0,
                spinner: "off",
                stopLoop: "off",
                stopAfterLoops: -1,
                stopAtSlide: -1,
                shuffle: "off",
                autoHeight: "off",
                autoPlay: "true",
                fullScreenAutoWidth: "off",
                fullScreenAlignForce: "off",
                fullScreenOffsetContainer: ".header",
                fullScreenOffset: "",
                disableProgressBar: "on",
                hideThumbsOnMobile: "off",
                hideSliderAtLimit: 0,
                hideCaptionAtLimit: 0,
                hideAllCaptionAtLilmit: 0,
                debugMode: false,
                fallbacks: {
                  simplifyAll: "off",
                  nextSlideOnWindowFocus: "off",
                  disableFocusListener: false,
                },
              });
          }
        }); /*ready*/
      }
    },
    //Scroll
    Scroll_to_bottom: function () {
      $(".int_scroll").on("click", function () {
        var height = $(window).height();
        $("html,body").animate(
          {
            scrollTop: $(this).offset().top,
          },
          height
        );
      });
    },

    //Menu toggle
    Menu_toggle: function () {
      $(".menu_btn").on("click", function () {
        $(".hm_menu").toggleClass("open_menu");
      });

      $(".hm_menu ul li.dropdown")
        .children("a")
        .append(function () {
          return '<div class="dropdown-expander"><i class="fa fa-bars"></i></div>';
        });
      $(".hm_menu > ul > li.dropdown a >.dropdown-expander").on(
        "click",
        function () {
          $(this).parent().parent().children(".sub-menu").slideToggle();
          return false;
        }
      );

      //Menu style2

      $(".hm_menu_bar > i").on("click", function () {
        $(".hm_menu_wrapper.menu_hide").addClass("hidden_menu_open");
      });

      $(".hm_hidden-bar-close i").on("click", function () {
        $(".hm_menu_wrapper.menu_hide").removeClass("hidden_menu_open");
      });

      $(".home_style2 .hm_menu ul li.dropdown")
        .children("a")
        .append(function () {
          return '<div class="dropdown-expander2"><i class="fa fa-bars"></i></div>';
        });
      $(".home_style2 .hm_menu > ul > li.dropdown a >.dropdown-expander2").on(
        "click",
        function () {
          $(this).parent().parent().children(".sub-menu").slideToggle();
          return false;
        }
      );
    },

    //Search

    Search: function () {
      // Search box
      $(".hm_home_style1 .hm_header_search > i").on("click", function () {
        $(this).parent().toggleClass("search_open");
      });
      $(".icon_close i").on("click", function () {
        $(".hm_home_style1 .hm_header_search").removeClass("search_open");
      });
    },

    //onclick login form

    Login_form: function () {
      $(".popup-with-form").on("click", function () {
        $(".hm_login_form_overlay").addClass("login_open");
        $("body").addClass("login_overflow");
      });
      $(".login_close").on("click", function () {
        $(".hm_login_form_overlay").removeClass("login_open");
        $("body").removeClass("login_overflow");
      });

      $(".hm_login_form_overlay").on("click", function () {
        $(".hm_login_form_overlay").removeClass("login_open");
        $("body").removeClass("login_overflow");
      });
      $(".hm_login_form").on("click", function () {
        return false;
      });
    },

    //Onclick signup form

    Signup_form: function () {
      $(".popup-signup-form").on("click", function () {
        $(".hm_signup_form_overlay").addClass("login_open");
        $("body").addClass("login_overflow");
      });
      $(".login_close").on("click", function () {
        $(".hm_signup_form_overlay").removeClass("login_open");
        $("body").removeClass("login_overflow");
      });

      $(".hm_signup_form_overlay").on("click", function () {
        $(".hm_signup_form_overlay").removeClass("login_open");
        $("body").removeClass("login_overflow");
      });
      $(".hm_signup_form ").on("click", function () {
        return false;
      });
    },

    //Testimonial slider

    Testimonial: function () {
      $(".related_pro_slider").owlCarousel({
        loop: true,
        margin: 20,
        items: 3,
        nav: false,
        autoplay: true,
        responsive: {
          0: {
            items: 1,
          },
          600: {
            items: 2,
          },
          1000: {
            items: 3,
          },
        },
      });
    },
    //Related Product Slider

    Related_pro: function () {
      $(".test_slider").owlCarousel({
        loop: true,
        margin: 10,
        dots: false,
        items: 5,
        nav: false,
        autoplay: true,
        responsive: {
          0: {
            items: 1,
          },
          600: {
            items: 3,
          },
          1000: {
            items: 5,
          },
        },
      });
    },


    Related_pro_item: function () {
      $(".test_slider_pro").owlCarousel({
        loop: true,
        margin: 4,
        items: 3,
        nav: false,
        autoplay: true,
        responsive: {
          0: {
            items: 1,
          },
          600: {
            items: 2,
          },
          1000: {
            items: 3,
          },
        },
      });
    },

    // ....................poroduct..........
    //      Related_pro: function () {
    //     $(".testimonial-slider").owlCarousel({
    //         loop: true,
    //         items: 3,
    //         margin:20,
    //         pagination: false,
    //         navigation: false,
    //         autoplay: true,
    //         lazyLoad:true,
    //         autoplayTimeout:3000,
    //         responsiveClass:true,
    //         responsive:{
    //             0:{
    //                 items:1
    //             },
    //             600:{
    //                 items:2
    //             },
    //             1000:{
    //                 items:3,
    //             }
    //         }
    //     });
    // })
    //Gallery
    Gallery: function () {
      if ($(".hm_gallery_inner").length > 0) {
        $(".popup-gallery").magnificPopup({
          type: "image",
          removalDelay: 500,
          mainClass: "mfp-with-zoom",
          gallery: {
            enabled: true,
          },
        });
      }
      //Magnific for iframe
      if ($(".hm_news_wrapper").length > 0) {
        $(".popup-iframe").magnificPopup({
          type: "iframe",
        });
      }
      //Magnific for Blog
      if ($(".hm_news_wrapper").length > 0) {
        $(".popup-news-gallery").magnificPopup({
          type: "image",
          removalDelay: 500,
          mainClass: "mfp-with-zoom",
          gallery: {
            enabled: true,
          },
        });
      }
      //Magnific for instagram gallery
      if ($(".insta_gallery").length > 0) {
        $(".popup-gallery").magnificPopup({
          type: "image",
          removalDelay: 500,
          mainClass: "mfp-with-zoom",
          gallery: {
            enabled: true,
          },
        });
      }
    },
    // Portfolio Sorting
    Sorting: function () {
      if ($(".filter_list ul li a").length > 0) {
        $(".filter_list ul li a").on("click", function (e) {
          e.preventDefault();
        });
        $("#portfolio").mixItUp();
      }
    },
    //Wow
    Wow: function () {
      new WOW().init();
    },

    //Spiner

    Spiner: function () {
      if ($(".quantity-spinner").length) {
        $(".quantity-spinner .plus").on("click", function () {
          var val = $(this).prev(".prod_qty").val();
          $(this)
            .prev(".prod_qty")
            .val(val * 1 + 1);
        });
        $(".quantity-spinner .minus").on("click", function () {
          var val = $(this).next(".prod_qty").val();
          if (val != 1) {
            $(this)
              .next(".prod_qty")
              .val(val * 1 - 1);
          }
        });
      }
    },
    //Range slider

    Range_slider: function () {
      if ($("#slider_range").length) {
        $("#slider_range").slider({
          range: true,
          min: 0,
          max: 500,
          values: [75, 300],
          slide: function (event, ui) {
            $("#amount").val("$" + ui.values[0] + " - $" + ui.values[1]);
          },
        });
        $("#amount").val(
          "$" +
            $("#slider_range").slider("values", 0) +
            " - $" +
            $("#slider_range").slider("values", 1)
        );
      }
    },

    //Contact mail
    MailFunction: function () {
      $(".submit_frm").on("click", function () {
        var u_name = $("#name").val();
        var u_email = $("#email").val();
        var u_phone = $("#number").val();
        var u_date = $("#subject").val();
        var u_msg = $("#message").val();

        $.ajax({
          type: "POST",
          url: "contactmail.php",
          data: {
            username: u_name,
            useremail: u_email,
            userphone: u_phone,
            usersubject: u_subject,
            user_msg: u_msg,
          },
          success: function (msg) {
            var full_msg = msg.split("#");
            if (full_msg[0] == "1") {
              $("#name").val("");
              $("#email").val("");
              $("#number").val("");
              $("#subject").val("");
              $("#message").val("");
              $("#err_msg").html(full_msg[1]);
            } else {
              $("#name").val(u_name);
              $("#email").val(u_email);
              $("#number").val(u_phone);
              $("#subject").val(u_phone);
              $("#message").val(u_msg);
              $("#err_msg").html(full_msg[1]);
            }
          },
        });
      });
    },
  };

  HandMade.init();
  //On scroll fixed menu
  $(window).scroll(function () {
    var wh = window.innerWidth;
    if (wh > 767) {
      var h = window.innerHeight;
      var window_top = $(window).scrollTop() + 1;
      if (window_top > 100) {
        $(".hm_menu_wrapper").addClass("hm_fixed");
        $(".home_style2 .hm_menu_wrapper").removeClass("hm_fixed");
      } else {
        $(".hm_menu_wrapper").removeClass("hm_fixed");
      }
    }
  });
  // Load Event

  $(window).on("load", function () {
    jQuery(".loader").fadeOut();
    jQuery(".loader").delay(600).fadeOut("slow");
  });
})(jQuery);

// .................................................ajhs
