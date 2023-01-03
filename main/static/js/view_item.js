function viewGameItem(id) {
    window.location.href = ('/view/game/'+id);
}

loading = `<img src="/media/loading.gif" alt="Loading" style="width: 200px; height: 200px; margin-left: auto; 
margin-right: auto; margin-top: auto; margin-bottom: auto;">`;
modalContainer = $('#modal-container');
$("#viewModal").on("hidden.bs.modal", function () {
    modalContainer.empty();
});
function viewCustomItem(model_id,id) {
    modalContainer.append(loading);
    $.ajax({
        url: '/view/'+model_id+'/'+id,
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