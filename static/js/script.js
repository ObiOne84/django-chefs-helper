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
        $('#alert-rated').hide();
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

    // Display average rating as starts
    let aveRating = $('#average-rating').html();
    let aveRatingNum = parseFloat(aveRating);
    // Check if the conversion was successful
    if (!isNaN(aveRatingNum)) {
        // Round the average rating to the nearest 0.5
        let roundedRating = Math.round(aveRatingNum * 2) / 2;

        // Clear existing stars
        // $('#rating-container').html('');

        // Add full stars
        for (let i = 0; i < Math.floor(roundedRating); i++) {
            $('#rating-container').append('<i class="fa-solid fa-star full-stars"></i> ');
        }

        // Add half star if needed
        if (roundedRating % 1 !== 0) {
            $('#rating-container').append('<i class="fa-solid fa-star-half-stroke"></i> ');
        }

        // Add empty stars
        for (let i = Math.ceil(roundedRating); i < 5; i++) {
            $('#rating-container').append('<i class="fa-regular fa-star empty-stars"></i> ');
        }

        console.log("Numeric Value:", aveRatingNum);
    } else {
        console.log("It's not a number");
    }

    // Dark mode
    // Toggle dark mode when the button is clicked
    document.getElementById('toggleDarkMode').addEventListener('click', function () {
        document.body.classList.toggle('dark-mode');
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


    $(document).ready(function () {
        $('#add-ingredient').click(function () {
            // Clone the last form and append it to the formset
            var newForm = $('#update-recipe-form .formset:last').clone(true);
            newForm.find(':input').val('');
            $('#update-recipe-form .formset:last').after(newForm);
        });
    });


});