var masterIP;
var statusCheckTime = 10000;
var counter = 0;

function onloading(){}

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
			if(data != ""){
				var dataArray= data.split("_");
				if(dataArray[0] == "data"){
					for (i = 1; i < dataArray.length; i++){
						$('#step5').append('<img id="c' + counter + '" src="data:image/  png;base64,' + dataArray[i] + '">');
						counter++;
					}
				}
			}else{
				console.log("No data")
			}
		}
	});
}

function startSimulation(){
	document.getElementById("step2").className += " working";
	var startAngle = document.getElementById("startAngle").value;
	var endAngle = document.getElementById("endAngle").value;
	var nrAngle = document.getElementById("nrAngle").value;
	var nodes = document.getElementById("nodes").value;
	var levels = document.getElementById("levels").value;
	var maxAngles = document.getElementById("maxAngles").value;

	masterIP = document.getElementById("masterIP").value;

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
		}
	});
}