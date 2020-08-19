function filterProducts() {
    var PWomen = document.getElementsByName('PWoman');
    var PMen = document.getElementsByName('PMan');
    var PSmart = document.getElementsByName('PSmart');
    var select = document.getElementById("categoriesSelect");
    var selected = select.options[select.selectedIndex].value;
    if (selected == "0") {
        blockDisplay(PWomen);
        blockDisplay(PMen);
        blockDisplay(PSmart);
    }
    if (selected == "1") {
        blockDisplay(PWomen);
        hideDisplay(PMen);
        hideDisplay(PSmart);
    }
    if (selected == "2") {
        hideDisplay(PWomen);
        blockDisplay(PMen);
        hideDisplay(PSmart);
    }
    if (selected == "3") {
        hideDisplay(PWomen);
        hideDisplay(PMen);
        blockDisplay(PSmart);
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