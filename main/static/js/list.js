$(document).ready(function() {
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
    //list pages start
    pageSection = $('#page-section');
    cardSection = $('#card-section');
    loadinImg = $('#loading-img');
    //list pages end
    searching=0;    

    try {
        $.ajax({
            url: '/src/list/'+custom+init_paras_url,
            dataType:'json',
            success:function(res){
                loadinImg.hide()
                pageSection.html(res.p);
                cardSection.html(res.c);
            }
        });
    }
    catch(err) {
        console.log(err);
        return;
    }

});	


function truncate(str, n){
    return (str.length > n) ? str.slice(0, n-1) + '&hellip;' : str;
};



//list pages start
const templatePage1 = `<div class="page-item"><button class="page-link btn" type="button" onclick=goToPage(this.textContent)>`;
const templatePage1active = `<div class="page-item active"><button class="page-link btn" type="button">`;
const templatePage2 = `</button></div>`;
function goToPage(page) {
    try {
        cardSection.empty();
        loadinImg.show()
        page = parseInt(page);
        if (!isFinite(page) || page<1) {throw "exceed";}
        term = searchText.val().trim();
        if (searching) {
            url='/src/custom-search/'+custom+'?sort='+ sort.find(":selected").val()+'&n_per='+n_per.val()+'&page='+page+'&q='+term;
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
                loadinImg.hide()
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