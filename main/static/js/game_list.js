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

    
    max_page = $('#page-collections').attr('value');
    custom = $('#django-custom').val();
    current = parseInt($('#django-page').val());
    $('#page-previous:first-child').on( "click", function() {goToPage(current-1);});
    $('#page-next:first-child').on( "click", function() {goToPage(current+1);});
    const templatePage1 = `<div class="page-item"><button class="page-link btn" type="button" onclick=goToPage(this.textContent)>`;
    const templatePage1active = `<div class="page-item active"><button class="page-link btn" type="button">`;
    const templatePage2 = `</button></div>`;
    pages = "";
    if (max_page<6) {
        pages += renderPage(1,max_page);
    } 
    else {
        if (current<4) {
            pages += renderPage(1,4);
            pages += renderEllipsis();
            pages += renderPage(max_page,max_page);
        } else if (current>max_page-3) {
            pages += renderPage(1,1);
            pages += renderEllipsis();
            pages += renderPage(max_page-3,max_page);
        } else {
            pages += renderPage(1,1);
            pages += renderEllipsis();
            pages += renderPage(current-1,current+1);
            pages += renderEllipsis();
            pages += renderPage(max_page,max_page);
        }
    }
    $(pages).insertBefore('#page-next');

    function renderPage(start,end) {
        var template = "";
        for (let i=start; i<=end; i++) {
            if (i === current) {template += templatePage1active + i + templatePage2;}
            else {template += templatePage1 + i + templatePage2;}
        }
        return template;
    }
    function renderEllipsis() {
        return templatePage1 + "..." + templatePage2;
    }

    $('#reset-button').on("click", function() {
        $('.select2-class').val(null).trigger('change');
        $('#datepicker').datepicker('clearDates');
    })
    $('#apply-button').on("click",function() { goToPage(current);});
});	

function goToPage(page) {
    try {
        page = parseInt(page);
        if (!isFinite(page) || page<1 || page>max_page) {throw "exceed";}
        var url_string = '/game-list/?sort='+ $('#sort').find(":selected").val()+'&n_per='+$('#pro').val()+'&page='+page;
        const startdate = $('#datepicker-start').datepicker('getFormattedDate');
        if (startdate) url_string += '&startdate='+startdate;
        const enddate = $('#datepicker-end').datepicker('getFormattedDate');
        if (enddate) url_string += '&enddate='+enddate;
        $('#select2-genre').select2('data').forEach(genre => {url_string += '&genre='+genre.id});
        $('#select2-publisher').select2('data').forEach(publisher => {url_string += '&publisher='+publisher.id});
        $('#select2-platform').select2('data').forEach(platform => {url_string += '&platform='+platform.id});
        window.location.replace(url_string);
    }
    catch(err) {
        console.log(err);
        return;
    }
}
