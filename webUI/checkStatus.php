<?php
$masterIP = ($_POST["masterIP"]);
$command = "curl -i http://".$masterIP.":5000/status";
$data= exec($command);
echo $data;
//echo "img_12";
?>
