<?php
$startAngle = ($_POST["startAngle"]);
$endAngle = ($_POST["endAngle"]);
$nrAngle = ($_POST["nrAngle"]);
$nodes = ($_POST["nodes"]);
$levels = ($_POST["levels"]);
$masterIP = ($_POST["masterIP"]);
$command = "curl -i http://".$masterIP.":5000/webUIBackend?";
$command = $command."values=".$startAngle."_".$endAngle."_".$nrAngle."_".$nodes."_".$levels; 
$data= exec($command);
echo $data;
?>
