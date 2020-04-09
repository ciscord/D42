/**
 * website
 * (c) Device42 <dave.amato@device42.com>
 */
var jQuery = window.jQuery = window.$ = require('jquery');
/* vendor scripts */
require('./libs/polyfills');
require('./libs/bootstrap');
require('./libs/owl.carousel');
require('./libs/waypoints');
require('./libs/featherlight');
require('./libs/jquery.validate.min');
require('./libs/jquery.validate.extras.min');
require('./libs/matchHeight');
require('./libs/prettify');

/* d42 scripts */
var D42 = window.D42 = require('./libD42');

$(function () {
    var csrftoken = D42.getCookie('csrftoken');
    D42.initListeners();
    D42.initAnimations();
    D42.setActiveSection();

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!D42.csrfSafeMethod(settings.type) && D42.sameOrigin(settings.url)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    $.fn.extend({
        animateCss: function (animationName) {
            var animationEnd = 'webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend';
            $(this).addClass('animated ' + animationName).one(animationEnd, function () {
                $(this).removeClass('animated ' + animationName);
            });
        }
    });

    if (!("ontouchstart" in document.documentElement)) {
        document.documentElement.className += " no-touch";
    }
    // initialize nav dropdown listener
    $('.dropdown').hover(function() {
        var $this = $(this);
        var $toggle = $this.find(".dropdown-toggle");
        var notMobileMenu = $('.navbar-toggle').size() > 0 && $('.navbar-toggle').css('display') === 'none';
        if (notMobileMenu) {
            $toggle.trigger("click");
        }
    });
    // fix that disables submenu hide on click
    $('.dropdown').click(function(e){
        var notMobileMenu = $('.navbar-toggle').size() > 0 && $('.navbar-toggle').css('display') === 'none';
        if((e.originalEvent !== undefined) && (notMobileMenu)) {
            e.stopPropagation();
        }
    });
    $(".row.match-height").matchHeight();
    $("[data-toggle='tooltip']").tooltip();
});

