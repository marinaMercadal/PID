(function () {
  var SELECTOR_CONTENEDOR = "[data-recargable]";

  function reemplazarContenido(html, url) {
    var documentoNuevo = new DOMParser().parseFromString(html, "text/html");
    var contenedorActual = document.querySelector(SELECTOR_CONTENEDOR);
    var contenedorNuevo = documentoNuevo.querySelector(SELECTOR_CONTENEDOR);

    if (!contenedorActual || !contenedorNuevo) {
      window.location.href = url;
      return;
    }

    contenedorActual.innerHTML = contenedorNuevo.innerHTML;
    document.title = documentoNuevo.title;
    window.history.pushState({}, "", url);
  }

  function navegar(url, opciones) {
    var contenedor = document.querySelector(SELECTOR_CONTENEDOR);
    if (contenedor) contenedor.classList.add("cargando");

    fetch(url, opciones)
      .then(function (respuesta) {
        if (!respuesta.ok) {
          window.location.reload();
          return null;
        }
        return respuesta.text().then(function (html) {
          return { html: html, url: respuesta.url };
        });
      })
      .then(function (resultado) {
        if (resultado) reemplazarContenido(resultado.html, resultado.url);
      })
      .catch(function () {
        window.location.href = url;
      })
      .finally(function () {
        var contenedorActual = document.querySelector(SELECTOR_CONTENEDOR);
        if (contenedorActual) contenedorActual.classList.remove("cargando");
      });
  }

  document.addEventListener("click", function (evento) {
    var link = evento.target.closest(SELECTOR_CONTENEDOR + " a");
    if (!link || link.target === "_blank" || link.origin !== window.location.origin) return;
    evento.preventDefault();
    navegar(link.href);
  });

  document.addEventListener("submit", function (evento) {
    if (!evento.target.closest(SELECTOR_CONTENEDOR)) return;
    var form = evento.target;
    evento.preventDefault();
    var metodo = (form.getAttribute("method") || "GET").toUpperCase();

    if (metodo === "GET") {
      var parametros = new URLSearchParams(new FormData(form));
      navegar(form.action.split("?")[0] + "?" + parametros.toString());
    } else {
      navegar(form.action, { method: "POST", body: new FormData(form) });
    }
  });

  window.addEventListener("popstate", function () {
    navegar(window.location.href);
  });
})();
