function async_remove_from_cart_funtion(slug) {
    $.ajax({
        type: 'GET',
        url: "async-remove-from-cart",
        data: { "slug": slug },
        success: function (response) {
            // if not valid user, alert the user
            if (response["scc"]) {
                location.reload();
            }
        },
        error: function (response) {
            console.log(response)
        }
    })
}

function remove_single_item_from_cart_funtion(url) {
    $.ajax({
        type: 'GET',
        url: url,
        success: function (response) {
            // if not valid user, alert the user
            if (response["scc"]) {
                var oldQ = parseInt(document.getElementById(slug).innerHTML.trim());
                document.getElementById(slug).innerHTML = " " + (oldQ - 1) + " ";
            }
        },
        error: function (response) {
            console.log(response)
        }
    })
}

function add_single_item_to_cart_funtion(slug) {
    $.ajax({
        type: 'GET',
        url: "{% url 'core:add-single-item-to-cart' %}",
        data: { "slug": slug },
        success: function (response) {
            // if not valid user, alert the user
            if (response["scc"]) {
                var oldQ = parseInt(document.getElementById(slug).innerHTML.trim());
                document.getElementById(slug).innerHTML = " " + (oldQ + 1) + " ";
            }
        },
        error: function (response) {
            console.log(response)
        }
    })
}