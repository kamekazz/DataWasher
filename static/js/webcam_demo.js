const video = document.getElementById('videoInput');
const canvas = document.getElementById('canvasOutput');
const ctx = canvas.getContext('2d');

function onOpenCvReady() {
  navigator.mediaDevices.getUserMedia({ video: true, audio: false })
    .then(stream => {
      video.srcObject = stream;
      video.play();
      requestAnimationFrame(processVideo);
    })
    .catch(err => console.error('getUserMedia() failed:', err));
}

function processVideo() {
  const src = new cv.Mat(video.height, video.width, cv.CV_8UC4);
  const dst = new cv.Mat(video.height, video.width, cv.CV_8UC1);

  ctx.drawImage(video, 0, 0, video.width, video.height);
  src.data.set(ctx.getImageData(0, 0, video.width, video.height).data);

  cv.cvtColor(src, dst, cv.COLOR_RGBA2GRAY);
  cv.imshow('canvasOutput', dst);

  src.delete();
  dst.delete();
  requestAnimationFrame(processVideo);
}

Module = {
  onRuntimeInitialized: onOpenCvReady
};
