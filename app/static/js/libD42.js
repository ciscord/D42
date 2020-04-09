var jQuery = window.$ = window.jQuery = require('jquery');
var D42 = function () {
};
D42.tools = {};
D42.setSiteSection = function(section) {
  if (!section) return;

  var _sitesection = String(section).toLowerCase();
  $(".dropdown-toggle").each(function() {
    var _sect = $(this).text().toLowerCase();
    if (_sect.indexOf(_sitesection) >= 0) {
      $(this).toggleClass("active");
    }
  });
};
D42.initListeners = function () {
  $('a[data-jump], button[data-jump]').on('click', function (e) {
    e.preventDefault();
    var target = this.getAttribute("data-jump");
    var offset = this.getAttribute("data-offset");
    var $target = $(target);

    if (offset && offset.toLowerCase() === "top-nav") {
      offset = ($("#nav").height() + $(".feature-menu-wrap").height());
    } else if (offset && isNaN(parseInt(offset))) {
      offset = offset;
    } else {
      offset = "51";
    }

    if (!$target || $target.length < 1) return false;

    $('html, body').stop().animate({
      'scrollTop': $target.offset().top - offset
    }, 900, 'swing', function () {
      window.location.hash = target;
    });
  });
};
D42.initAnimations = function () {
  var navHeight = function () {
    return document.querySelector('#nav').scrollHeight || '53';
  };
  $('img.animated').waypoint(function () {
    this.element.classList.toggle('fadeIn');
  }, {offset: '90%'});

  $('.go2top').waypoint(function () {
    this.element.classList.toggle('fadeIn');
  }, {offset: '75%'});

  $('.feature-menu-wrap').waypoint(function () {
    this.element.classList.toggle('stuck-feature-menu');
  }, {offset: navHeight()});
};
D42.initCarousel = function (carousel, options) {
  if ($(carousel).length > 0) {
    $(carousel).owlCarousel(options);
  }
};
D42.setActiveSection = function () {
  var path = window.location.pathname;

  $(".dropdown-toggle").each(function () {
    var $this = $(this);
    var section = "/" + $this.text().toLowerCase() + "/";

    if ((path.indexOf(section) >= 0) || path.indexOf(window.D42._sitesection) >= 0) {
      $(this).toggleClass('active');
    }
  });
};
D42.getCookie = function (name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = $.trim(cookies[i]);
      if (cookie.substring(0, name.length + 1) == (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
};
D42.csrfSafeMethod = function (method) {
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
};
D42.sameOrigin = function (url) {
  var host = document.location.host;
  var protocol = document.location.protocol;
  var sr_origin = '//' + host;
  var origin = protocol + sr_origin;
  return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
    (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') || !(/^(\/\/|http:|https:).*/.test(url));
};
D42.embedWistia = function (videoId) {
  if (videoId) {
    $.getScript('http://fast.wistia.net/static/E-v1.js', function () {
      D42._wistia.init(videoId);
    });
  }
};

D42._wistia = {
  'init': function (videoId) {
    wistiaEmbed = Wistia.embed(videoId, {
      stillUrl: "https://d42cdn.s3.amazonaws.com/img/branding/transparent-logo.png",
      playerColor: "#22a3df",
      fullscreenButton: true,
      videoFoam: true,
      container: "wistia_video"
    });
  },
  'initMetadata': function (videoId, callback) {
    var baseUrl = "http://fast.wistia.com/oembed/?url=";
    var accountUrl = encodeURIComponent('http://www.device42.com/videos/');

    $.getJSON(baseUrl + accountUrl + videoID + "?embedType=open_graph_tags&format=json&callback=?", callback);
  },
  'load': function (json) {
    $(".wistia_embed").prepend(json.html);
  }
};

D42.tools.loadJs = function (src, async, callback) {
  if (!src) callback && callback();
  else {
    var head = document.querySelector('head');
    var tag = document.createElement('script');
    if (async && async===true) {
      tag.setAttribute('async', 'true');
    }
    tag.setAttribute('type', 'text/javascript');
    tag.setAttribute('src', src);
    document.querySelector('body').appendChild(tag);

    tag.onreadystatechange = function () {
      if (tag.readyState == 'complete') {
        callback && callback();
      }
    };
  }
};

D42.tracking = {
  init: function () {
    $t = $('[data-event="ev"]');
    $t.click(function () {
      var evCat = $(this).data('category') ? $(this).data('category') : '',
        evAct = $(this).data('action') ? $(this).data('action') : '',
        evLab = $(this).data('label') ? $(this).data('label') : '',
        evVal = $(this).data('value') ? $(this).data('value') : '';
      try {
        _gaq.push(['_trackEvent', evCat, evAct, evLab, evVal]);
        ga('send', 'event', evCat, evAct, evLab, evVal);
      } catch (e) {
        console.log(e);
      }
    });
  }
}
D42.d42DownloadForm = function (formId) {
  if (!formId) return false;
  var $this = $(formId);
  var canClick = true;
  var $button = $this.find('.d42_download_form_submit');

  $button.click(function (event) {
    if (canClick) {
      event.preventDefault();
      var name = $this.find('.d42_download_form_name').val();
      var email = $this.find('.d42_download_form_mail').val();
      var check = $this.find('.d42_download_form_check').val();
      var csrftoken = $("input[name=csrfmiddlewaretoken]").val();
      var page_title = document.title;
      var type = $(this).attr('type');
      canClick = false;

      $button.fadeTo("fast", 0.5);

      var data = {
        'name': name,
        'email': email,
        'main': check,
        'title': page_title,
        'type': type,
        'csrftoken': csrftoken
      };

      $.ajax({
        url: url_prepend_lang + '/ajax_download/',
        type: 'POST',
        data: data,
        success: function (res) {
          if (type == 'download') {
            window.location = url_prepend_lang + '/thanks/1/';
          } else {
            window.location = url_prepend_lang + '/thanks/0/';
          }
        },
        error: function (res) {
          res = JSON.parse(res.responseText);
          var error_msg = null;

          if (res.msg.email_error) {
            error_msg = gettext('Please check that you have used your work email address. If you are unable to do so, please send us a note to support@device42.com ');
          } else if (res.msg.name_error) {
            error_msg = gettext('Please enter your name');
          }

          if (error_msg) {
            $this.find('.d42_download_form_error').text(error_msg).slideDown();
          }

          canClick = true;
          $button.fadeTo("fast", 1);
        }
      });
    }
  });
}

D42.accordion = function(accordionId) {
  if (!accordionId) return false;
  $(".accordion").find(".accordion-title a").click(function() {
    var $this=$(this);

  });
}

module.exports = D42;
