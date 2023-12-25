/*jshint esversion: 6 */
/* globals $, bootstrap */

$(document).ready(function () {

    // Update html page date
    $('#copyright').text(new Date().getFullYear());

    // Print recipe card
    $('#print-button').on("click", function () {
        let body = $('body').html();
        print(body);
    });

    showModal('#logout-link', 'click', 'logoutModal');
    showModal('#delete-recipe-link', 'click', 'deleteRecipeModal');

    // Hide Django messages
    hideButton('#msg');

    hideButton('#alert-rated');
    hideButton('#no-recipe-alert');
    hideButton('#title-error');

    hideAlert('.form-alert');

    rateRecipWithStars();

    dispalyAverageRatingAsStars();

    hideEmptyIngredientFieldsExceptFirst();

    addIngredientField();

    hideIngredientFields();

    warnWhenLeavesFormWithoutSaving();

    addInstructionField();

    removeInstructionField();

    addInstructionFieldToInstructionListTwo('#add-recipe-form');

    addInstructionFieldToInstructionListTwo('#udpate-recipe-form');

    putRecipeInstructionIntoSeparateFields();

    // Check review field if it is not empty, or empty spaces
    $('#review-form').submit(function () {
        return validateReviewForm('.review-body-holder textarea');
    });

});

/**
 * Function to show modal, on the event on the object, defined with jquery
 */
const showModal = (object, event, modal) => {
    $(object).on(event, function () {
        let myModal = new bootstrap.Modal(document.getElementById(modal));
        myModal.show();
    });
};

/**
 * Function to hide alert message after 3 seconds
 * source:https://api.jquery.com/hide/#hide
 */
const hideButton = (message) => {
    setTimeout(function () {
        $(message).hide();
    }, 3000);
};

/**
 * Function to hide alert message after 9 seconds
 */
const hideAlert = (alert) => {
    setTimeout(function () {
        $(alert).hide();
    }, 9000);
};

/**
 * Function to allow user rate the recipe by clicking on stars,
 * the stars will fill with color from first to the one chosen by user
 */
const rateRecipWithStars = () => {
    $('.star-rating i').on('click', function () {
        let value = $(this).data('value');
        // source: https://api.jquery.com/val/#val
        $('#id_rating').val(value);

        $(this).addClass('active fa-solid').removeClass('fa-regular');
        $(this).prevAll().addClass('active fa-solid').removeClass('fa-regular');
        $(this).nextAll().addClass('fa-regular').removeClass('active fa-solid');
    });
};

/**
 * Function displays average rating as stars, rounding the average rating
 * to nearest 0.5, and displaying half star for any value below 0.5
 */
const dispalyAverageRatingAsStars = () => {

    let aveRating = $('#average-rating').html();
    let aveRatingNum = parseFloat(aveRating);
    if (!isNaN(aveRatingNum)) {
        let roundedRating = Math.round(aveRatingNum * 2) / 2;

        $('#rating-container').html('');

        for (let i = 0; i < Math.floor(roundedRating); i++) {
            $('#rating-container').append('<i class="fa-solid fa-star full-stars"></i> ');
        }

        if (roundedRating % 1 !== 0) {
            $('#rating-container').append('<i class="fa-solid fa-star-half-stroke"></i> ');
        }

        for (let i = Math.ceil(roundedRating); i < 5; i++) {
            $('#rating-container').append('<i class="fa-regular fa-star empty-stars"></i> ');
        }
    }
};

/**
 * Function hides empty ingredient fields except the first on
 * also, it adds attribute required to name and quantity fields - first row
 * and unchecks DELETE hidden field for first row, and set hidden row DELETE
 * field to true
 */
const hideEmptyIngredientFieldsExceptFirst = () => {

    $('.ingredient-name:first').attr('required', 'required');
    $('.ingredient-quantity:first').attr('required', 'required');
    $("#ingredient-formset-container").find('.formset-row:not(:first)').each(function () {
        var nameField = $(this).find('input[name$="name"]');
        var quantityField = $(this).find('input[name$="quantity"]');

        if (!quantityField.val()) {
            $(this).removeClass('show').addClass('hide');
            $(this).find("[name$='-DELETE']").prop('checked', true);
        } else {
            $(this).removeClass('hide').addClass('show');
            nameField.prop('required', true);
            quantityField.prop('required', true);
        }
    });
};

/**
 * Function  unhides hidden ingredient fields on the click on the plus button
 * and make them required
 */
const addIngredientField = () => {

    $("#ingredient-formset-container").on("click", ".add-ingredient", function () {

        var formsetContainer = $("#ingredient-formset-container");
        var formsetRow = formsetContainer.find(".formset-row.hide:first");
        var nameField = formsetRow.find('input[name$="name"]');
        var quantityField = formsetRow.find('input[name$="quantity"]');
        var alertContainer = formsetRow.find('.ingredient-alert');

        if (formsetRow.length) {
            alertContainer.hide();
            formsetRow.removeClass('hide');
            formsetRow.addClass('show');
            formsetRow.find("[name$='-DELETE']").prop('checked', false);
            nameField.prop('required', true);
            quantityField.prop('required', true);
        } else {
            formsetRow.find("[name$='-DELETE']").prop('checked', true);
        }
    });
};

/**
 * Function  hides ingredient fields on the click on the minus button
 * removes attribute required, and clear their content
 */
const hideIngredientFields = () => {
    $("#ingredient-formset-container").on("click", ".remove-ingredient", function () {

        var formsetRow = $(this).closest(".formset-row");
        var formsetRows = $('.formset-row.show');
        var nameField = formsetRow.find('input[name$="name"]');
        var quantityField = formsetRow.find('input[name$="quantity"]');

        if (formsetRows.length > 1) {
            nameField.val('');
            quantityField.val('');
            formsetRow.removeClass('show');
            formsetRow.addClass('hide');
            formsetRow.find("[name$='-DELETE']").prop('checked', true);
            nameField.prop('required', false);
            quantityField.prop('required', false);
        }
    });
};

/**
 * Function first checks if on add_recipe.html page, and if the form has any values entered,
 * and when user tries to leave before saving, it display warnining message about loss of unsaved data
 * source: https://stackoverflow.com/questions/33805766/detect-current-page-with-javascript
 */
const warnWhenLeavesFormWithoutSaving = () => {

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
                        if (element.value.trim()) {
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
};

/**
 * Function  creates additional instruction fields by cloning the first field
 * and clearing its content on the click on the plus button
 * function creates instruction list
 */
const addInstructionField = () => {

    $(document).on('click', '.add-instruction', function () {

        var newItem = $(this).closest('.instruction-list-item').clone();
        newItem.find('textarea').val('');
        $('.instruction-list').append(newItem);

    });
};

/**
 * Function  allows to remove instruction fields, on the click of the minus
 * sign button, except the first field
 */
const removeInstructionField = () => {

    $(document).on('click', '.remove-instruction', function () {
        $(this).closest('.instruction-list-item:not(:first-child)').remove();
    });

};

/**
 * Function creates an textarea input field with defined value
 */
function createInputField(data) {
    return `<li class="my-1 instruction-list-item ">
        <div class="input-group instruction-textarea-field my-1">
           <textarea name="instruction-step" cols="40" rows="2"
              class="d-inline form-control instruction-input-field instruction-steps" required
              placeholder="Add cooking instruction here..." maxlength="350">${data}</textarea>
           <button class="btn btn-outline-secondary remove-instruction" type="button"><i
                 class="fa-solid fa-minus"></i></button>
           <button class="btn btn-outline-secondary add-instruction" type="button"><i
                 class="fa-regular fa-plus"></i></button>
        </div>
     </li>`;
}

/**
 * Function  checks field for empty value, and if empty it displays
 * error message to the user
 */
function validateReviewForm(className) {

    let isValid = true;

    $(className).each(function () {
        let reviewField = $(this);
        let reviewValue = reviewField.val().trim();

        if (reviewValue === '') {
            isValid = false;

            $('.empty-error').text('Text input cannot be empty').show();
            setTimeout(function () {
                $('.empty-error').empty().hide();
            }, 8000);

            reviewField.focus();
        }
    });
    return isValid;
}

/**
 * Function check instruction filed before form is submitted
 * and append content of instruction fields to the instruction box
 */
const addInstructionFieldToInstructionListTwo = (form) => {
    $(form).submit(function (event) {
        event.preventDefault();
        if (validateReviewForm('.instruction-input-field')) {
            // Clear the current textarea content
            $('textarea[name="instructions"]').val('');
            let instructionValue = '';
            let x = 1;
            $('.instruction-list-item').each(function () {
                let inputValue = $(this).find('textarea').val();
                let step = '<p class="steps">' + '<strong>Step ' + x + '</strong>. ' + inputValue + '</p>';
                instructionValue += step;
                x += 1;
            });

            $('textarea[name="instructions"]').val(instructionValue.trim());
            $(this).unbind('submit').submit();
        }
    });
};

/**
 * Function get instruciton from the instruction recipe field and
 * appends each instruction to separate textarea fields
 * after removing html formatting presented inside textarea box
 */
const putRecipeInstructionIntoSeparateFields = () => {
    // source: https://stackoverflow.com/questions/4635297/how-to-remove-html-tags-from-textarea-with-javascript

    let textareaContent = $('#id_instructions').html();
    let decodedContent = $('<div/>').html(textareaContent).text();
    let $textInstruction = $(decodedContent);

    if ($textInstruction.length > 0) {
        let instructionList = $('#update-instruction-list');
        let instructionText = $textInstruction.filter('p.steps').map(function () {
            let text = $(this).text();
            let insText = text.replace(/^Step \d+\. /, '');
            return insText;
        }).get();

        $.each(instructionText, function (index, value) {
            let instruction = value;
            let inputField = createInputField(instruction);
            instructionList.append(inputField);
        });
    }
};