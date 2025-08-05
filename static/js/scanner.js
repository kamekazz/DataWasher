// Initialize Quagga barcode scanner
const resultInput = document.getElementById('scan-result');
const history = document.getElementById('scan-history');

function addToHistory(code) {
  const div = document.createElement('div');
  div.textContent = code;
  history.prepend(div);
}

Quagga.init({
  inputStream: {
    type: 'LiveStream',
    target: document.querySelector('#interactive'),
    constraints: {
      facingMode: 'environment'
    }
  },
  decoder: {
    readers: [
      'code_128_reader',
      'ean_reader',
      'ean_8_reader',
      'code_39_reader',
      'upc_reader',
      'upc_e_reader',
      'codabar_reader'
    ]
  }
}, function(err) {
  if (err) {
    console.error(err);
    return;
  }
  Quagga.start();
});

Quagga.onDetected(function(data) {
  const code = data.codeResult.code;
  resultInput.value = code;
  addToHistory(code);
});
