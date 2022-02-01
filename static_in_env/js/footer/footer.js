function sendMail() {
    var mail = document.getElementById("mailfield").value;
    $.ajax({
        type: 'GET',
        url: "send-mail",
        data: { "mail": mail},
        success: function (response) {
            // if not valid user, alert the user
            if (response["scc"]) {
                $('#MailSended').modal('show');
            }
            else{
                $('#MailNotSended').modal('show');
            }
        },
        error: function (response) {
            $('#MailNotSended').modal('show');
        }
    });
}