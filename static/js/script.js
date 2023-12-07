$(document).ready(function () {
    // update html page date
    $('#copyright').text(new Date().getFullYear());

    // print recipe card
    $('#print-button').on("click", function () {
        let body = $('body').html();
        print(body);
    });

    // function to activate modal
    const showModal = (object, event, modal) => {
        $(object).on(event, function () {
            let myModal = new bootstrap.Modal(document.getElementById(modal));
            myModal.show();
        });
    };

    showModal('#logout-link', 'click', 'logoutModal');
    showModal('#delete-recipe-link', 'click', 'deleteRecipeModal');

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
    // document.getElementById('toggleDarkMode').addEventListener('click', function () {
    //     document.body.classList.toggle('dark-mode');
    // });

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

    function updateFormset() {

        // Loop through each form in the formset
        $('form[name="ingredient_formset"]').find('.formset-row').each(function () {
            var nameField = $(this).find('input[name$="name"]');
            var quantityField = $(this).find('input[name$="quantity"]');
            var unitField = $(this).find('select[name$="unit"]');

            // Check if both name and quantity are empty
            if (!nameField.val() && !quantityField.val()) {
                // Remove the formset row from the DOM
                $(this).remove();

            }
        });

        // Check the number of remaining visible formset rows
        var remainingVisibleRows = $('form[name="ingredient_formset"]').find('.formset-row:visible').length;
        console.log('here is:' + remainingVisibleRows);

        // Disable the minus button if there is only one row left
        if (remainingVisibleRows === 1) {
            $('form[name="ingredient_formset"]').find('.remove-ingredient').prop('disabled', true);
        } else {
            $('form[name="ingredient_formset"]').find('.remove-ingredient').prop('disabled', false);
        }
    }

    $('.formset').on('input', 'input, select', function () {
        updateFormset($('.formset-row'));
    });

    $('.add-ingredient').on('click', function () {
        alert('You clicked plus');

        updateFormset($('.formset-row'));

    });

    $('.remove-ingredient').on('click', function () {

        updateFormset($('.formset-row'));
        $(this).closest('.formset-row').hide();
    });

});