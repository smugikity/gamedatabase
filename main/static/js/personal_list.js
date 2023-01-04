const addon_url = 'list_id='+list_id;
$(document).ready(function() {
    //list pages start
    pageSection = $("#page-section");
    cardSection = $("#card-section");
    //list pages end

    $('#datepicker').datepicker();
    //Select2 
    $('.select2-class').select2({
        ajax: {
            url: function () {
                return '/search/' + this.attr('value');
            },
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return {
                    q: params.term, // search term
                };
            },
            processResults: function (data) {
                return {
                    results: data.items,
                };
            },
        },
        placeholder: 'Type something',
        minimumInputLength: 1,
        templateResult: formatSelect2Result,
        templateSelection: formatSelect2Selecion
    }); 
    function formatSelect2Result (item) {
        if (item.loading) {
            return 'loading...';
        }
        return item.title;
    }
    function formatSelect2Selecion (item) {
        return item.title;
    }
    //End select 2
    searching = 0;
    searchText = $('#search-text');
    sort = $('#sort');
    n_per = $('#pro');
    $('#search-button').on("click", function() {
        searching = 1;
        goToPage(1);
    })
    $('#reset-button').on("click", function() {
        $('.select2-class').val(null).trigger('change');
        $('#datepicker').datepicker('clearDates');
        $('#search-text').val("");
    })
    $('#apply-button').on("click",function() {
        searching = 0;
        goToPage(current);
    });

    goToPage(1);
});	

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
            url='/src/game-search?sort='+ sort.find(":selected").val()+'&n_per='+n_per.val()+'&page='+page+'&q='+term+'&'+addon_url;
        }
        else url='/src/game-list?sort='+ sort.find(":selected").val()+'&n_per='+n_per.val()+'&page='+page+'&'+addon_url;
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

