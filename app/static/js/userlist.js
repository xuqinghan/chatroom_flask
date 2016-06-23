(function () {
    d = document,
    w = window,
    w.USERLIST = {
        selected_id : -1,
        user_dict : {},

        build_dict_local:function(){
            //模拟加载全部用户
            user_dict = {};
            var cNode = d.getElementById("user_list").getElementsByTagName('li');
            for( var i=0; i<cNode.length; i++){
                var uid = cNode[i].getAttribute("uid");
                var usrname = cNode[i].getAttribute("usrname"); //自定义属性要用这个函数才能取！
                user_dict[uid] = {};
                user_dict[uid]["usrname"] = usrname;
                user_dict[uid]["silenced"] = false;
                user_dict[uid]["enhance"] = false;
            }
        },
        clicked:  function(obj){
        	var temp = obj.innerHTML;
            
            var clicked_id = obj.getAttribute("uid");

            var cNode = d.getElementById("user_list").getElementsByTagName('li');
        	for( var i=0; i<cNode.length; i++){
                var uid = cNode[i].getAttribute("uid");
                var usrname = cNode[i].getAttribute("usrname"); //自定义属性要用这个函数才能取！
                if (clicked_id == uid){
                    cNode[i].innerHTML = "<mark>" + usrname + "</mark>"; //当前选中
                }
                else{
                    cNode[i].innerHTML = usrname;//恢复普通显示
                }
                
        	    //alert(cNode[i].innerHTML);
            }
            selected_id = clicked_id;
        	//console.log(temp)
            alert(selected_id);
        },
        change_silenced:  function(){ //点击禁言按钮，对selected_id用户进行禁言操作

            obj = d.getElementById("user_list").getElementsByAttributeValue("uid",selected_id).first();
            if (obj.classList.contains("silenced")) {
                obj.classList.remove("silenced");
                //obj.innerHTML = "<mark>" + usrname + "</mark>";
            }
            else{
                obj.classList.add("silenced");
            }
            alert(obj.innerHTML);
        },
    };

})();