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

    // Hides empty ingredient fields except the first row or fields with values
    $(document).ready(function () {
        $("#ingredient-formset-container").find('.formset-row:not(:first)').each(function () {
            var nameField = $(this).find('input[name$="name"]');
            var quantityField = $(this).find('input[name$="quantity"]');

            // console.log('nameField value:', nameField.val());
            // console.log('quantityField value:', quantityField.val());

            if (!quantityField.val()) {
                console.log('No data');

                $(this).removeClass('show').addClass('hide');
                $(this).find("[name$='-DELETE']").prop('checked', true);
            } else {
                console.log('Some data');
                $(this).removeClass('hide').addClass('show');
            }
        });
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

    // Add instruction
    $(document).on('click', '.add-instruction', function () {
        // Clone the first list item
        var newItem = $(this).closest('.instruction-list-item').clone();

        // Clear the input field in the new item
        newItem.find('input').val('');

        // Append the new item to the list
        $('.instruction-list').append(newItem);
    });

    // Remove instruction
    $(document).on('click', '.remove-instruction', function () {
        // Remove the clicked list item
        $(this).closest('.instruction-list-item:not(:first-child)').remove();
    });

    // Add instruction list to instruction field
    $('#add-recipe-form').submit(function (event) {
        console.log('Not submitted');
        event.preventDefault();
        let instructionValue = '';
        let x = 1;
        $('.instruction-list-item').each(function () {
            let inputValue = $(this).find('input').val();
            let step = '<p class="steps">' + 'Step ' + x + '. ' + inputValue + '</p>';
            instructionValue += step;
            x += 1
        });

        $('textarea[name="instructions"]').val(instructionValue.trim());
        $(this).unbind('submit').submit();
    });

    // function creates an input field with defined value
    function createInputField(data) {
        return `<li class="instruction-list-item">
        <input type="text" style="width: 80%;" class="d-inline" required value="${data}">
        <button type="button" class="btn-like remove-instruction">
            <i class="fa-solid fa-circle-minus"></i>
        </button>
        <button type="button" name="add-instruction" class="btn-like add-instruction">
            <i class="fa-solid fa-circle-plus d-inline"></i>
        </button>
    </li>`;
    }

    // Edit user instructions
    let textareaContent = $('#id_instructions').html();
    let decodedContent = $('<div/>').html(textareaContent).text();
    console.log(decodedContent);
    let $textInstruction = $(decodedContent);

    // Check if $textInstruction contains any content
    if ($textInstruction.length > 0) {
        let instructionList = $('#update-instruction-list');
        let instructionText = $textInstruction.filter('p.steps').map(function () {
            console.log("Success");
            let text = $(this).text();
            let insText = text.replace(/^Step \d+\. /, '');
            return insText
        }).get();

        // Loop through each element in the instructionText array
        $.each(instructionText, function (index, value) {
            let instruction = value;
            let inputField = createInputField(instruction);
            instructionList.append(inputField);

            console.log(instruction);
        });
    } else {
        console.log('No content found in #id_instructions');
    }

    // $('#update-recipe-form').submit(function (event) {
    //     console.log('Not submitted');
    //     event.preventDefault();

    //     $('#update-instruction-text textarea').val('');

    //     let instructionValue = '';
    //     let x = 1;
    //     $('.instruction-list-item').each(function () {
    //         let inputValue = $(this).find('input').val();
    //         let step = '<p class="steps">' + 'Step ' + x + '. ' + inputValue + '</p>';
    //         instructionValue += step;
    //         $('#update-instruction-text textarea').val(instructionValue.trim());
    //         x += 1
    //     });


    //     $(this).unbind('submit').submit();
    // });


    $('#update-recipe-form').submit(function (event) {
        console.log('Form submitted');
        event.preventDefault();

        // Clear the current textarea content
        $('#update-instruction-text textarea').val('');

        let x = 1;
        $('.instruction-list-item input').each(function () {
            let inputValue = $(this).val();
            console.log(inputValue);
            let step = '<p class="steps">' + 'Step ' + x + '. ' + inputValue + '</p>';

            // Append the new content to the textarea
            $('#update-instruction-text textarea').val(function (index, value) {
                return value + step;
            });

            console.log(step);
            x += 1;
        });

        // Log the final textarea content
        console.log($('#update-instruction-text textarea').val());

        // Uncomment the line below to submit the form
        // $(this).unbind('submit').submit();
    });






});