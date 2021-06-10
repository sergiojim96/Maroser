function SendUserMail(){
	var mail = document.getElementsByClassName("form-control textinfc")[0].value;
	console.log(mail)
	 $.ajax({
        type: 'GET',
        url: "send-mail",
		data: {"mail":mail},
        success: function (response) {
            if (response["scc"]) {
                $('#MailSended').modal('show');
            }
        },
        error: function (response) {
            $('#MailNotSended').modal('show');
        }
    })
}