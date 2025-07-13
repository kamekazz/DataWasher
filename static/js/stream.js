document.addEventListener('DOMContentLoaded', () => {
    const img = document.getElementById('stream');
    const startBtn = document.getElementById('startBtn');
    const stopBtn = document.getElementById('stopBtn');
    let source;

    function start() {
        fetch('/start-detection');
        source = new EventSource('/video_feed');
        source.onmessage = (e) => {
            img.src = 'data:image/jpeg;base64,' + e.data;
        };
    }

    function stop() {
        fetch('/stop-detection');
        if (source) {
            source.close();
            source = null;
        }
    }

    startBtn.addEventListener('click', start);
    stopBtn.addEventListener('click', stop);
});
