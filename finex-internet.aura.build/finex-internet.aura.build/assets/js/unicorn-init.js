/* Initialize the UnicornStudio runtime. Loads the library on demand
   when not already on the page, then calls UnicornStudio.init() once. */
!function () {
  var e = function () {
    window.UnicornStudio &&
      !window.UnicornStudio.isInitialized &&
      (UnicornStudio.init(), (window.UnicornStudio.isInitialized = !0));
  };
  window.UnicornStudio
    ? e()
    : ((window.UnicornStudio = { isInitialized: !1 }),
      (function () {
        var n = document.createElement("script");
        n.src =
          "https://cdn.jsdelivr.net/gh/hiunicornstudio/unicornstudio.js@v1.4.29/dist/unicornStudio.umd.js";
        n.onload = e;
        (document.head || document.body).appendChild(n);
      })());
}();
