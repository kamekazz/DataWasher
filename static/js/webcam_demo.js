document.addEventListener('DOMContentLoaded', () => {
  const results = document.getElementById('barcode-results');
  const primary = document.getElementById('primary-barcode');
  const video = document.getElementById('video-container');
  let primaryCode = null;
  let lastCode = null;

  Quagga.init({
    inputStream: {
      type: 'LiveStream',
      target: document.querySelector('#video-container'),
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
    if (code === lastCode) {
      return;
    }
    lastCode = code;

    if (!primaryCode) {
      primaryCode = code;
      primary.textContent = `Primary Barcode: ${code}`;
      video.classList.remove('border-red-500', 'border-gray-300');
      video.classList.add('border-green-500');
      return;
    }

    const match = code === primaryCode;
    const div = document.createElement('div');
    div.textContent = code;
    div.className = match ? 'text-green-600' : 'text-red-600';
    results.appendChild(div);

    video.classList.remove('border-red-500', 'border-green-500', 'border-gray-300');
    video.classList.add(match ? 'border-green-500' : 'border-red-500');
  });
});

