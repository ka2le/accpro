function onloading(){}

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
var statusCheckTime = 10000;
var counter = 0;

function connectToMaster(){
	masterIP = document.getElementById("masterIP").value;
	checkStatus();
	//setTimeout(function(){ checkStatus(); }, statusCheckTime);
}

function checkStatus(){
	counter++;
	console.log("checkStatus");
	if(!finished){
		setTimeout(function(){ checkStatus(); }, statusCheckTime);
	}

	$.ajax({
		type: "GET",
		url: "http://" + masterIP + ":5000/status",
		success: function(data) {
			if(data=="Complete" || counter == 30){
				finished = true;
			}
			console.log(data+"<data progress>"+progress);
			if(progress == data){
				console.log("Nothing Happened");
			}else{
				var dataArray= data.split("_");
				progress = data;
				if(dataArray[0] = "img"){ 
					$("#step4").append('<br><canvas id="c'+counter+'" width="800" height="600"></canvas>');
					var canvas = document.getElementById("c"+counter);
					var ctx = canvas.getContext("2d");
					var image = new Image();
					var base64String = dataArray[1];
					image.onload = function() {
						ctx.drawImage(this, 0, 0, canvas.width, canvas.height);
					};
					image.src = "data:image/  png;base64,"+base64String;
				}else{
					console.log(data);
					print("Progress: "+data, "k");
					progress = data;
				}
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

	$.ajax({
	type: "GET",
	url: "http://" + masterIP + ":5000/webUIBackend",
	data: {
		startAngle: startAngle,
		endAngle: endAngle,
		nrAngle: nrAngle,
		nodes: nodes,
		levels: levels
	},
	success: function(data) {
		console.log(data);
		//finished = true;
		checkStatus();
		}
	});
}