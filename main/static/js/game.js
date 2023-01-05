const selectedCssClass = 'selected';
$(document).ready(function() {
    tab_reviews_section = $('#tab-reviews-section');
    tab_list_section = $('#tab-list-section');
    tab_loading_img = $('#tab-loading-img');
    token =  $('input[name="csrfmiddlewaretoken"]').attr('value'); 
    comment_box = $('#comment-box');
    comment_box.scrollTop(1000);
    
    showReviews();
    if (is_authenticated) {
        $('#wish-icon').on("click", function() {
            if ($(this).children(":first").hasClass("fa-heart")) {
                $.ajax({
                    url: '/p-list/wishlist/remove?game='+game_id,
                });
            } else {
                $.ajax({
                    url: '/p-list/wishlist/add?game='+game_id,
                });
            }
            $(this).children(":first").toggleClass('fa-heart fa-heart-o');
        });

        $('#comment-submit').on('click', function() {
            submitComment();
        });

        $('#self-star-rating li').on('click', function() {
            var $this = $(this);
            $this.siblings('.' + selectedCssClass).removeClass(selectedCssClass);
            $this
              .addClass(selectedCssClass)
              .parent().addClass('vote-cast');
        });
        
        $('#review-delete').on('click', function() {
            deleteReview();
        });

        $('#review-save').on('click', function() {
            saveReview();
        });
    } else {
        $('#comment-submit').attr("disabled", true);
        $('#review-delete').attr("disabled", true);
        $('#review-save').attr("disabled", true);
    }
});


function showReviews() {
    tab_loading_img.show();
    try {
        $.ajax({
            url: '/rating?n_per=5&by_game='+game_id+'&by_user='+user_id,
            dataType:'json',
            success: function(res) {
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

function submitComment() {
    content = $('#comment-input').val();
    $('#comment-input').val("");
    if (content.trim()==="") return;
    $.ajax({
        type: 'POST',
        url: '/comment/add',
        data:{
            csrfmiddlewaretoken: token,
            content: content,
            game_id: game_id,
        },
        success: function(res) {
            comment_box.append(`<li><div class="commenterImage"><a href="/profile/`+username+`"><img src="`+pfp+`"/></a>
            </div><div class="commentText"><a class="text-decoration-none text-reset" href="/profile/`+username+`"><b>`+username+`</b></a><br/>
                <p class="">`+content+`</p></div></li>`);
            comment_box.scrollTop(1000);
        },
        error: function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}

function saveReview() {
    $('#review-error').empty();
    selectedStar = $('#self-star-rating .star.selected');
    if (!(selectedStar.length)) return;
    rating = selectedStar.attr("value");
    title = $('#review-input-title').val();
    content = $('#review-input-content').val();
    $.ajax({
        type: 'POST',
        url: '/review/add',
        data:{
            csrfmiddlewaretoken: token,
            rating: rating.trim(),
            title: title.trim(),
            content: content,
            game_id: game_id,
        },
        success: function(res) {
            $('#review-alert-danger').hide();
            $('#review-alert-success').html('Update successfully!').show();
        },
        error: function(xhr,errmsg,err) {
            $('#review-alert-success').hide();
            $('#review-alert-danger').html(xhr.responseText).show();
            console.log(error); // provide a bit more info about the error to the console
        }
    });
}

function deleteReview() {
    $('#review-error').empty();
    $('#self-star-rating').children('.' + selectedCssClass).removeClass(selectedCssClass);
    $('#review-input-title').val("");
    $('#review-input-content').val("");
    $.ajax({
        type: 'POST',
        url: '/review/delete',
        data:{
            csrfmiddlewaretoken: token,
            game_id: game_id,
        },
        success: function(res) {
            $('#review-alert-danger').hide();
            $('#review-alert-success').html('Update successfully!').show();
        },
        error: function(xhr,errmsg,err) {
            $('#review-alert-success').hide();
            $('#review-alert-danger').html(xhr.responseText).show();
            console.log(err); // provide a bit more info about the error to the console
        }
    });
}