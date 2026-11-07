Computer Directory Console v0.4 SD-Streamed firmware

Flash:
  firmware/DirectoryConsole/DirectoryConsole.ino

Keeps v0.4 behavior but changes the directory architecture:
- microSD is the primary database
- up to 128 records indexed with only 512 bytes of record offsets
- one computer record is read from SD when needed
- portraits are streamed one row at a time
- microSD init retries 5 times
- built-in five PCs are fallback only

Expected SD wiring:
CS=13, SCK=18, MISO=19, MOSI=23

Serial Monitor: 115200 baud
