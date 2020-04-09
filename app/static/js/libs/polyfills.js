/*! CSS rel=preload polyfill. Depends on loadCSS function. [c]2016 @scottjehl, Filament Group, Inc. Licensed MIT  */
(function (w) {
  if (!w.loadCSS) {
    return;
  }
  var rp = loadCSS.relpreload = {};
  rp.support = function () {
    try {
      return w.document.createElement("link").relList.supports("preload");
    } catch (e) {
      return false;
    }
  };
  rp.poly = function () {
    var links = w.document.getElementsByTagName("link");
    for (var i = 0; i < links.length; i++) {
      var link = links[i];
      if (link.rel === "preload" && link.getAttribute("as") === "style") {
        w.loadCSS(link.href, link);
        link.rel = null;
      }
    }
  };

  if (!rp.support()) {
    rp.poly();
    var run = w.setInterval(rp.poly, 300);
    if (w.addEventListener) {
      w.addEventListener("load", function () {
        w.clearInterval(run);
      });
    }
    if (w.attachEvent) {
      w.attachEvent("onload", function () {
        w.clearInterval(run);
      })
    }
  }
}(this));
/*! loadCSS: load a CSS file asynchronously. [c]2016 @scottjehl, Filament Group, Inc. Licensed MIT */
(function (w) {
  "use strict";
  var loadCSS = function (href, before, media) {
    var doc = w.document;
    var ss = doc.createElement("link");
    var ref;
    if (before) {
      ref = before;
    }
    else {
      var refs = ( doc.body || doc.getElementsByTagName("head")[0] ).childNodes;
      ref = refs[refs.length - 1];
    }

    var sheets = doc.styleSheets;
    ss.rel = "stylesheet";
    ss.href = href;
    ss.media = "only x";

    function ready(cb) {
      if (doc.body) {
        return cb();
      }
      setTimeout(function () {
        ready(cb);
      });
    }

    ready(function () {
      ref.parentNode.insertBefore(ss, ( before ? ref : ref.nextSibling ));
    });
    var onloadcssdefined = function (cb) {
      var resolvedHref = ss.href;
      var i = sheets.length;
      while (i--) {
        if (sheets[i].href === resolvedHref) {
          return cb();
        }
      }
      setTimeout(function () {
        onloadcssdefined(cb);
      });
    };

    function loadCB() {
      if (ss.addEventListener) {
        ss.removeEventListener("load", loadCB);
      }
      ss.media = media || "all";
    }

    if (ss.addEventListener) {
      ss.addEventListener("load", loadCB);
    }
    ss.onloadcssdefined = onloadcssdefined;
    onloadcssdefined(loadCB);
    return ss;
  };

  if (typeof exports !== "undefined") {
    exports.loadCSS = loadCSS;
  }
  else {
    w.loadCSS = loadCSS;
  }
}(typeof global !== "undefined" ? global : this));
/*! classList: adds DOMObject.classList */
(function () {

  if (typeof window.Element === "undefined" || "classList" in document.documentElement) return;

  var prototype = Array.prototype,
    push = prototype.push,
    splice = prototype.splice,
    join = prototype.join;

  function DOMTokenList(el) {
    this.el = el;
    // The className needs to be trimmed and split on whitespace
    // to retrieve a list of classes.
    var classes = el.className.replace(/^\s+|\s+$/g, '').split(/\s+/);
    for (var i = 0; i < classes.length; i++) {
      push.call(this, classes[i]);
    }
  };

  DOMTokenList.prototype = {
    add: function (token) {
      if (this.contains(token)) return;
      push.call(this, token);
      this.el.className = this.toString();
    },
    contains: function (token) {
      return this.el.className.indexOf(token) != -1;
    },
    item: function (index) {
      return this[index] || null;
    },
    remove: function (token) {
      if (!this.contains(token)) return;
      for (var i = 0; i < this.length; i++) {
        if (this[i] == token) break;
      }
      splice.call(this, i, 1);
      this.el.className = this.toString();
    },
    toString: function () {
      return join.call(this, ' ');
    },
    toggle: function (token) {
      if (!this.contains(token)) {
        this.add(token);
      } else {
        this.remove(token);
      }

      return this.contains(token);
    }
  };

  window.DOMTokenList = DOMTokenList;

  function defineElementGetter(obj, prop, getter) {
    if (Object.defineProperty) {
      Object.defineProperty(obj, prop, {
        get: getter
      });
    } else {
      obj.__defineGetter__(prop, getter);
    }
  }

  defineElementGetter(Element.prototype, 'classList', function () {
    return new DOMTokenList(this);
  });

})();
