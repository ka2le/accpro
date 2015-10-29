function onloading(){

}
function startMaster(){
	print("Starting a VM that will act as a Master...", "k");
	document.getElementById("step1").className += " working";
	setTimeout(function(){
		document.getElementById("checkbox1").checked = true;
		document.getElementById("step1").className = "step finished";
		print("Master has been started successfully")
	}, 2000);
	
}
function startWorkers(){
	print("Starting VM's that will act as a Workers...", "k");
	document.getElementById("step6").className += " working";
	setTimeout(function(){
		document.getElementById("checkbox3").checked = true;
		document.getElementById("step6").className = "step finished";
		print("Workers has been started successfully")
	}, 2000);
	
}
function handleResult(data){
	var text = data.value; //inte exakt såhär men
	print(text);
}
function print(text, type){
	
	var newHtml = document.getElementById("step3").innerHTML;
	if(type== "h"){
		newHtml+='<h3>'+text+'</h3>';
	}else if(type== "k"){
		newHtml+='<h4>'+text+'</h4>';
		
	}else{
		newHtml+='<p>'+text+'</p>';
	}
	
	
	document.getElementById("step3").innerHTML = newHtml;
}

var masterIP;
var progress = "Just Started";
var finished;
var statusCheckTime = 1000;
var counter = 0;
function createImg(i, dataArray){
$("#step4").append('<br><canvas id="c'+counter+'" width="500" height="500"></canvas>');
	var canvas = document.getElementById("c"+counter);
	var ctx = canvas.getContext("2d");
	var image = new Image();
	var base64String = dataArray[i];
	console.log("createing img "+counter);
	image.onload = function() {
		ctx.drawImage(this, 0, 0);
		console.log("created img "+counter);
	};
	image.src = "data:image/  png;base64,"+base64String;
	counter++;	
}
function checkStatus(){
	counter++;
	console.log("checkStatus");
	if(!finished){
		setTimeout(function(){ checkStatus(); }, statusCheckTime);
	}
	$.post("checkStatus.php",{
	masterIP:masterIP
	},function(data){
		if(data=="Complete" || counter == 30){
			finished = true;
		}
		//console.log(data+"<data progress>"+progress);
		if(progress == data){
			console.log("Nothing Happened");
		}else{
			var dataArray= data.split("_");
			progress = data;
			if(dataArray[0] == "img"){ 
				console.log(dataArray);
				for(var i = 1; i< dataArray.length; i++){
					createImg(i, dataArray);
				}
			}else{
				//console.log(data);
				print("Progress: "+data, "k");
				progress = data;
			}
		}
	}); 
}

function startSimulation(){
	print("Analyzing...", "k");
	finished = false;
	document.getElementById("step2").className += " working";
	var startAngle = document.getElementById("startAngle").value;
	var endAngle = document.getElementById("endAngle").value;
	var nrAngle = document.getElementById("nrAngle").value;
	var nodes = document.getElementById("nodes").value;
	var levels = document.getElementById("levels").value;
	masterIP = document.getElementById("masterIP").value;
	setTimeout(function(){ checkStatus(); }, statusCheckTime);
	//print("startAngle: "+ startAngle);
	$.post("flask.php",{
	startAngle:startAngle,
	endAngle:endAngle,
	nrAngle:nrAngle,
	nodes:nodes,
	levels:levels,
	masterIP:masterIP
	},function(data){
		//console.log(data);
		//print("Result: "+data, "h");
	//	finished = true;
		checkStatus();
	});
	/* $.ajax({
            type: "GET",
            url: "http://script/Root" + "/ourApp/",
            contentType: "application/json; charset=utf-8",
            data: { startAngle: startAngle, endAngle:endAngle, nrAngle:nrAngle, nodes:nodes, levels:levels },
            success: function(data) {
                printResults(data);
            }
        });   */   
	
	/* @app.route('/ourApp/', methods=['GET'])
	def ourApp():
		startAngle = {"value": request.args.get('startAngle')}
		#do Stuff
		return result */
}
