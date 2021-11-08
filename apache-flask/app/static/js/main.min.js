"use strict";
Array.from(document.getElementsByClassName("menu is-menu-main")).forEach(
  function (e) {
    Array.from(e.getElementsByClassName("has-dropdown-icon")).forEach(function (
      e
    ) {
      e.addEventListener("click", function (e) {
        var t = e.currentTarget
          .getElementsByClassName("dropdown-icon")[0]
          .getElementsByClassName("mdi")[0];
        e.currentTarget.parentNode.classList.toggle("is-active"),
          t.classList.toggle("mdi-plus"),
          t.classList.toggle("mdi-minus");
      });
    });
  }
),
  Array.from(document.getElementsByClassName("jb-aside-mobile-toggle")).forEach(
    function (e) {
      e.addEventListener("click", function (e) {
        var t = e.currentTarget
          .getElementsByClassName("icon")[0]
          .getElementsByClassName("mdi")[0];
        document.documentElement.classList.toggle("has-aside-mobile-expanded"),
          t.classList.toggle("mdi-forwardburger"),
          t.classList.toggle("mdi-backburger");
      });
    }
  ),
  Array.from(document.getElementsByClassName("jb-navbar-menu-toggle")).forEach(
    function (e) {
      e.addEventListener("click", function (e) {
        var t = e.currentTarget
          .getElementsByClassName("icon")[0]
          .getElementsByClassName("mdi")[0];
        document
          .getElementById(e.currentTarget.getAttribute("data-target"))
          .classList.toggle("is-active"),
          t.classList.toggle("mdi-dots-vertical"),
          t.classList.toggle("mdi-close");
      });
    }
  ),
  Array.from(document.getElementsByClassName("jb-modal")).forEach(function (e) {
    e.addEventListener("click", function (e) {
      var t = e.currentTarget.getAttribute("data-target");
      document.getElementById(t).classList.add("is-active"),
        document.documentElement.classList.add("is-clipped");
    });
  }),
  Array.from(document.getElementsByClassName("jb-modal-close")).forEach(
    function (e) {
      e.addEventListener("click", function (e) {
        e.currentTarget.closest(".modal").classList.remove("is-active"),
          document.documentElement.classList.remove("is-clipped");
      });
    }
  ),
  Array.from(
    document.getElementsByClassName("jb-notification-dismiss")
  ).forEach(function (e) {
    e.addEventListener("click", function (e) {
      e.currentTarget.closest(".notification").classList.add("is-hidden");
    });
  });


  
// For Live Projects
window.addEventListener("load", function () {
  document.querySelector("body").classList.add("loaded");
});








// // Get the modal
// var modal = document.getElementById("sample-modal");

// // Get the button that opens the modal
// var btn = document.getElementById("oda_sec");

// // Get the <span> element that closes the modal
// var span = document.getElementsByClassName("delete jb-modal-close")[0];
// var close = document.getElementsByClassName("button jb-modal-close")[0];
// // When the user clicks on the button, open the modal

// btn.onclick = function () {
//   modal.style.display = "block";
// };

// // When the user clicks on <span> (x), close the modal
// span.onclick = function () {
//   modal.style.display = "none";
// };
// close.onclick = function () {
//   modal.style.display = "none";
// };

// // When the user clicks anywhere outside of the modal, close it
// window.onclick = function (event) {
//   if (event.target == modal) {
//     modal.style.display = "none";
//   }
// };

// function click_sec(tiklanan_id) {
//   document.getElementById("oda_numarasi").value = tiklanan_id;
//   modal.style.display = "none";
// }
