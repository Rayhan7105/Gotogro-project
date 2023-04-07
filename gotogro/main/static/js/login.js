$(document).ready(() => {
    // Validate on update
    $("input").change((event) => {
        validateEmpty($(event.currentTarget));
    });

    // Form submission
    $(".buttonWrapper").click(() => {
        if ($("input").each((index, element) => { validateEmpty($(element)); })) {
            $("form").submit();
        }
    });
});