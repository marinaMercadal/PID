(function () {
  var SELECTOR_CONTENEDOR = "[data-recargable]";

  var peticionActual = null;

  function actualizarFecha(fecha) {
    document.querySelectorAll('[data-recargable] input[name="fecha"]').forEach(function (input) {
      input.value = fecha;
    });
    document.querySelectorAll(".mini-calendario-dia").forEach(function (link) {
      link.classList.toggle("mini-calendario-dia-seleccionado", new URL(link.href).searchParams.get("fecha") === fecha);
    });
    var nuevaJuntada = document.querySelector("[data-nueva-juntada]");
    if (nuevaJuntada) {
      var destino = new URL(nuevaJuntada.href);
      destino.searchParams.set("fecha", fecha);
      nuevaJuntada.href = destino.href;
    }
  }

  function mostrarDiaLocal(url, guardarHistorial) {
    var destino = new URL(url, window.location.href);
    if (destino.pathname !== "/calendario") return false;
    var fecha = destino.searchParams.get("fecha");
    if (!fecha) {
      var hoy = new Date();
      fecha = hoy.getFullYear() + "-" + String(hoy.getMonth() + 1).padStart(2, "0") + "-" + String(hoy.getDate()).padStart(2, "0");
    }
    var plantilla = Array.from(document.querySelectorAll("template[data-eventos-fecha]")).find(function (item) {
      return item.dataset.eventosFecha === fecha;
    });
    var panel = document.querySelector(".calendario-eventos");
    if (!plantilla || !panel) return false;
    if (peticionActual) peticionActual.abort();
    panel.replaceChildren(plantilla.content.cloneNode(true));
    var contenedor = document.querySelector(SELECTOR_CONTENEDOR);
    contenedor.dataset.calendarioFecha = fecha;
    contenedor.classList.remove("cargando");
    actualizarFecha(fecha);
    if (guardarHistorial) window.history.pushState({}, "", destino.href);
    return true;
  }

  function reemplazarContenido(html, url, guardarHistorial) {
    var documentoNuevo = new DOMParser().parseFromString(html, "text/html");
    var contenedorActual = document.querySelector(SELECTOR_CONTENEDOR);
    var contenedorNuevo = documentoNuevo.querySelector(SELECTOR_CONTENEDOR);

    if (!contenedorActual || !contenedorNuevo) {
      window.location.href = url;
      return;
    }

    contenedorActual.innerHTML = contenedorNuevo.innerHTML;
    document.title = documentoNuevo.title;
    if (guardarHistorial) window.history.pushState({}, "", url);
    if (contenedorActual.dataset.calendarioFecha && contenedorNuevo.dataset.calendarioFecha) {
      contenedorActual.dataset.calendarioFecha = contenedorNuevo.dataset.calendarioFecha;
      actualizarFecha(contenedorNuevo.dataset.calendarioFecha);
    }
  }

  function navegar(url, opciones, guardarHistorial) {
    if (guardarHistorial === undefined) guardarHistorial = true;
    if (peticionActual) peticionActual.abort();
    var controlador = new AbortController();
    peticionActual = controlador;
    opciones = Object.assign({}, opciones, { signal: controlador.signal });
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
        if (resultado) reemplazarContenido(resultado.html, resultado.url, guardarHistorial);
      })
      .catch(function (error) {
        if (error.name === "AbortError") return;
        window.location.href = url;
      })
      .finally(function () {
        if (peticionActual !== controlador) return;
        peticionActual = null;
        var contenedorActual = document.querySelector(SELECTOR_CONTENEDOR);
        if (contenedorActual) contenedorActual.classList.remove("cargando");
      });
  }

  document.addEventListener("click", function (evento) {
    var link = evento.target.closest(SELECTOR_CONTENEDOR + " a");
    if (evento.button !== 0 || evento.ctrlKey || evento.metaKey || evento.shiftKey || evento.altKey) return;
    if (!link || link.target === "_blank" || link.origin !== window.location.origin) return;
    evento.preventDefault();
    if (!mostrarDiaLocal(link.href, true)) navegar(link.href);
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
    if (!mostrarDiaLocal(window.location.href, false)) navegar(window.location.href, undefined, false);
  });
})();
