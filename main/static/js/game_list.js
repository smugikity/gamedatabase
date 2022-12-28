$(document).ready(function(){

    //
    $('.select2-class').select2();
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
                    results: data.items
                };
            },
        },
        placeholder: 'Search',
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
    //



    max_page = $('#page-collections').attr('value');
    custom = $('#django-custom').val();
    current = parseInt($('#django-page').val());
    modalContainer = $('#modal-container')
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
    $("#viewModal").on("hidden.bs.modal", function () {
        modalContainer.empty();
    });
});	
function truncate(str, n){
    return (str.length > n) ? str.slice(0, n-1) + '&hellip;' : str;
};
function goToPage(page) {
    try {
        page = parseInt(page);
        if (!isFinite(page) || page<1 || page>max_page) {throw "exceed";}
        window.location.replace('/list/'+custom+'?sort='+ $('#sort').find(":selected").val()+'&n_per='+$('#pro').val()+'&page='+page);
    }
    catch(err) {
        console.log(err);
        return;
    }
}
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