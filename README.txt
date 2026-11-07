Computer Directory Console v0.4 SD-first image-rendering fix

This keeps the v0.4 SD-first firmware and replaces only drawAvatar().
The old renderer alternated SD reads and TFT drawPixel calls tens of thousands of times.
The new renderer reads one BMP row at a time and sends the row to the TFT in one operation.

Expected portrait format:
- BMP
- 120 x 120 recommended
- 24-bit RGB
- uncompressed

Serial Monitor: 115200 baud. If a row cannot be read, the firmware prints the exact failed row.
