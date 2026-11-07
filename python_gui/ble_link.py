"""Bleak UART-like BLE transport for Computer Directory Console, fragmented newline protocol.
A background asyncio loop avoids blocking tkinter's UI thread.
"""
import asyncio
import threading

SERVICE_UUID = 'f23a0001-6cf8-4c4c-a3f2-120c95e7ca13'
RX_UUID      = 'f23a0002-6cf8-4c4c-a3f2-120c95e7ca13'  # Python -> ESP32
TX_UUID      = 'f23a0003-6cf8-4c4c-a3f2-120c95e7ca13'  # ESP32 -> Python

class BLELink:
    def __init__(self, on_event):
        self.on_event=on_event
        self.loop=asyncio.new_event_loop()
        self.thread=threading.Thread(target=self._runner,daemon=True)
        self.thread.start()
        self.client=None
        self.buffer=bytearray()
        self.send_lock=None

    def _runner(self):
        asyncio.set_event_loop(self.loop)
        self.send_lock=asyncio.Lock()
        self.loop.run_forever()

    def emit(self, kind, payload):
        self.on_event(kind,payload)

    def run(self, coro):
        return asyncio.run_coroutine_threadsafe(coro,self.loop)

    def connect(self):
        self.run(self._connect())

    async def _connect(self):
        try:
            from bleak import BleakScanner, BleakClient
            self.emit('log','Scanning for DirectoryConsole (up to 10 seconds)...')
            target=await BleakScanner.find_device_by_filter(
                lambda device,ad: device.name=='DirectoryConsole' or
                getattr(ad,'local_name',None)=='DirectoryConsole', timeout=10)
            if not target:
                self.emit('connection',False)
                self.emit('log','ESP32 not found. Check firmware / Bluetooth / permissions.')
                return
            self.client=BleakClient(target,disconnected_callback=lambda _:self.emit('connection',False))
            await self.client.connect(timeout=15)
            await self.client.start_notify(TX_UUID,self._notification)
            self.emit('connection',True)
            self.emit('log','BLE connected to '+str(target.name))
        except Exception as exc:
            self.emit('connection',False)
            self.emit('log',f'BLE connection failed: {exc}')

    def _notification(self, _sender, data):
        self.buffer.extend(data)
        while b'\n' in self.buffer:
            raw, _, rest=self.buffer.partition(b'\n')
            self.buffer=bytearray(rest)
            msg=raw.decode('utf-8','replace').strip()
            if msg:self.emit('received',msg)
        if len(self.buffer)>512:
            self.buffer.clear()
            self.emit('log','BLE message discarded: frame too long')

    def send(self,msg):
        self.run(self._send(msg))

    async def _send(self,msg):
        if not self.client or not self.client.is_connected:
            self.emit('log','BLE not connected. Edit saved locally only.')
            return
        data=(msg.rstrip('\r\n')+'\n').encode('utf-8')
        if len(data)>240:
            self.emit('log','Message too long for ESP32 frame, shorten notes/name.')
            return
        async with self.send_lock:
            try:
                for offset in range(0,len(data),20):
                    await self.client.write_gatt_char(RX_UUID,data[offset:offset+20],response=True)
                    await asyncio.sleep(.01)
            except Exception as exc:
                self.emit('log',f'BLE send failed: {exc}')

    def disconnect(self):
        self.run(self._disconnect())

    async def _disconnect(self):
        if self.client:
            try:await self.client.disconnect()
            except Exception:pass
            self.client=None
        self.emit('connection',False)
