document.addEventListener("DOMContentLoaded", function() {
  // Eventuali validazioni dinamiche per il form dei parametri
  const form = document.querySelector(".parameters-card form");
  if (form) {
    form.addEventListener("submit", function(e) {
      const inpsRate = parseFloat(document.getElementById("inpsRate").value);
      if (inpsRate < 0 || inpsRate > 100) {
        alert("L'aliquota INPS deve essere compresa tra 0 e 100%.");
        e.preventDefault();
      }
    });
  }
});
