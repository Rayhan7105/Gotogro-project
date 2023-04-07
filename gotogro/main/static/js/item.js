$(document).ready(() => {
    // Validate name
    $("#id_name").change((event) => {
        validateEmpty($(event.currentTarget));
    });

    // Validate price
    $("#id_price").change((event) => {
        validateQuantity($(event.currentTarget));
    });

    // Validate stock
    $("#id_stock").change((event) => {
        validateQuantity($(event.currentTarget));
    });

    // Form submission
    $(".buttonWrapper").click(() => {
        if (validateEmpty($("#id_name")) && validateQuantity($("#id_price")) && validateQuantity($("#id_stock"))) {
            $("form").submit();
        }
    });
});