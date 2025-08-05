const resultInput = document.getElementById('zxing-result');
const history = document.getElementById('zxing-history');

function addToHistory(code) {
  const div = document.createElement('div');
  div.textContent = code;
  history.prepend(div);
}

const codeReader = new ZXingBrowser.BrowserMultiFormatReader();
codeReader.decodeFromVideoDevice(undefined, 'zxing-video', (result, err) => {
  if (result) {
    const text = result.getText();
    resultInput.value = text;
    addToHistory(text);
  }
});
