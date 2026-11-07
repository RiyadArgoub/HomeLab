"""LAN actions for the prototype. Off by default in the GUI.
Remote OFF uses preconfigured OpenSSH and a fixed OS command. Wake sends WOL magic packet.
Do not put credentials, LAN endpoints or private SSH keys into a public repo.
"""
import re
import socket
import subprocess
from pathlib import Path

MAC_RE = re.compile(r'^(?:[0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$')
HOST_RE = re.compile(r'^[A-Za-z0-9.\-:]+$')
USER_RE = re.compile(r'^[A-Za-z_][A-Za-z0-9_.\-]*$')


def wake_on_lan(mac: str, broadcast='255.255.255.255', port=9):
    if not MAC_RE.fullmatch(mac):
        raise ValueError('A real MAC address is required for Wake-on-LAN (AA:BB:CC:DD:EE:FF).')
    raw = bytes.fromhex(mac.replace(':', ''))
    packet = b'\xff' * 6 + raw * 16
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(packet, (broadcast, port))
    return 'WOL packet sent, power-on not yet verified'


def probe_tcp(record: dict, timeout=0.7):
    host = str(record.get('host', '')).strip()
    try:
        port = int(record.get('probe_port', 22))
        if not (1 <= port <= 65535) or not HOST_RE.fullmatch(host):
            return 'UNVERIFIED'
        with socket.create_connection((host, port), timeout=timeout):
            return 'ONLINE'
    except (OSError, ValueError, TypeError):
        return 'UNVERIFIED'  # Closed TCP port does NOT prove machine is off.


def shutdown_over_ssh(record: dict, timeout=12):
    host = str(record.get('host', '')).strip()
    user = str(record.get('ssh_user', '')).strip()
    key = str(record.get('ssh_key', '')).strip()
    platform = str(record.get('platform', 'linux')).lower().strip()
    if not HOST_RE.fullmatch(host) or not USER_RE.fullmatch(user):
        raise ValueError('Set a valid host and ssh_user first.')
    if not key or not Path(key).expanduser().is_file():
        raise ValueError('Configure ssh_key to an existing private key file.')
    if platform == 'linux':
        command = 'sudo -n /usr/bin/systemctl poweroff'
    elif platform == 'windows':
        command = 'shutdown /s /t 0'
    else:
        raise ValueError('Supported platforms: linux, windows with OpenSSH.')
    result = subprocess.run(
        ['ssh', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=5',
         '-o', 'StrictHostKeyChecking=yes', '-i', str(Path(key).expanduser()),
         f'{user}@{host}', command],
        text=True, capture_output=True, timeout=timeout, check=False
    )
    if result.returncode != 0:
        raise RuntimeError((result.stderr or result.stdout or f'SSH exit {result.returncode}').strip()[:250])
    return 'SSH shutdown command accepted; shutdown not yet confirmed'
