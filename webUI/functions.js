
var masterIP;
var statusCheckTime = 10000;
var counter = 0;

function onloading(){}

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

function connectToMaster(){
	masterIP = document.getElementById("masterIP").value;
	checkStatus();
}

function checkStatus(){
	setTimeout(function(){ checkStatus(); }, statusCheckTime);
	$.ajax({
		type: "GET",
		url: "http://" + masterIP + ":5000/status",
		success: function(data) {
			var dataArray= data.split("_");
			if(dataArray[0] == "data"){
				for (i = 1; i < dataArray.length; i++) {
					$("#step5").append('<img id="c'+counter+'" src="data:image/  png;base64,' + dataArray[i] +'">');
					counter++;
				}
			}
		}
	});
}

function test(){
	$.ajax({
		type: "GET",
		url: "http://" + masterIP + ":5000/",
		success: function(data) {
			console.log(data)
				$("#testdiv").innerHTML(data);
		}
	});
}

function startSimulation(){
	print("Analyzing...", "k");
	document.getElementById("step2").className += " working";
	var startAngle = document.getElementById("startAngle").value;
	var endAngle = document.getElementById("endAngle").value;
	var nrAngle = document.getElementById("nrAngle").value;
	var nodes = document.getElementById("nodes").value;
	var levels = document.getElementById("levels").value;
	var maxAngles = document.getElementById("maxAngles").value;

	$.ajax({
	type: "GET",
	url: "http://" + masterIP + ":5000/webUIBackend",
	data: {
		startAngle: startAngle,
		endAngle: endAngle,
		nrAngle: nrAngle,
		nodes: nodes,
		levels: levels,
		maxAngles: maxAngles
	},
	success: function(data) {
		checkStatus();
		}
	});
}