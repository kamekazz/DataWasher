document.addEventListener('DOMContentLoaded', () => {
  const results = document.getElementById('barcode-results');

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
    const div = document.createElement('div');
    div.textContent = code;
    results.appendChild(div);
  });
});

