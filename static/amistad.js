(function () {
  function actualizarSugerencias(input) {
    var lista = document.getElementById("sugerencias");
    if (!lista) return;

    var texto = input.value.trim().toLowerCase();
    var items = lista.querySelectorAll("li");

    if (!texto) {
      lista.hidden = true;
      return;
    }

    var hayCoincidencias = false;
    items.forEach(function (item) {
      var coincide = item.dataset.nombre.toLowerCase().includes(texto);
      item.hidden = !coincide;
      if (coincide) hayCoincidencias = true;
    });
    lista.hidden = !hayCoincidencias;
  }

  document.addEventListener("input", function (evento) {
    if (evento.target.id === "nombre") actualizarSugerencias(evento.target);
  });

  document.addEventListener("focusin", function (evento) {
    if (evento.target.id === "nombre") actualizarSugerencias(evento.target);
  });

  document.addEventListener("click", function (evento) {
    var input = document.getElementById("nombre");
    var lista = document.getElementById("sugerencias");
    if (!input || !lista) return;

    var item = evento.target.closest("#sugerencias li");
    if (item) {
      input.value = item.dataset.nombre;
      lista.hidden = true;
      input.form.requestSubmit();
      return;
    }

    if (!input.contains(evento.target) && !lista.contains(evento.target)) {
      lista.hidden = true;
    }
  });
})();
