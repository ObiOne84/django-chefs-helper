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


    // Hides all ingredient fields, and marke them for delegit co
    // $(".formset-row").not(":first").removeClass('show').addClass('hide');
    // $(".formset-row").not(":first").find("[name$='-DELETE']").prop('checked', true);
    $("#ingredient-formset-container").find('.formset-row').each(function () {
        var nameField = $(this).find('input[name$="name"]');
        var quantityField = $(this).find('input[name$="quantity"]');
        var unitField = $(this).find('select[name$="unit"]');

        if (!nameField.val() && !quantityField.val()) {
            console('some value is here');
        } else {
            console.log('Some data');
        }
    });

    // // Add ingredient
    $("#ingredient-formset-container").on("click", ".add-ingredient", function () {
        console.log("Clicked plus");
        var formsetContainer = $("#ingredient-formset-container");
        var formsetRow = formsetContainer.find(".formset-row.hide:first");

        if (formsetRow.length) {
            formsetRow.removeClass('hide');
            formsetRow.addClass('show');
            formsetRow.find("[name$='-DELETE']").prop('checked', false);
        } else {
            // If no hidden rows are available, you can choose to do nothing or provide some feedback
            console.log("No hidden rows available");
            formsetRow.find("[name$='-DELETE']").prop('checked', true);
        }
    });


    $("#ingredient-formset-container").on("click", ".remove-ingredient", function () {
        console.log("Clicked minus");
        var formsetRow = $(this).closest(".formset-row");
        var formsetRows = $('.formset-row.show'); // Get all visible rows

        if (formsetRows.length > 1) {
            formsetRow.removeClass('show');
            formsetRow.addClass('hide');
            formsetRow.find("[name$='-DELETE']").prop('checked', true);
        } else {
            console.log("Cannot hide the last row");
        }
    });


});