$(document).ready(() => {

    // Initialise dropdown and collapsible
    $(".dropdown-trigger").dropdown({hover: true, coverTrigger: false, alignment: "middle"});
    $('.collapsible').collapsible();
    
    // Input field animation
    $("input").change((event) => {
        if ($(event.currentTarget).val()) {
            $(event.currentTarget).addClass("populated");
        } else {
            $(event.currentTarget).removeClass("populated");
        };
    });

    // Set field to error state
    fieldError = (field, message) => {
        label = field.siblings("label");
        field.css("border-bottom", "2px solid red");
        label.html(`<i>${label.text().split(message.split(" ")[0])[0]} ${message}</i>`);
        label.css("color", "red");
        return false;
    }

    // Set field to valid state
    fieldValid = (field, message) => {
        label = field.siblings("label");
        field.css("border-bottom", "");
        label.html(`<i>${label.text().split(message.split(" ")[0])[0]}</i>`);
        label.css("color", "");
        return true;
    }

    // Check if field is empty
    validateEmpty = (field) => {
        message = "must not be empty";
        if (!field.val()) {
            return fieldError(field, message);
        }
        return fieldValid(field, message);
    }

    // Check if field only contains letters
    validateLetters = (field) => {
        message = "must only contain letters";
        if (field.val().match(/^[A-Za-z]+$/) == null) {
            return fieldError(field, message);
        }
        return fieldValid(field, message);
    }

    // Check if field contains valid email
    validateEmail = (field) => {
        message = "must be a valid email address";
        if (field.val().match(/\S+@\S+\.\S+/) == null) {
            return fieldError(field, message);
        }
        return fieldValid(field, message);
    }

    // Check if field contains valid postcode
    validatePostcode = (field) => {
        message = "must contain 4 numbers between 3000 and 3999";
        if (field.val().match(/^[0-9]+$/) == null || field.val() < 3000 || field.val() > 3999) {
            return fieldError(field, message);
        }
        return fieldValid(field, message);
    }

    // Check quantity is not less than 0
    validateQuantity = (field) => {
        message = "must not be less than 0";
        if (field.val() < 0) {
            return fieldError(field, message);
        }
        return fieldValid(field, message);
    }

    // Check element has children
    validateChildren = (parent, field) => {
        message = "must not be empty";
        if (parent.children().length < 1) {
            return fieldError(field, message);
        }
        return fieldValid(field, message);
    }
});