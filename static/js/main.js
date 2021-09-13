function showPassword() {
    var x = document.getElementById("Password");
    if (x.type === "password") {
      x.type = "text";
    } else {
      x.type = "password";
    }
  }


// Get the container element
var btnContainer = document.getElementById("myDiv");

// Get all buttons with class="btn" inside the container
var btns = btnContainer.getElementsByClassName("nav__link");

// Loop through the buttons and add the active class to the current/clicked button
for (var i = 0; i < btns.length; i++) {
  btns[i].addEventListener("click", function() {
    var current = document.getElementsByClassName("active");

    // If there's no active class
    if (current.length > 0) {
      current[0].className = current[0].className.replace(" active", "");
    }

    // Add the active class to the current/clicked button
    this.className += " active";
  });
}
// Get the modal
// var modal = document.getElementById("myModal");

// // Get the image and insert it inside the modal - use its "alt" text as a caption
// var img = document.getElementById("webImage");
// var modalImg = document.getElementById("img01");
// var captionText = document.getElementById("caption");

// img.onclick = function(){
//   modal.style.display = "block";
//   modalImg.src = this.src;
//   captionText.innerHTML = this.alt;
// }

// // Get the <span> element that closes the modal
// var span = document.getElementsByClassName("close")[0];

// // When the user clicks on <span> (x), close the modal
// span.onclick = function() {
//   modal.style.display = "none";
// }

/* Navbar fx */



// function scrollFunction(){
//   document.getElementById("navbar").style.background = "#fff";
// }

// const navToggle = document.querySelector(".nav-toggle");
// const navLinks = document.querySelectorAll(".nav__link");

// navToggle.addEventListener("click", () => {
//   document.body.classList.toggle("nav-open");
// });

// navLinks.forEach((link) =>{
//   link.addEventListener("click", () => {
//       document.body.classList.remove("nav-open");
//   });
// });

