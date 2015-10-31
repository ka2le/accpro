var masterIP;

function onloading(){}

function connectToMaster(){
	masterIP = document.getElementById("masterIP").value;
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
		},
	success: function(data) {
			if(data != ""){
				var dataArray= data.split("_");
				if(dataArray[0] == "data"){
					for (i = 1; i < dataArray.length; i++){
						$('#step5').append('<img src="data:image/  png;base64,' + dataArray[i] + '">');
					}
				}
			}else{
				console.log("No data")
			}
		}
	});
}