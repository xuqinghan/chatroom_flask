(function () {
	w = window,
	w.user_list = {
        clicked:  function(item){
        	var temp = item.innerHTML;
            var name = item.name;
            var cNode = d.getElementById("user_list").getElementsByTagName('li');
        	for( var i=0; i<cNode.length; i++){
        	    alert(cNode[i].innerHTML);
            }
        	//console.log(name)
        },
    };

})();