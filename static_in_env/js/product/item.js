function increaseAmount() {
    document.getElementById("productAmount").stepUp(1);
}
function decreaseAmount() {
    document.getElementById("productAmount").stepDown(1);
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