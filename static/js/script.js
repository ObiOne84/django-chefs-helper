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
    const hideButton = (message) => {
        setTimeout(function () {
            $(message).hide();
        }, 3000);
    }
    // setTimeout(function () {
    //     $('#msg').hide();
    //     $('#alert-rated').hide();
    // }, 3000);

    hideButton('#msg');
    hideButton('#alert-rated');
    hideButton('#no-recipe-alert');

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
        $('#rating-container').html('');

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

            if (!quantityField.val()) {
                $(this).removeClass('show').addClass('hide');
                $(this).find("[name$='-DELETE']").prop('checked', true);
            } else {
                $(this).removeClass('hide').addClass('show');
                nameField.prop('required', true);
                quantityField.prop('required', true); // Fix the typo here
            }
        });
    });


    // // Add ingredient
    $("#ingredient-formset-container").on("click", ".add-ingredient", function () {
        // remove test console log
        console.log("Clicked plus");
        var formsetContainer = $("#ingredient-formset-container");
        var formsetRow = formsetContainer.find(".formset-row.hide:first");
        var nameField = formsetRow.find('input[name$="name"]');
        var quantityField = formsetRow.find('input[name$="quantity"]');

        if (formsetRow.length) {
            formsetRow.removeClass('hide');
            formsetRow.addClass('show');
            formsetRow.find("[name$='-DELETE']").prop('checked', false);
            // formsetRow.find("[name$='-name']").prop('required', true);
            nameField.prop('required', true);
            quantityField.prop('required', true);

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
            formsetRow.find("[name$='-name']").prop('required', false);
        } else {
            console.log("Cannot hide the last row");
        }
    });


    // Add instruction

    // $(document).on('click', '.add-instruction', function () {
    //     // Clone the first list item
    //     var newItem = $(this).closest('.instruction-list-item').clone();

    //     // Clear the input field in the new item
    //     newItem.find('input').val('');

    //     // Append the new item to the list
    //     $('.instruction-list').append(newItem);
    // });

    // Remove instruction

    // $(document).on('click', '.remove-instruction', function () {
    //     // Remove the clicked list item
    //     $(this).closest('.instruction-list-item:not(:first-child)').remove();
    // });

    // Add instruction list to instruction field

    // $('#add-recipe-form').submit(function (event) {
    //     console.log('Not submitted');
    //     event.preventDefault();
    //     let instructionValue = '';
    //     let x = 1;
    //     $('.instruction-list-item').each(function () {
    //         let inputValue = $(this).find('input').val();
    //         let step = '<p class="steps">' + '<strong>Step ' + x + '</strong>. ' + inputValue + '</p>';
    //         instructionValue += step;
    //         x += 1
    //     });

    //     $('textarea[name="instructions"]').val(instructionValue.trim());
    //     $(this).unbind('submit').submit();
    // });

    // function creates an input field with defined value

    // function createInputField(data) {
    //     return `<li class="my-1 instruction-list-item">
    //     <input type="text" class="d-inline form-control instruction-input-field instruction-steps" required value="${data}" placeholder="Add cooking instruction here...">
    //     <button type="button" class="btn-like list-button remove-instruction">
    //         <i class="fa-solid fa-circle-minus"></i>
    //     </button>
    //     <button type="button" name="add-instruction" class="btn-like list-button add-instruction">
    //         <i class="fa-solid fa-circle-plus d-inline"></i>
    //     </button>
    // </li>`;
    // }

    // Edit user instructions
    // let textareaContent = $('#id_instructions').html();
    // let decodedContent = $('<div/>').html(textareaContent).text();
    // let $textInstruction = $(decodedContent);

    // Check if $textInstruction contains any content
    // if ($textInstruction.length > 0) {
    //     let instructionList = $('#update-instruction-list');
    //     let instructionText = $textInstruction.filter('p.steps').map(function () {
    //         console.log("Success");
    //         let text = $(this).text();
    //         let insText = text.replace(/^Step \d+\. /, '');
    //         return insText
    //     }).get();

    //     // Loop through each element in the instructionText array
    //     $.each(instructionText, function (index, value) {
    //         let instruction = value;
    //         let inputField = createInputField(instruction);
    //         instructionList.append(inputField);

    //         console.log(instruction);
    //     });
    // } else {
    //     console.log('No content found in #id_instructions');

    // }


    // $('#udpate-recipe-form').submit(function (event) {
    //     console.log('Form submitted');
    //     event.preventDefault();

    //     // Clear the current textarea content
    //     $('textarea[name="instructions"]').val('');
    //     let instructionValue = '';
    //     let x = 1;
    //     $('.instruction-list-item').each(function () {
    //         let inputValue = $(this).find('input').val();
    //         let step = '<p class="steps">' + '<strong>Step ' + x + '</strong>. ' + inputValue + '</p>';
    //         instructionValue += step;
    //         x += 1
    //         console.log(inputValue);
    //         console.log(instructionValue);
    //     });

    //     // $('textarea[name="instructions"]').val('');
    //     console.log(instructionValue);
    //     $('textarea[name="instructions"]').val(instructionValue.trim());
    //     console.log(instructionValue);
    //     $(this).unbind('submit').submit();
    // });


    // Check if on add_recipe.html page, and if the form has any values entered,
    // and when user try to leave before saving, warn about loosing any information entered
    // source: https://stackoverflow.com/questions/33805766/detect-current-page-with-javascript
    var pathname = window.location.pathname;

    switch (pathname) {
        case "/add_recipe":

            let formSubmitted = false;
            $('#add-recipe-form').on('submit', function () {
                formSubmitted = true;
            });

            window.addEventListener('beforeunload', function (event) {
                if (!formSubmitted) {
                    let formElements = document.querySelectorAll('.form-field');

                    let hasValue = false;

                    formElements.forEach(function (element) {
                        if (!element.value.trim()) {
                            console.log('Form element is empty');
                        } else {
                            console.log('Form element has value');
                            hasValue = true;
                        }
                    });

                    if (hasValue) {
                        var confirmationMessage = 'You have unsaved changes. Are you sure you want to leave?';
                        event.returnValue = confirmationMessage;
                        return confirmationMessage;
                    }
                }
            });
            break;
    }

    // add instruction textarea test here
    // Add instruction
    $(document).on('click', '.add-instruction', function () {
        // Clone the first list item
        var newItem = $(this).closest('.instruction-list-item').clone();

        // Clear the input field in the new item
        newItem.find('textarea').val('');

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
            let inputValue = $(this).find('textarea').val();
            let step = '<p class="steps">' + '<strong>Step ' + x + '</strong>. ' + inputValue + '</p>';
            instructionValue += step;
            x += 1
        });

        console.log('Instruction Value:', instructionValue);

        $('textarea[name="instructions"]').val(instructionValue.trim());
        $(this).unbind('submit').submit();
    });

    // function creates an input field with defined value
    function createInputField(data) {
        return `<li class="my-1 instruction-list-item instruction-textarea-field">
            <div class="input-group my-1">
            <textarea name="instruction-step" cols="40" rows="1" class="d-inline form-control instruction-input-field instruction-steps" required placeholder="Add cooking instruction here...">${data}</textarea>
            <button type="button" class="btn-like list-button remove-instruction">
                <i class="fa-solid fa-circle-minus"></i>
            </button>
            <button type="button" name="add-instruction" class="btn-like list-button add-instruction">
                <i class="fa-solid fa-circle-plus d-inline"></i>
            </button>
            </div>
        </li>`;
    }

    // Edit user instructions
    let textareaContent = $('#id_instructions').html();
    let decodedContent = $('<div/>').html(textareaContent).text();
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


    $('#udpate-recipe-form').submit(function (event) {
        console.log('Form submitted');
        event.preventDefault();

        // Clear the current textarea content
        $('textarea[name="instructions"]').val('');
        let instructionValue = '';
        let x = 1;
        $('.instruction-list-item').each(function () {
            let inputValue = $(this).find('textarea').val();
            let step = '<p class="steps">' + '<strong>Step ' + x + '</strong>. ' + inputValue + '</p>';
            instructionValue += step;
            x += 1
            console.log(inputValue);
            console.log(instructionValue);
        });

        // $('textarea[name="instructions"]').val('');
        console.log(instructionValue);
        $('textarea[name="instructions"]').val(instructionValue.trim());
        console.log(instructionValue);
        $(this).unbind('submit').submit();
    });

    function validateReviewForm(field) {
        let reviewField = $(field);
        let reviewValue = reviewField.val().trim();

        if (reviewValue === '') {
            // Display error message
            $('.empty-error').text('Text input cannot be empty').show();

            // Remove the error message after 5 seconds
            setTimeout(function () {
                $('.empty-error').empty().hide();
            }, 5000);
            return false;
        }

        // Continue with form submission or other actions if needed
        return true;
    }

    $('#review-form').submit(function () {
        return validateReviewForm('.review-body-holder textarea');
    });



});