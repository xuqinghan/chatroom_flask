(function () {
	var d = document,
	w = window,
	p = parseInt,
	dd = d.documentElement,
	db = d.body,
	dc = d.compatMode == 'CSS1Compat',
	dx = dc ? dd: db,
	ec = encodeURIComponent;
	URL = window.URL;
	
	w.CHAT = {
		msgObj:d.getElementById("message"),
		screenheight:w.innerHeight ? w.innerHeight : dx.clientHeight,
		username:null,
		nickname:null,
		userid:null,
		socket:null,
		room:null,
		//让浏览器滚动条保持在最低部
		scrollToBottom:function(){
			w.scrollTo(0, this.msgObj.clientHeight);
		},
		close:function(){
			this.socket.disconnect();
		},
		//退出，本例只是一个简单的刷新
		logout:function(){
			this.socket.disconnect();
			//location.reload();
		},
		//提交聊天消息内容
		submit:function(){
			var content = d.getElementById("content").value;
			if(content != ''){
				var obj = {
					userid: this.userid,
					username: this.username,
					content: content
				};
				this.socket.emit('message_txt', obj);
				d.getElementById("content").value = '';
			}
			return false;
		},
		//提交录音内容
		submit_wav:function(blob){
			//var fd = new FormData();
    		//fd.append('audioData', blob);
			//if(content != ''){
/*				var obj = {
					userid: this.userid,
					username: this.username,
					content: blob
				};*/
				this.socket.emit('message_wav', blob);
				//d.getElementById("content").value = '';
			//}*/
			alert('发表录音消息');
			return false;
		},
		//提交录音内容
		submit_mp3:function(mp3Blob){
			//var fd = new FormData();
    		//fd.append('audioData', blob);
			if(content != ''){
				var obj =new Object();
				obj.userid = this.userid;
				obj.username = this.username;
				obj.content = mp3Blob
				this.socket.emit('message_mp3', obj);
				//d.getElementById("content").value = '';
			}
			alert('发表mp3录音消息');
			return false;
		},

		genUid:function(){
			return new Date().getTime()+""+Math.floor(Math.random()*899+100);
		},
		//更新系统消息，本例中在用户加入、退出的时候调用
		updateSysMsg:function(o, action){
			//当前在线用户列表
			var onlineUsers = o.onlineUsers;
			//当前在线人数
			var onlineCount = o.onlineCount;
			//新加入用户的信息
			var user = o.user;
				
			//更新在线人数
			var userhtml = '';
			var separator = '';
			for(key in onlineUsers) {
		        if(onlineUsers.hasOwnProperty(key)){
					userhtml += separator+onlineUsers[key];
					separator = '、';
				}
		    }
			d.getElementById("onlinecount").innerHTML = '当前共有 '+onlineCount+' 人在线，在线列表：'+userhtml;
			


			//添加系统消息
			var html = '';
			html += '<div class="msg-system">';
			html += user.username;
			html += (action == 'login') ? ' 加入了聊天室' : ' 退出了聊天室';
			html += '</div>';
			var section = d.createElement('section');
			section.className = 'system J-mjrlinkWrap J-cutMsg';
			section.innerHTML = html;
			this.msgObj.appendChild(section);	
			this.scrollToBottom();
		},
        userList_clicked:function(item){
        	var temp = item.innerHTML;
            var name = item.name;
            var cNode = d.getElementById("user_list").getElementsByTagName('li');
        	for( var i=0; i<cNode.length; i++){
        	    alert(cNode[i].innerHTML);
            }
        	//console.log(name)
        },
		//第一个界面用户提交用户名
		usernameSubmit:function(){
			var username = d.getElementById("username").value;
			var room = d.getElementById("room").value;
			this.room = room;
			console.log("usernameSubmit调用：room="+room);
			if(username != ""){
				d.getElementById("username").value = '';
				d.getElementById("loginbox").style.display = 'none';
				d.getElementById("chatbox").style.display = 'block';
				//this.init(username,this.genUid(),room);
				this.build(username,this.genUid(),room);
			}
			return false;
		},
		send:function(e,data){
			this.socket.emit(e,data);
		},
		login:function(){
			this.socket.emit('login', {userid:this.userid, username:this.username,room:this.room}); 
		},
		build:function(username,uid,room){
			/*
			客户端根据时间和随机数生成uid,这样使得聊天室用户名称可以重复。
			实际项目中，如果是需要用户登录，那么直接采用用户的uid来做标识就可以
			*/
			//alert("init调用："+username);
			console.log("init调用："+username);
			d.getElementById("loginbox").style.display = 'none';
			d.getElementById("chatbox").style.display = 'block';
			this.userid = uid;
			this.username = username;
			this.room = room;

			d.getElementById("showusername").innerHTML = this.username;
			//this.msgObj.style.minHeight = (this.screenheight - db.clientHeight + this.msgObj.clientHeight) + "px";
			this.scrollToBottom();
			
			//连接websocket后端服务器

            this.socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');

			//this.socket = io.connect('http://' + document.domain + ':' + location.port);

			this.socket.on('connect', function(o){
				//CHAT.send('login', data); // 在on 中 必须调用外面的，不能直接 this.socket.emit  data 必须在外面定义好
				CHAT.login()
				
			});
			

			//this.socket.emit('login',{});

			//告诉服务器端有用户登录
			//this.socket.emit('login', {userid:this.userid, username:this.username,room:this.room});
			
			
			//监听新用户登录
			this.socket.on('login', function(o){
				//this.socket.join(this.room);
				CHAT.updateSysMsg(o, 'login');	
				//alert('login');
			});
			
			//监听用户退出
			this.socket.on('logout', function(o){
				CHAT.updateSysMsg(o, 'logout');
			});
			
			//监听消息发送
			this.socket.on('message_txt', function(obj){
				var isme = (obj.userid == CHAT.userid) ? true : false;
				var contentDiv = '<div>'+obj.content+'</div>';
				var usernameDiv = '<span>'+obj.username+'</span>';
				
				var section = d.createElement('section');
				if(isme){
					section.className = 'user';
					section.innerHTML = contentDiv + usernameDiv;
				} else {
					section.className = 'service';
					section.innerHTML = usernameDiv + contentDiv;
				}
				CHAT.msgObj.appendChild(section);
				CHAT.scrollToBottom();	
			});
			//监听消息发送
			this.socket.on('message_audio', function(obj){
				var isme = (obj.userid == CHAT.userid) ? true : false;

				var fd = new FormData();
				var mp3Name = encodeURIComponent(obj.mp3_name + '.mp3');

				var binaryData = [];
				binaryData.push(obj.content);

				var mp3Blob = new Blob(binaryData, {type: 'audio/mp3'});
				var url = URL.createObjectURL(mp3Blob);

				var contentDiv = '<audio src="'+url+'" controls="controls"></audio>';
				var usernameDiv = '<span>'+obj.username+'</span>';
				
				var section = d.createElement('section');
				if(isme){
					section.className = 'user';
					section.innerHTML = contentDiv + usernameDiv;
				} else {
					section.className = 'service';
					section.innerHTML = usernameDiv + contentDiv;
				}
				CHAT.msgObj.appendChild(section);
				CHAT.scrollToBottom();	
			});



		}
	};
	//通过“回车”提交用户名
	d.getElementById("username").onkeydown = function(e) {
		e = e || event;
		if (e.keyCode === 13) {
			CHAT.usernameSubmit();
		}
	};
	//通过“回车”提交信息
	d.getElementById("content").onkeydown = function(e) {
		e = e || event;
		if (e.keyCode === 13) {
			CHAT.submit();
		}
	};





})();