"""Computer Directory Console GUI (prototype).
Run: python python_gui/console_manager.py
Dependencies: pip install -r python_gui/requirements.txt
Live remote commands MUST be explicitly armed for each session.
"""
import json
import queue
import threading
import time
import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox, filedialog

from PIL import Image,ImageTk
from ble_link import BLELink
from remote import wake_on_lan, shutdown_over_ssh, probe_tcp
from media_tools import import_portrait, export_sd_card, avatar_filename

ROOT=Path(__file__).resolve().parents[1]
REGISTRY=ROOT/'assets'/'computers.json'
AVATARS=ROOT/'assets'/'avatars'
COLS=['name','role','host','mac','avatar','status','notes','probe_port','ssh_user','ssh_key','platform']
ALLOWED_STATUS={'ONLINE','UNKNOWN','UNVERIFIED','OFFLINE','WAKE SENT','SIMULATED'}

def load_records(path=REGISTRY):
    data=json.loads(Path(path).read_text(encoding='utf-8'))
    if not isinstance(data,list) or len(data)>20:raise ValueError('Expect list of <=20 computer records')
    return data

def save_records(records,path=REGISTRY):
    Path(path).write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def clean_field(value):
    return str(value).replace('|','/').replace('\n',' ').replace('\r',' ').strip()

def sync_message(index,rec):
    fields=[index,rec.get('name',''),rec.get('role',''),rec.get('host',''),
            rec.get('mac',''),rec.get('avatar',''),rec.get('status','UNKNOWN'),
            rec.get('notes','')]
    line='SYNC|'+'|'.join(clean_field(v) for v in fields)
    if len((line+'\n').encode())>240: raise ValueError('Record too long for BLE, shorten notes')
    return line

class ConsoleGUI:
    def __init__(self,root):
        self.root=root;root.title('Computer Directory Console')
        root.geometry('1130x800');root.minsize(960,680)
        self.records=load_records()
        self.events=queue.Queue()
        self.ble=BLELink(lambda k,v:self.events.put((k,v)))
        self.ble_connected=False
        self.armed=tk.BooleanVar(value=False)
        self.status_auto=tk.BooleanVar(value=False)
        self.photo=None
        self.selected=0
        self.last_probe=0
        self.make_ui()
        self.refresh()
        root.after(100,self.poll_events)
        root.after(1500,self.maybe_probe)
        root.protocol('WM_DELETE_WINDOW',self.on_close)

    def make_ui(self):
        style=ttk.Style()
        if 'clam' in style.theme_names():style.theme_use('clam')
        style.configure('Treeview',rowheight=29,font=('Arial',10))
        style.configure('Header.TLabel',font=('Arial',18,'bold'))
        toolbar=ttk.Frame(self.root,padding=12);toolbar.pack(fill='x')
        ttk.Label(toolbar,text='COMPUTER DIRECTORY',style='Header.TLabel').pack(side='left')
        ttk.Label(toolbar,text='  // NETWORK CONTROL CONSOLE',foreground='#728398').pack(side='left')
        ttk.Button(toolbar,text='Connect Bluetooth',command=self.ble.connect).pack(side='right',padx=4)
        ttk.Button(toolbar,text='Push all to ESP32',command=self.push_all).pack(side='right',padx=4)
        ttk.Button(toolbar,text='Export microSD files',command=self.export_sd).pack(side='right',padx=4)
        self.link=ttk.Label(toolbar,text='BLE disconnected',foreground='#bd4242');self.link.pack(side='right',padx=8)

        top=ttk.Panedwindow(self.root,orient='horizontal');top.pack(fill='both',expand=True,padx=12,pady=4)
        left=ttk.Frame(top);right=ttk.Frame(top);top.add(left,weight=3);top.add(right,weight=2)
        ttk.Label(left,text='Computers',font=('Arial',14,'bold')).pack(anchor='w',pady=(0,6))
        cols=('name','role','host','status')
        self.tree=ttk.Treeview(left,columns=cols,show='headings',selectmode='browse',height=13)
        for c,w in [('name',175),('role',110),('host',155),('status',115)]:
            self.tree.heading(c,text=c.upper());self.tree.column(c,width=w,stretch=True)
        self.tree.pack(fill='both',expand=True)
        self.tree.bind('<<TreeviewSelect>>',self.select_record)
        row=ttk.Frame(left);row.pack(fill='x',pady=8)
        ttk.Button(row,text='Save changes',command=self.save_current).pack(side='left',padx=3)
        ttk.Button(row,text='Push selection',command=self.push_selected).pack(side='left',padx=3)
        ttk.Button(row,text='Probe host',command=self.probe_current).pack(side='left',padx=3)
        ttk.Button(row,text='Wake selected',command=lambda:self.ask_action('WAKE')).pack(side='left',padx=3)
        ttk.Button(row,text='Shutdown selected',command=lambda:self.ask_action('STOP')).pack(side='left',padx=3)
        toggle=ttk.Frame(left);toggle.pack(fill='x',pady=4)
        ttk.Checkbutton(toggle,text='ARM real LAN power commands (this session only)',variable=self.armed).pack(anchor='w')
        ttk.Checkbutton(toggle,text='Probe all hosts every 20 seconds (reachable port ≠ full health)',variable=self.status_auto).pack(anchor='w')
        ttk.Label(left,text='Unarmed mode simulates Wake/Shutdown. Remote STOP requires final GUI confirmation.',foreground='#855a20',wraplength=600).pack(anchor='w',pady=(2,5))

        ttk.Label(right,text='Selected computer',font=('Arial',14,'bold')).pack(anchor='w',pady=(0,6))
        self.img=ttk.Label(right,text='Placeholder portrait');self.img.pack(anchor='center',pady=5)
        ttk.Button(right,text='Choose / replace portrait',command=self.choose_portrait).pack(anchor='center',pady=(0,8))
        form=ttk.Frame(right);form.pack(fill='both',expand=True,padx=5)
        self.fields={}
        for i,key in enumerate(COLS):
            ttk.Label(form,text=key.replace('_',' ').title()+':').grid(row=i,column=0,sticky='w',pady=3)
            entry=ttk.Entry(form,width=40);entry.grid(row=i,column=1,sticky='ew',padx=5,pady=3)
            self.fields[key]=entry
        form.columnconfigure(1,weight=1)

        logbox=ttk.LabelFrame(self.root,text='Event log / BLE / remote actions',padding=5)
        logbox.pack(fill='both',expand=False,padx=12,pady=8)
        self.logtext=tk.Text(logbox,height=7,font=('Consolas',9),state='disabled')
        self.logtext.pack(fill='both',expand=True)
        self.log('Offline editing is ready. Real LAN commands are DISARMED.')
        self.log('Replace placeholder hosts, MACs, SSH settings and character portraits before deployment.')

    def log(self,s):
        self.logtext.configure(state='normal');self.logtext.insert('end',time.strftime('%H:%M:%S')+'  '+s+'\n')
        self.logtext.see('end');self.logtext.configure(state='disabled')

    def refresh(self):
        for item in self.tree.get_children():self.tree.delete(item)
        for i,r in enumerate(self.records):
            self.tree.insert('', 'end',iid=str(i),values=(r.get('name'),r.get('role'),r.get('host'),r.get('status')))
        if self.records:
            self.selected=max(0,min(self.selected,len(self.records)-1))
            self.tree.selection_set(str(self.selected));self.tree.focus(str(self.selected))
            self.populate(self.selected)

    def select_record(self,_event=None):
        selected=self.tree.selection()
        if selected:
            self.selected=int(selected[0]);self.populate(self.selected)

    def populate(self,index):
        r=self.records[index]
        for key,entry in self.fields.items():
            entry.delete(0,'end');entry.insert(0,str(r.get(key,'')))
        avatar=Path(r.get('avatar','')).stem+'.png'
        p=AVATARS/avatar
        if p.is_file():
            im=Image.open(p).convert('RGB');im.thumbnail((170,170))
            self.photo=ImageTk.PhotoImage(im)
            self.img.configure(image=self.photo,text='')
        else:self.img.configure(image='',text='Missing portrait: '+avatar)

    def choose_portrait(self):
        """Import a desktop photo and create both GUI and ESP32 image formats."""
        filename = filedialog.askopenfilename(
            title='Choose a portrait',
            filetypes=[('Image files', '*.png *.jpg *.jpeg *.bmp *.webp *.gif'), ('All files', '*.*')])
        if not filename:
            return
        try:
            # Use existing 8.3 filename (or a safe per-record fallback).
            preferred = self.fields['avatar'].get().strip()
            try:
                target = avatar_filename(preferred)
            except ValueError:
                target = f'pc{self.selected + 1:02}.bmp'
            import_portrait(filename, target, AVATARS)
            self.fields['avatar'].delete(0, 'end')
            self.fields['avatar'].insert(0, target)
            self.save_current()
            self.log(f'Portrait converted to {target}. Export to microSD to update TFT image.')
        except (OSError, ValueError) as exc:
            messagebox.showerror('Portrait import failed', str(exc))

    def export_sd(self):
        """Build microSD files in an output folder. Does not format a card."""
        folder = filedialog.askdirectory(title='Choose a FOLDER for microSD files (card root or staging folder)')
        if not folder:
            return
        try:
            if not self.save_current():
                return
            destination = Path(folder)
            overwrite = [name for name in ('computers.csv',) if (destination / name).exists()]
            if overwrite and not messagebox.askyesno(
                'Overwrite microSD data?',
                'Existing computers.csv will be replaced with your current saved GUI records. Continue?'):
                return
            count, images = export_sd_card(self.records, destination, AVATARS)
            self.log(f'Exported {count} records and {images} BMP image(s) to {destination}')
            messagebox.showinfo('microSD files ready',
                f'Exported computers.csv + {images} BMP image(s) for {count} computer(s).\n'
                'Copy these files to the ROOT of a FAT16/FAT32 microSD card.\n'
                'Bluetooth does not transfer images.')
        except (OSError, ValueError) as exc:
            messagebox.showerror('microSD export failed', str(exc))

    def save_current(self):
        r=self.records[self.selected]
        for key,entry in self.fields.items():
            val=entry.get().strip()
            if key=='probe_port':
                try:val=int(val)
                except ValueError:messagebox.showerror('Invalid port','probe_port must be an integer');return False
            r[key]=val
        save_records(self.records);self.log('Saved local registry: '+r.get('name',''))
        self.refresh()
        return True

    def push_selected(self):
        if not self.save_current():return
        try:self.ble.send(sync_message(self.selected,self.records[self.selected]))
        except ValueError as exc:self.log(str(exc))

    def push_all(self):
        # Save the currently selected form first.
        if not self.save_current():return
        for index,r in enumerate(self.records):
            try:self.ble.send(sync_message(index,r))
            except ValueError as exc:self.log(str(exc))
        self.log('Queued '+str(len(self.records))+' directory entries over BLE.')

    def probe_current(self):
        index=self.selected
        threading.Thread(target=self._probe,args=(index,),daemon=True).start()

    def _probe(self,index):
        status=probe_tcp(self.records[index])
        self.events.put(('probed',(index,status)))

    def maybe_probe(self):
        if self.status_auto.get() and time.monotonic()-self.last_probe>20:
            self.last_probe=time.monotonic()
            for i in range(len(self.records)):
                threading.Thread(target=self._probe,args=(i,),daemon=True).start()
        self.root.after(1500,self.maybe_probe)

    def ask_action(self,action):
        self.dispatch_request(self.selected,action,source='GUI')

    def dispatch_request(self,index,action,source='ESP32'):
        if action not in ('WAKE','STOP'):self.log('Unknown requested action');return
        if index=='ALL':
            if action!='STOP':self.log('ALL is only supported for STOP');return
            targets=list(range(len(self.records)))
        else:
            try:index=int(index)
            except (TypeError,ValueError):return
            if not 0<=index<len(self.records):return
            targets=[index]
        names=', '.join(self.records[i]['name'] for i in targets)
        state='LIVE' if self.armed.get() else 'SIMULATION'
        question=f'{source} requested {action} for {names}.\nMode: {state}\n\nProceed?'
        if not messagebox.askyesno('Confirm power operation',question):
            self.log(f'Cancelled {action} for {names}')
            return
        if not self.armed.get():
            self.log(f'SIMULATION: {action} for {names}. No network power command was sent.')
            self.ble.send(f'ACK|{index}|{action}|SIM')
            return
        for i in targets:
            threading.Thread(target=self._execute,args=(i,action),daemon=True).start()

    def _execute(self,index,action):
        r=self.records[index]
        try:
            if action=='WAKE':
                detail=wake_on_lan(r.get('mac',''))
            else:
                detail=shutdown_over_ssh(r)
            self.events.put(('operation',(index,action,True,detail)))
        except Exception as exc:
            self.events.put(('operation',(index,action,False,str(exc))))

    def poll_events(self):
        try:
            while True:
                kind,payload=self.events.get_nowait()
                if kind=='log':self.log(payload)
                elif kind=='connection':
                    self.ble_connected=payload
                    self.link.configure(text=('BLE connected' if payload else 'BLE disconnected'),foreground=('#168153' if payload else '#bd4242'))
                    if payload:self.ble.send('PING')
                elif kind=='received':self.on_ble_message(payload)
                elif kind=='probed':
                    i,status=payload
                    self.records[i]['status']=status
                    self.log(self.records[i]['name']+' probe: '+status)
                    if self.ble_connected:self.ble.send('STATE|'+str(i)+'|'+status)
                    self.refresh()
                elif kind=='operation':
                    i,action,success,detail=payload
                    self.log(f'{action} {self.records[i]["name"]}: '+('sent' if success else 'FAILED')+' / '+detail)
                    self.ble.send(f'ACK|{i}|{action}|'+('OK' if success else 'FAIL'))
        except queue.Empty:pass
        self.root.after(100,self.poll_events)

    def on_ble_message(self,message):
        self.log('ESP32 > '+message)
        parts=message.split('|')
        if len(parts)==3 and parts[0]=='REQ':
            self.dispatch_request(parts[1],parts[2],source='ESP32')
        elif message=='HELLO':
            self.push_all()

    def on_close(self):
        try:save_records(self.records)
        except Exception:pass
        self.ble.disconnect()
        self.root.destroy()

if __name__=='__main__':
    root=tk.Tk();ConsoleGUI(root);root.mainloop()
