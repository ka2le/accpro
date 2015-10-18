<?php
$startAngle = ($_POST["startAngle"]);
$endAngle = ($_POST["endAngle"]);
$nrAngle = ($_POST["nrAngle"]);
$nodes = ($_POST["nodes"]);
$levels = ($_POST["levels"]);
$command = "curl -i http://127.0.0.1:5000/webUIBackend?";
$command = $command."values=".$startAngle."_".$endAngle."_".$nrAngle."_".$nodes."_".$levels; 
$data= exec($command);
echo $data;
?>
