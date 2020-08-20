function SaveCategory(cat){
	localStorage.setItem("category", cat);
}
	
function GetCategory(){
	return localStorage["category"];
}
