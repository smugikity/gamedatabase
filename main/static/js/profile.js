$(document).ready(function() {
  $('.tab-button').click(function() {
    $(this)
      .addClass("active")
      .siblings()
      .removeClass("active");
  });
  tabBtn = $('.tab-button');
  tab = $('.tab');

  if (document.querySelector(".alert-message").innerText > 9) {
    document.querySelector(".alert-message").style.fontSize = ".7rem";
  }
  tabs(0);
  // bio = document.querySelector(".bio");
  // bioMore = document.querySelector("#see-more-bio");
  // bioLength = bio.innerText.length;
  // bioText();
  //        console.log(bio.innerText)
});

// function bioText() {
//   bio.oldText = bio.innerText;

//   bio.innerText = bio.innerText.substring(0, 100) + "...";
//   bio.innerHTML += `<span onclick='addLength()' id='see-more-bio'>See More</span>`;
// }

function tabs(panelIndex) {
  tab.each(function() {
    $(this).hide();
  });
  tab[panelIndex].style.display="block";
}

function addLength() {
  bio.innerText = bio.oldText;
  bio.innerHTML +=
    "&nbsp;" + `<span onclick='bioText()' id='see-less-bio'>See Less</span>`;
  document.getElementById("see-less-bio").addEventListener("click", () => {
    document.getElementById("see-less-bio").style.display = "none";
  });
}
