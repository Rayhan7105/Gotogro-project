$(document).ready(() => {
    // Validate first name
    $("#id_first_name").change((event) => {
        validateLetters($(event.currentTarget));
    });

    // Validate last name
    $("#id_last_name").change((event) => {
        validateLetters($(event.currentTarget));
    });

    // Validate email
    $("#id_email").change((event) => {
        validateEmail($(event.currentTarget));
    });

    // Validate postcode
    $("#id_postcode").change((event) => {
        validatePostcode($(event.currentTarget));
    });

    // Form submission
    $(".buttonWrapper").click(() => {
        if (validateLetters($("#id_first_name")) && validateLetters($("#id_last_name")) && validateEmail($("#id_email")) && validatePostcode($("#id_postcode"))) {
            $("form").submit();
        }
    });
    $("#export").click(() => {
        window.location.href = "http://127.0.0.1:8000/memberscsv";
    });
});