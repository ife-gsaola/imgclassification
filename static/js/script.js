(function() {
    var width = 320;
    var height = 0;
    var streaming = false;
    var video = null;
    var canvas = null;
    var photo = null;
    var startbutton = null;
    var cameraDiv = null;
    var outputDiv = null;

    function startup() {
        video = document.getElementById('video');
        canvas = document.getElementById('canvas');
        photo = document.getElementById('photo');
        startbutton = document.getElementById('startbutton');
        cameraDiv = document.getElementById('cameraDiv');
        outputDiv = document.getElementById('outputDiv');

        navigator.mediaDevices.getUserMedia({
            video: true,
            audio: false
        })
        .then(function(stream) {
            video.srcObject = stream;
            video.play();
        })
        .catch(function(err) {
            console.log("An error occurred: " + err);
        });

        video.addEventListener('canplay', function(ev) {
            if (!streaming) {
                height = video.videoHeight / (video.videoWidth / width);

                if (isNaN(height)) {
                    height = width / (4 / 3);
                }

                video.setAttribute('width', width);
                video.setAttribute('height', height);
                canvas.setAttribute('width', width);
                canvas.setAttribute('height', height);
                streaming = true;
            }
        }, false);

        startbutton.addEventListener('click', function(ev) {
            takepicture();
            ev.preventDefault();
        }, false);
    }

    function takepicture() {
        var context = canvas.getContext('2d');
        if (width && height) {
            canvas.width = width;
            canvas.height = height;
            context.drawImage(video, 0, 0, width, height);

            var data = canvas.toDataURL('image/jpeg');
            photo.setAttribute('src', data);

            // Hide camera frame and show captured image frame
            cameraDiv.style.display = 'none';
            outputDiv.style.display = 'block';

            // Close the camera
            closeCamera();

            // Download the photo
            var a = document.createElement('a');
            a.href = data;
            a.download = 'webcam_photo.jpg';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        }
    }

    function closeCamera() {
        // Stop the media stream
        if (video.srcObject) {
            var tracks = video.srcObject.getTracks();
            tracks.forEach(track => {
                track.stop();
            });
            video.srcObject = null;
        }
    }

    window.addEventListener('load', startup, false);
})();
