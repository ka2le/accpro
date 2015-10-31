
var masterIP;

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
				console.log(dataArray.toString())
				if(dataArray[0] == "data" && dataArray.length > 0){
					for (i = 1; i < dataArray.length; i++){
						$('#step5').append('<img src="data:image/  png;base64,' + dataArray[i] + '">');
					}
				}
				delete dataArray;
			}else{
				console.log("No data")
			}
		}
	});
}