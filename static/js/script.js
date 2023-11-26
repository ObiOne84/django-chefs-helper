$(document).ready(function () {
    // update html page date
    $('#copyright').text(new Date().getFullYear());

    // print recipe card
    $('#print-button').on("click", function () {
        let body = $('body').html();
        print(body);
    });

    // activate logout modal
    $('#logout-link').on("click", function () {
        let myModal = new bootstrap.Modal(document.getElementById('logoutModal'));
        myModal.show();
    })

    // django messages timeout source:https://api.jquery.com/hide/#hide
    setTimeout(function() {
        $('#msg').hide();
    }, 3000);
});