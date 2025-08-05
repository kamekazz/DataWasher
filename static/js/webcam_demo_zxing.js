import { BrowserMultiFormatReader, NotFoundException } from 'https://cdn.jsdelivr.net/npm/@zxing/library@0.19.3/+esm';

const videoContainer = document.getElementById('video-container');
const video = document.getElementById('barcode-video');
const results = document.getElementById('barcode-results');
const primaryInput = document.getElementById('primary-barcode-input');
const editBtn = document.getElementById('edit-primary-btn');

let primaryCode = '';
let lastCode = null;
let lastScanTime = 0;

const beepGood = new Audio('/static/audio/beep-good.mp3');
const beepBad = new Audio('/static/audio/beep-bad.mp3');

// --- Edit button logic ---
editBtn.addEventListener('click', () => {
  primaryInput.removeAttribute('readonly');
  primaryInput.focus();
});

primaryInput.addEventListener('change', () => {
  primaryInput.setAttribute('readonly', true);
  primaryCode = primaryInput.value.trim();
  videoContainer.classList.remove('border-red-500', 'border-green-500');
  videoContainer.classList.add('border-gray-300');
});

primaryInput.addEventListener('input', () => {
  primaryCode = primaryInput.value.trim();
  if (!primaryCode) {
    videoContainer.classList.remove('border-red-500', 'border-green-500');
    videoContainer.classList.add('border-gray-300');
  }
});

// --- ZXing Barcode Scanning ---
const codeReader = new BrowserMultiFormatReader();
codeReader.decodeFromVideoDevice(null, video, (result, err) => {
  if (result) {
    const code = result.getText();
    console.log("ZXing scanned: ", code);
    // Ignore "weird" barcodes
    if (!/^[A-Za-z0-9\-]{6,30}$/.test(code)) return;

    // Avoid double reads within 1.5 seconds
    const now = Date.now();
    if (code === lastCode && now - lastScanTime < 1500) return;
    lastCode = code;
    lastScanTime = now;

    // First scan sets the primary barcode
    if (!primaryCode) {
      primaryCode = code;
      primaryInput.value = code;
      primaryInput.setAttribute('readonly', true);
      videoContainer.classList.remove('border-red-500', 'border-gray-300');
      videoContainer.classList.add('border-green-500');
      beepGood.play();
      return;
    }

    // Compare scanned to primary
    const match = code === primaryCode;
    const div = document.createElement('div');
    div.textContent = code;
    div.className = match ? 'text-green-600' : 'text-red-600';
    results.appendChild(div);

    videoContainer.classList.remove('border-red-500', 'border-green-500', 'border-gray-300');
    if (match) {
      videoContainer.classList.add('border-green-500');
      beepGood.play();
    } else {
      videoContainer.classList.add('border-red-500');
      beepBad.play();
    }
  } else if (err && !(err instanceof NotFoundException)) {
    // Optionally handle other errors here
    // console.error(err);
  }
});
