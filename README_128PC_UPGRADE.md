# Computer Directory Console v0.5 - 128 computer upgrade

This build raises the directory limit from 12/20 to 128 computers.

Changes:
- ESP32 firmware: MAX_PC = 128.
- TFT directory scrolls through all records in a 9-row window.
- GUI registry accepts up to 128 records.
- microSD exporter accepts up to 128 records.
- Push All uses SYNCBEGIN/SYNCEND so the ESP32 writes computers.csv once per batch instead of once per record.
- Avatar BMP filenames may be up to 31 characters before .bmp, including bridgette1.bmp.
- GUI computer list now has a vertical scrollbar.

Important: flash the included firmware and use the included Python GUI files together because the batch-sync protocol changed.
