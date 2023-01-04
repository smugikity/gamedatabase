$(document).ready(function() {
  $('.tab-button').click(function() {
    $(this)
      .addClass("active")
      .siblings()
      .removeClass("active");
  });
  tabBtn = $('.tab-button');
  tab_reviews_section = $('#tab-reviews-section');
  tab_list_section = $('#tab-list-section');
  tab_loading_img = $('#tab-loading-img');
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
  tab_reviews_section.empty();
  tab_list_section.empty();
  if (panelIndex==0) {
    showReviews();
  } else {
    showList(panelIndex);
  }
}

function showReviews() {
  tab_loading_img.show();
  try {
    $.ajax({
        url: '/rating?n_per=5&by_user='+user_id,
        dataType:'json',
        success:function(res) {
            tab_loading_img.hide()
            tab_reviews_section.html(res.c
              +`<p class="my-4 text-center"><a href="{% url 'game-list' %}" class="btn btn-dark btn-sm"><i class="fa fa-thumbs-up"></i> All Reviews</a></p>`);
        }
    });
  }
  catch(err) {
      console.log(err);
      return;
  }
}

function showList(id) {
  tab_loading_img.show();
  try {
      $.ajax({
          url: '/src/game-search?list_id='+id,
          dataType:'json',
          success:function(res) {
              tab_loading_img.hide()
              tab_list_section.html(res.c
                +`<p class="my-4 text-center"><a href="/p-list/`+id+`" class="btn btn-dark btn-sm"><i class="fa fa-thumbs-up"></i> All items</a></p>`);
          }
      });
  }
  catch(err) {
      console.log(err);
      return;
  }
}

