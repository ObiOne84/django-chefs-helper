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
    setTimeout(function () {
        $('#msg').hide();
    }, 3000);

    // setting star rating 
    $('.star-rating i').on('click', function () {
        let value = $(this).data('value');
        // source: https://api.jquery.com/val/#val
        $('#id_rating').val(value);

        $(this).addClass('active fa-solid').removeClass('fa-regular');
        $(this).prevAll().addClass('active fa-solid').removeClass('fa-regular');
        $(this).nextAll().addClass('fa-regular').removeClass('active fa-solid');
    });

    // Add rating form validation
    // $('#review-form').submit(function (e) {
    //     e.preventDefault();
    //     let rating = $('#id_rating').data('value');
    //     let range = [1, 2, 3, 4, 5];
    //     let rated = $('#rated-alert').css('display');
    //     let rate = $('#rating-alert').css('display', 'block');

    //     if (!(range.includes(rating)) || rated === 'none') {
    //         alert("please rate the recipe");
    //     } else {
    //         $(this).submit();
    //     }
    // });

});