$(document).ready(() => {
    // Setup autocomplete
    $('#autocomplete-member').autocomplete({onAutocomplete: (val) => { setMemberValue(val); }});
    $('#autocomplete-item').autocomplete({onAutocomplete: (val) => { createItemChip(val); }});
    var member_instance = M.Autocomplete.getInstance($('#autocomplete-member'));
    var item_instance = M.Autocomplete.getInstance($('#autocomplete-item'));
    var member_id;
    var item_ids = [];

    // Set member autocomplete value
    setMemberValue = (val) => {
        member_id = val.match(/\(([^)]+)\)/)[1];
        var member_name = val.split(' (')[0];
        $('#autocomplete-member').val(member_name);
    }

    // Setup chips
    createItemChip = (val) => {
        var item_id = val.match(/\(([^)]+)\)/)[1];
        var item_name = val.split(' (')[0];

        if (!item_ids.includes(item_id)) {
            $('#item-chip').append(`<div id='${item_id}' class='chip'>${item_name}<i id='item-close' class='close material-icons'>close</i></div>`);
            item_ids.push(item_id);
        }

        $('#autocomplete-item').val('');
        $('#autocomplete-item').removeClass('populated');
    };

    // Chip close
    $("#item-chip").on('click', (event) => {
        var item_index = item_ids.indexOf($(event.currentTarget).attr('id'));
        item_ids.splice(item_index, 1);
    });

    // Members ajax
    getMembers = (member_name) => {
        var csrftoken = $('[name=csrfmiddlewaretoken]').val();

        $.ajax({
            url: '/get-members',
            type: 'POST',
            dataType: 'json',
            headers: {'X-CSRFToken': csrftoken},
            data: {'member_name': member_name},
    
            success: (data) => {
                var jdata = JSON.parse(data.members);
                var member_data = {};
                var member;

                for (i = 0; i < jdata.length; i++) {
                    member = `${jdata[i].fields.first_name} ${jdata[i].fields.last_name} (${jdata[i].pk})`;
                    member_data[member] = null;
                };

                member_instance.updateData(member_data);
            }
        });
    };

    // Items ajax
    getItems = (item_name) => {
        var csrftoken = $('[name=csrfmiddlewaretoken]').val();

        $.ajax({
            url: '/get-items',
            type: 'POST',
            dataType: 'json',
            headers: {'X-CSRFToken': csrftoken},
            data: {'item_name': item_name},
    
            success: (data) => {
                var jdata = JSON.parse(data.items);
                var item_data = {};
                var item;

                for (i = 0; i < jdata.length; i++) {
                    item = `${jdata[i].fields.name} (${jdata[i].pk})`;
                    item_data[item] = null;
                };

                item_instance.updateData(item_data);
            }
        });
    };

    // Fire member ajax on regex match
    $('#autocomplete-member').on('input', (event) => {
        if ($(event.currentTarget).val().match(/[A-Za-z]+/) != null) {
            getMembers($(event.currentTarget).val());
        };
    });

    // Fire item ajax on regex match
    $('#autocomplete-item').on('input', (event) => {
        if ($(event.currentTarget).val().match(/[A-Za-z]+/) != null) {
            getItems($(event.currentTarget).val());
        };
    });

    // Validate first name
    $("#id_total_cost").change((event) => {
        validateQuantity($(event.currentTarget));
    });

    // Validate member
    $("#autocomplete-member").change((event) => {
        validateEmpty($(event.currentTarget));
    });

    // Form submission
    $("#addData").click(() => {
        // $("#id_member").children().each((index, element) => {
        //     if (element.value == member_id) {
        //         $(element).attr("selected", "");
        //     }
        // });

        // $("#id_item").children().each((index, element) => {
        //     item_ids.forEach(elem => {
        //         if(element.value == elem) {
        //             $(element).attr("selected", "");
        //         }
        //     });
        // });

        $("#id_member").val(member_id)
        $("#id_item").val(item_ids)
        if (validateQuantity($("#id_total_cost")) && validateEmpty($("#autocomplete-member")) && validateChildren($("#item-chip"), $("#autocomplete-item"))) {
            $("form").submit();
        }
    });

    $("#export").click(() => {
        window.location.href = "http://127.0.0.1:8000/salescsv";
    });
});