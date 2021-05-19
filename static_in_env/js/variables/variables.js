function SaveCategory(cat, value){
	localStorage.setItem(cat, value);
}
	
function GetCategory(cat){
	return localStorage[cat];
}






