function async_remove_from_cart_funtion(slug) {
    $.ajax({
        type: 'GET',
        url: "async-remove-from-cart",
        data: { "slug": slug },
        success: function (response) {
			if (response["scc"] === "Ok") {
                location.reload();
			}
			else if (response["scc"] === "OrderNotExists") {
				$('#OrderNotExists').modal('show');
			}
        },
        error: function (response) {
            location.reload();
        }
    })
}

function remove_single_item_from_cart_funtion(url, slug) {
    var quantityField = Number(document.getElementById("quantityField" + slug).value);
    if (quantityField != 1) {
        $.ajax({
            type: 'GET',
            url: url,
            success: function (response) {
                // if not valid user, alert the user
                if (response["scc"] === "Ok") {
                    var dataBundle = response["dataBundle"];
                    document.getElementById("quantityField" + slug).stepDown(1);
                    document.getElementById("finalPrice").innerHTML = "$" + dataBundle["total"];
                    document.getElementById(dataBundle["slug"]).innerHTML = "$" + dataBundle["itemPrice"];
                    document.getElementById("tax").innerHTML = "$" + dataBundle["tax"];
                }
				else if (response["scc"] === "OrderNotExists") {
					$('#OrderNotExists').modal('show');
				}
				else if (response["scc"] === "NotInOrder") {
					$('#NotInOrder').modal('show');
				}
            },
            error: function (response) {
                window.alert("Error");
            }
        })
    }
}

function add_single_item_to_cart_funtion(url, slug, stock) {
    var quantityField = Number(document.getElementById("quantityField" + slug).value);
    if (quantityField != stock) {
        $.ajax({
            type: 'GET',
            url: url,
            success: function (response) {
                // if not valid user, alert the user
                if (response["scc"] === "Ok") {
                    const dataBundle = response["dataBundle"];
                    document.getElementById("quantityField" + slug).stepUp(1);
                    document.getElementById("finalPrice").innerHTML = "$" + dataBundle["total"];
                    document.getElementById(dataBundle["slug"]).innerHTML = "$" + dataBundle["itemPrice"];
                    document.getElementById("tax").innerHTML = "$" + dataBundle["tax"];
                }
				else if (response["scc"] === "OrderNotExists") {
					$('#OrderNotExists').modal('show');
				}
				else if (response["scc"] === "NotInOrder") {
					$('#NotInOrder').modal('show');
				}
            },
            error: function (response) {
                window.alert("Error");
            }
        })
    }
}

function sendMail() {
    $.ajax({
        type: 'GET',
        url: "send-mail",
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