function decreaseAmount() {
    if (document.getElementById("productAmount").value != 1) {
        document.getElementById("productAmount").stepDown(1);
        document.getElementById("toCart").setAttribute('href',
            getNewUrl(document.getElementById("toCart").getAttribute('href'),
                document.getElementById("productAmount").value));
    }
}

function increaseAmount(max) {
    if (document.getElementById("productAmount").value != max) {
        document.getElementById("productAmount").stepUp(1);
        document.getElementById("toCart").setAttribute('href',
            getNewUrl(document.getElementById("toCart").getAttribute('href'),
                document.getElementById("productAmount").value));
    }
    else {

        $('increase').on('click', function () {
            $(this).tooltip('enable').tooltip('open');
        });
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
