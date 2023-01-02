$(document).ready(function() {
    searching = 0;
    //list pages start
    pageSection = $('#page-section');
    cardSection = $('#card-section');
    //list pages end

    custom = $('#django-custom').val();
    modalContainer = $('#modal-container');
    $("#viewModal").on("hidden.bs.modal", function () {
        modalContainer.empty();
    });
    searchText = $('#search-text');
    sort = $('#sort');
    n_per = $('#pro');
    $('#search-button').on("click", function() {
        searching = 1;
        goToPage(1);
    })
    $('#reset-button').on("click", function() {
        $('#search-text').val("");
    })
    $('#apply-button').on("click",function() {
        searching = 0;
        goToPage(current);
    });
});	


function truncate(str, n){
    return (str.length > n) ? str.slice(0, n-1) + '&hellip;' : str;
};

const loading = `<img src="/media/loading.gif" alt="Loading" style="width: 200px; height: 200px; margin-left: auto; 
margin-right: auto; margin-top: auto; margin-bottom: auto;">`
function viewCustomItem(id) {
    modalContainer.append(loading);
    $.ajax({
        url: '/view/'+custom+'/'+id,
        type: "GET",
        dataType: "json",
        success: (data) => {
            var tem = `<div class="image-container ">
                <div class="bg-image" id="modal-image" style='background-image: url("/media/`+data.image+`");'></div>
            </div>
            <div class="movie-info">
                <h2>`+data.custom+` no.`+data.id+`</h2>
                <div>
                    <h1>`+data.title+`</h1><small>Released Date: 27 Nov 2013</small>
                </div>
                <h4>Rating: 7.4 / 10</h4>
                <p>`+data.description+`</p>
                <div class="tags-container"><span>Animation</span><span>Adventure</span><span>Comedy</span></div>
            </div>`
            console.log(data);
            modalContainer.empty();
            modalContainer.append(tem);
        },
        error: (error) => {console.log(error);}
      });
}

//list pages start
const templatePage1 = `<div class="page-item"><button class="page-link btn" type="button" onclick=goToPage(this.textContent)>`;
const templatePage1active = `<div class="page-item active"><button class="page-link btn" type="button">`;
const templatePage2 = `</button></div>`;
function goToPage(page) {
    try {
        cardSection.empty();
        $('#loading-img').show()
        page = parseInt(page);
        if (!isFinite(page) || page<1) {throw "exceed";}
        term = searchText.val().trim();
        if (searching && term !== "") {
            url='/custom-search/'+custom+'?sort='+ sort.find(":selected").val()+'&n_per='+n_per.val()+'&page='+page+'&q='+term;
        }
        else url='/src/list/'+custom+'?sort='+ sort.find(":selected").val()+'&n_per='+n_per.val()+'&page='+page
        $.ajax({
            url: url,
            dataType:'json',
            // beforeSend:function(){
            // 	$(".ajaxLoader").show();
            // },
            success:function(res){
                console.log(res);
                $('#loading-img').hide()
                pageSection.html(res.p);
                cardSection.html(res.c);
            }
        });
    }
    catch(err) {
        console.log(err);
        return;
    }
}