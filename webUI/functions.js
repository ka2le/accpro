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
function startSimulation(){
	print("Analyzing...", "k");
	document.getElementById("step2").className += " working";
	var startAngle = document.getElementById("startAngle").value;
	var endAngle = document.getElementById("endAngle").value;
	var nrAngle = document.getElementById("nrAngle").value;
	var nodes = document.getElementById("nodes").value;
	var levels = document.getElementById("levels").value;
	print("startAngle: "+ startAngle)
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
