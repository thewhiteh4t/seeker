<?php
header('Content-Type: text/html');
{
  $err_status = $_POST['Status'];
  $err_text = $_POST['Error'];

  $f = fopen('../../logs/result.txt', 'w+');

  $data = array('status' => $err_status, 'error' => $err_text);
  $json_data = json_encode($data);
  fwrite($f, $json_data);
  fclose($f);
}

