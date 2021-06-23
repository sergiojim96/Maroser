function initPayment(total) {
    paypal.Buttons({
        createOrder: function (data, actions) {
            var totalValue = parseInt(document.getElementById("finalPrice").innerHTML.replace('$', ''));
            var totalValueConvertion = totalValue * 0.8;
            gtag('event', 'conversion', {
                'send_to': 'AW-348792047/uRoRCOyOj8gCEO_JqKYB',
                'value': totalValueConvertion,
                'currency': 'USD'
            });
            // This function sets up the details of the transaction, including the amount and line item details.
            return actions.order.create({
                purchase_units: [{
                    amount: {
                        value: totalValue
                    }
                }]
            });
        },
        onApprove: function (data, actions) {
            $('#myModal').modal('show');
            // Authorize the transaction
            actions.order.authorize().then(function (authorization) {

                // Get the authorization id
                var authorizationID = authorization.purchase_units[0]
                    .payments.authorizations[0].id;
                // Call your server to validate and capture the transaction
                $.ajax({
                    type: 'GET',
                    url: "/order-summary/pay/" + data.orderID + "/" + authorizationID,
                    success: function (response) {
                        // if not valid user, alert the user
                        $('#myModal').modal('hide');
                        if (response["scc"]) {
                            window.location = "/order-summary/resume"
                        }
                    },
                    error: function (response) {
                        $('#myModal').modal('hide');
                        $('#myModalError').modal('show');
                        var oldQ = "h"
                    }
                });
            });
        }
    }).render('#paypal-button-container');
}
