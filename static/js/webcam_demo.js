document.addEventListener('DOMContentLoaded', () => {
  const results = document.getElementById('barcode-results');
  const primaryInput = document.getElementById('primary-barcode-input');
  const video = document.getElementById('video-container');
  const editBtn = document.getElementById('edit-primary-btn');

  let primaryCode = '';
  let lastCode = null;

  // Add your beep sound files here
  const beepGood = new Audio('/static/audio/beep-good.mp3');
  const beepBad = new Audio('/static/audio/beep-bad.mp3');

  const ERROR_THRESHOLD = 0.1;

  const computeAverageError = decodedCodes => {
    const errors = decodedCodes
      .filter(code => code.error !== undefined)
      .map(code => code.error);
    if (!errors.length) {
      return 0;
    }
    return errors.reduce((sum, err) => sum + err, 0) / errors.length;
  };

  // Edit button logic
  editBtn.addEventListener('click', () => {
    primaryInput.removeAttribute('readonly');
    primaryInput.focus();
  });

  primaryInput.addEventListener('change', () => {
    primaryInput.setAttribute('readonly', true);
    primaryCode = primaryInput.value.trim();
    video.classList.remove('border-red-500', 'border-green-500');
    video.classList.add('border-gray-300');
  });

  // Allow live updates, e.g. after clearing the input
  primaryInput.addEventListener('input', () => {
    primaryCode = primaryInput.value.trim();
    if (!primaryCode) {
      video.classList.remove('border-red-500', 'border-green-500');
      video.classList.add('border-gray-300');
    }
  });

  Quagga.init({
    inputStream: {
      type: 'LiveStream',
      target: video,
      constraints: {
        width: 640,
        height: 480,
        facingMode: 'environment'
      }
    },
    decoder: {
      readers: [
        'code_128_reader',
        'ean_reader',
        'ean_8_reader',
        'code_39_reader',
        'code_39_vin_reader',
        'codabar_reader',
        'upc_reader',
        'upc_e_reader',
        'i2of5_reader',
        '2of5_reader',
        'code_93_reader'
      ]
    }
  }, err => {
    if (err) {
      console.error(err);
      return;
    }
    Quagga.start();
  });

  Quagga.onDetected(data => {
    const code = data.codeResult.code;
    const error = computeAverageError(data.codeResult.decodedCodes || []);
    if (error > ERROR_THRESHOLD) {
      return;
    }

    // Only allow "barcode-looking" values: adjust regex as needed
    if (!/^[A-Za-z0-9\-]{6,30}$/.test(code)) {
      return; // Ignore weird scans
    }

    if (code === lastCode) {
      return;
    }
    lastCode = code;
    setTimeout(() => { lastCode = null; }, 2000); // allow rescanning after 2 seconds

    // If no primary code, set it to the first scan
    if (!primaryCode) {
      primaryCode = code;
      primaryInput.value = code;
      primaryInput.setAttribute('readonly', true);
      video.classList.remove('border-red-500', 'border-gray-300');
      video.classList.add('border-green-500');
      beepGood.play();
      return;
    }

    const match = code === primaryCode;

    // Show code in result list
    const div = document.createElement('div');
    div.textContent = code;
    div.className = match ? 'text-green-600' : 'text-red-600';
    results.appendChild(div);

    // Set border color and play beep
    video.classList.remove('border-red-500', 'border-green-500', 'border-gray-300');
    if (match) {
      video.classList.add('border-green-500');
      beepGood.play();
    } else {
      video.classList.add('border-red-500');
      beepBad.play();
    }
  });
});
