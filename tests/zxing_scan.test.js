const fs = require('fs');
const { PNG } = require('pngjs');
const {
  MultiFormatReader,
  BarcodeFormat,
  DecodeHintType,
  RGBLuminanceSource,
  HybridBinarizer,
  BinaryBitmap
} = require('@zxing/library');

function decode(filename) {
  const buffer = fs.readFileSync(filename);
  const png = PNG.sync.read(buffer);
  const { width, height, data } = png;
  const luminances = new Uint8ClampedArray(width * height);
  for (let i = 0; i < luminances.length; i++) {
    luminances[i] = data[i * 4];
  }
  const luminanceSource = new RGBLuminanceSource(luminances, width, height);
  const binaryBitmap = new BinaryBitmap(new HybridBinarizer(luminanceSource));
  const reader = new MultiFormatReader();
  const hints = new Map();
  hints.set(DecodeHintType.POSSIBLE_FORMATS, [BarcodeFormat.QR_CODE]);
  reader.setHints(hints);
  return reader.decode(binaryBitmap).getText();
}

const result = decode('tests/sample_qr.png');
console.log('ZXing scanned:', result);

if (result !== 'ZXing demo') {
  throw new Error(`Expected "ZXing demo", got "${result}"`);
}
