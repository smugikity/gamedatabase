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

    current = 1;
    pageSection = $("#page-section");
    cardSection = $("#card-section");

    $('#search-button').on("click", function() {
        searchPage($('#search-text').val());
    })

    $('#reset-button').on("click", function() {
        $('.select2-class').val(null).trigger('change');
        $('#datepicker').datepicker('clearDates');
        $('#search-text').val("");
    })

    $('#apply-button').on("click",function() {goToPage(current);});
});	

templatePage1 = `<div class="page-item"><button class="page-link btn" type="button" onclick=goToPage(this.textContent)>`;
templatePage1active = `<div class="page-item active"><button class="page-link btn" type="button">`;
templatePage2 = `</button></div>`;
function goToPage(page) {
    try {
        cardSection.empty();
        $('#loading-img').show()
        page = parseInt(page);
        if (!isFinite(page) || page<1) {throw "exceed";}
        var url_string = '/src/game-list?sort='+ $('#sort').find(":selected").val()+'&n_per='+$('#pro').val()+'&page='+page;
        const startdate = $('#datepicker-start').datepicker('getFormattedDate');
        if (startdate) url_string += '&startdate='+startdate;
        const enddate = $('#datepicker-end').datepicker('getFormattedDate');
        if (enddate) url_string += '&enddate='+enddate;
        $('#select2-genre').select2('data').forEach(genre => {url_string += '&genre='+genre.id});
        $('#select2-publisher').select2('data').forEach(publisher => {url_string += '&publisher='+publisher.id});
        $('#select2-platform').select2('data').forEach(platform => {url_string += '&platform='+platform.id});
        $.ajax({
			url: url_string,
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

function searchPage(term) {
    try {
        cardSection.empty();
        $('#loading-img').show()
        $.ajax({
			url: '/game-search?q='+term,
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

function viewGame(id) {
    window.location.href = ('/view/game/'+id);
}