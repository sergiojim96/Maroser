function filterProducts() {
    var PWomen = document.getElementsByName('PWoman');
    var PMen = document.getElementsByName('PMan');
    var PSmart = document.getElementsByName('PSmart');
    var select = document.getElementById("categoriesSelect");
    var selected = select.options[select.selectedIndex].value;
    if (selected == "0") {
        select.style.backgroundColor = '#ffffff';
        select.style.color = 'black';
        blockDisplay(PWomen);
        blockDisplay(PMen);
        blockDisplay(PSmart);
    }
    if (selected == "1") {
        select.style.backgroundColor = '#d1a2a3';
        blockDisplay(PWomen);
        hideDisplay(PMen);
        hideDisplay(PSmart);
        select.style.color = 'white';
    }
    if (selected == "2") {
        var selected = select.style.backgroundColor = '#2f4555';
        hideDisplay(PWomen);
        blockDisplay(PMen);
        hideDisplay(PSmart);
        select.style.color = 'white';
    }
    if (selected == "3") {
        var selected = select.style.backgroundColor = '#2f4555';
        hideDisplay(PWomen);
        hideDisplay(PMen);
        blockDisplay(PSmart);
        select.style.color = 'white';
    }
}

function blockDisplay(tagsList) {
    var i;
    for (i = 0; i < tagsList.length; i++) {
        tagsList[i].style.display = "block";
    }
}

function hideDisplay(tagsList) {
    var i;
    for (i = 0; i < tagsList.length; i++) {
        tagsList[i].style.display = "none";
    }
}

function checkCategory(){
	var category = GetCategory(); 
	if(category != "all" || category != undefined){
		if( category === "men")
		{
			document.getElementById("categoriesSelect").value = 2;
		}
		else if( category === "women")
		{
			document.getElementById("categoriesSelect").value = 1;
		}
		else if( category === "smart")
		{
			document.getElementById("categoriesSelect").value = 3;
		}
	}
	filterProducts();
}