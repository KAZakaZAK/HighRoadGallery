(function () {
  "use strict";

  var toggle = document.querySelector(".menu-toggle");
  var menu = document.getElementById("site-menu");
  var desktop = window.matchMedia("(min-width: 1024px)");

  function setMenu(open) {
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Close menu" : "Menu");
    menu.classList.toggle("is-open", open);
    document.body.style.overflow = open ? "hidden" : "";
  }

  if (toggle && menu) {
    toggle.addEventListener("click", function () {
      setMenu(toggle.getAttribute("aria-expanded") !== "true");
    });
    menu.addEventListener("click", function (event) {
      if (event.target.closest("a")) { setMenu(false); }
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && menu.classList.contains("is-open")) {
        setMenu(false);
        toggle.focus();
      }
    });
    desktop.addEventListener("change", function (event) {
      if (event.matches) { setMenu(false); }
    });
  }

  var year = document.getElementById("year");
  if (year) { year.textContent = String(new Date().getFullYear()); }

  /* Demo forms: validate, then confirm on the page. Nothing is sent. */
  function clearError(field) {
    field.classList.remove("is-invalid");
    var err = field.querySelector(".field__error");
    if (err) { err.remove(); }
    var control = field.querySelector("input, select, textarea");
    if (control) { control.removeAttribute("aria-invalid"); control.removeAttribute("aria-describedby"); }
  }

  function showError(field, message) {
    var control = field.querySelector("input, select, textarea");
    var err = document.createElement("p");
    err.className = "field__error";
    err.id = control.id + "-error";
    err.textContent = message;
    field.classList.add("is-invalid");
    field.appendChild(err);
    control.setAttribute("aria-invalid", "true");
    control.setAttribute("aria-describedby", err.id);
  }

  document.querySelectorAll("[data-demo-form]").forEach(function (form) {
    var status = form.querySelector(".form__status");
    form.addEventListener("input", function (event) {
      var field = event.target.closest(".field");
      if (field) { clearError(field); }
    });
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var first = null;
      form.querySelectorAll(".field").forEach(function (field) {
        clearError(field);
        var control = field.querySelector("input, select, textarea");
        if (!control.checkValidity()) {
          var label = field.querySelector("label").textContent.toLowerCase();
          showError(field, control.validity.valueMissing ? "Enter " + label + "." : "Check " + label + ".");
          if (!first) { first = control; }
        }
      });
      if (first) {
        status.hidden = true;
        first.focus();
        return;
      }
      status.hidden = false;
      status.textContent = "Thanks. This is a design preview, so nothing was sent.";
      form.reset();
    });
  });

  /* Donation amounts: single select, then a preview confirmation. */
  var amounts = document.querySelectorAll(".amount");
  var donate = document.querySelector("[data-donate]");
  var donateStatus = document.querySelector("[data-donate-status]");
  amounts.forEach(function (button) {
    button.addEventListener("click", function () {
      amounts.forEach(function (other) { other.setAttribute("aria-pressed", "false"); });
      button.setAttribute("aria-pressed", "true");
      if (donateStatus) { donateStatus.hidden = true; }
    });
  });
  if (donate && donateStatus) {
    donate.addEventListener("click", function () {
      var chosen = document.querySelector('.amount[aria-pressed="true"]');
      donateStatus.hidden = false;
      donateStatus.textContent = chosen
        ? "Preview only. Next step would be checkout for " + chosen.getAttribute("data-amount") + "."
        : "Choose an amount first.";
    });
  }

  /* Add to calendar: downloads a placeholder .ics. */
  var ics = document.querySelector("[data-ics]");
  if (ics) {
    ics.addEventListener("click", function () {
      var lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//High Road Gallery//Preview//EN", "BEGIN:VEVENT",
        "UID:preview-event@highroadgallery", "DTSTAMP:20260101T000000Z", "DTSTART:20260109T170000Z", "DTEND:20260109T210000Z",
        "SUMMARY:High Road Gallery event (preview)", "LOCATION:12 E Stafford, Worthington, OH 43085", "END:VEVENT", "END:VCALENDAR"];
      var blob = new Blob([lines.join("\r\n")], { type: "text/calendar" });
      var link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = "high-road-event.ics";
      document.body.appendChild(link);
      link.click();
      link.remove();
      URL.revokeObjectURL(link.href);
    });
  }

  if ("serviceWorker" in navigator) {
    window.addEventListener("load", function () {
      navigator.serviceWorker.register("sw.js").catch(function () {});
    });
  }
})();
