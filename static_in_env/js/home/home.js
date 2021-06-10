function getBSUrl(slug) {
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
