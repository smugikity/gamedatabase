$(document).ready(function() {
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

    searchText = $('#search-text');
    sort = $('#sort');
    n_per = $('#pro');
    $('#search-button').on("click", function() {
        $('.select2-class').val(null).trigger('change');
        $('#datepicker').datepicker('clearDates');
        searching = 1;
        goToPage(1);
    })
    $('#reset-button').on("click", function() {
        $('.select2-class').val(null).trigger('change');
        $('#datepicker').datepicker('clearDates');
        $('#search-text').val("");
    })
    $('#apply-button').on("click",function() {
        $('#search-text').val("");
        searching = 0;
        goToPage(current);
    });
    //list pages start
    pageSection = $("#page-section");
    cardSection = $("#card-section");
    //list pages end
    select2Genre=$('#select2-genre');
    select2Publisher=$('#select2-publisher');
    select2Platform=$('#select2-platform');
    searching=0;
    loadingImg = $('#loading-img');

    try {
        $.ajax({
            url: '/src/game-list'+init_paras_url,
            dataType:'json',
            success:function(res){
                loadingImg.hide()
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

//list pages start
const templatePage1 = `<div class="page-item"><button class="page-link btn" type="button" onclick=goToPage(this.textContent)>`;
const templatePage1active = `<div class="page-item active"><button class="page-link btn" type="button">`;
const templatePage2 = `</button></div>`;
function goToPage(page) {
    try {
        cardSection.empty();
        loadingImg.show()
        page = parseInt(page);
        if (!isFinite(page) || page<1) {throw "exceed";}
        var url_string = '';
        term = searchText.val().trim();
        if (searching) {
            url_string='/src/game-search?sort='+ sort.find(":selected").val()+'&n_per='+n_per.val()+'&page='+page+'&q='+term;
        } else {
            url_string = '/src/game-list?sort='+ sort.find(":selected").val()+'&n_per='+n_per.val()+'&page='+page;
            const startdate = $('#datepicker-start').datepicker('getFormattedDate');
            if (startdate) url_string += '&startdate='+startdate;
            const enddate = $('#datepicker-end').datepicker('getFormattedDate');
            if (enddate) url_string += '&enddate='+enddate;
            select2Genre.select2('data').forEach(genre => {url_string += '&genre='+genre.id});
            select2Publisher.select2('data').forEach(publisher => {url_string += '&publisher='+publisher.id});
            select2Platform.select2('data').forEach(platform => {url_string += '&platform='+platform.id});
        }
        $.ajax({
            url: url_string,
            dataType:'json',
            success:function(res){
                console.log(res);
                loadingImg.hide()
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

