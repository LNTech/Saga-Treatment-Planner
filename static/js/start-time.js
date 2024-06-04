function load_locations() {
    $.getJSON('/start-time/data', function(data) {
        $.each(data, function(index, item){
            var checkbox = $('input[data-customer="' + item.customer + '"][data-site="' + item.site + '"]');
            checkbox.prop('checked', true);
        });
        console.log("Loaded locations.");
    });
};

function save_locations() {
    var selectedFields = [];
    $('.siteCheck').each(function() {
        if ($(this).prop('checked')) {
            var selection = {
                "customer": $(this).data('customer'),
                "site": $(this).data('site')
            };
            selectedFields.push(selection);
        };
    });

    var jsonData = JSON.stringify(selectedFields);
    $.ajax({
        url: '/start-time/data',
        type: 'POST',
        contentType: 'application/json',
        data: jsonData,
        success: function(data) {
            console.log("Saved locations.");
        }
    });
}

$(document).ready(function() {
    load_locations();

    $('.select_all').click(function() {
        var parent = $(this).parent().parent();
        parent.find('.siteCheck').prop('checked', true);
    });
    
    $('#select_all_sites').click(function() {
        $('.siteCheck').prop('checked', true);
    });

    $('#clear_selection').click(function() {
        $('.siteCheck').prop('checked', false);
    });

    $('#save_selection').click(function() {
        save_locations();
    });
});