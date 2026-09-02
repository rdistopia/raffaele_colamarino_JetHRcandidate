document.addEventListener("DOMContentLoaded", function() {
  const ralInput = document.getElementById("ralInput");
  const calcForm = document.getElementById("calcForm");

  if (ralInput) {
    // Pulisce eventuali spazi all'input
    ralInput.addEventListener("blur", function() {
      if (ralInput.value) {
        ralInput.value = ralInput.value.trim();
      }
    });
  }
});
