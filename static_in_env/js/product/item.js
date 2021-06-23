function decreaseAmount() {
    if (document.getElementById("productAmount").value != 1) {
        document.getElementById("productAmount").stepDown(1);
    }
}

function increaseAmount(max) {
    if (document.getElementById("productAmount").value != max) {
        document.getElementById("productAmount").stepUp(1);
    }
}

function getNewUrl(str, char) {
    var xStr = str.substring(0, str.length - 1);
    return xStr + char;
}

function AddToCart(itemUrl) {
    var quantity = Number(document.getElementById("productAmount").value);
    itemUrl = itemUrl.concat(quantity);
    console.log(quantity)
    $.ajax({
        type: 'GET',
        url: itemUrl,
        data: { "quantity": quantity },
        success: function (response) {
            // if not valid user, alert the user
            window.location.assign("/order-summary/");
        },
        error: function (response) {
            console.log(response)
        }
    })
}
