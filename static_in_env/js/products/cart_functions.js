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
                var dataBundle = response["dataBundle"];
                var quantityField = document.getElementById("quantityField");
                if (quantityField != 0) {
                    quantityField.value = quantityField.value - 1;
                    document.getElementById("finalPrice").innerHTML = "$" + dataBundle["total"];
                    document.getElementById(dataBundle["slug"]).innerHTML = "$" + dataBundle["itemPrice"];
                    document.getElementById("tax").innerHTML = "$" + dataBundle["tax"];
                }
                else {
                    location.reload();
                }
            }
        },
        error: function (response) {
            console.log(response)
        }
    })
}

function add_single_item_to_cart_funtion(url) {
    $.ajax({
        type: 'GET',
        url: url,
        success: function (response) {
            // if not valid user, alert the user
            if (response["scc"]) {
                var dataBundle = response["dataBundle"];
                var quantityField = document.getElementById("quantityField");
                quantityField.value = quantityField.value + 1;
                document.getElementById("finalPrice").innerHTML = "$" + dataBundle["total"];
                document.getElementById(dataBundle["slug"]).innerHTML = "$" + dataBundle["itemPrice"];
                document.getElementById("tax").innerHTML = "$" + dataBundle["tax"];
            }
        },
        error: function (response) {
            console.log(response)
        }
    })
}