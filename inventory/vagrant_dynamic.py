#!/usr/bin/env python3
import sys, json, socket
from concurrent.futures import ThreadPoolExecutor, as_completed

# Rango DHCP de clientes
BASE, START, END = "172.16.1.", 100, 199
clients = [f"{BASE}{i}" for i in range(START, END+1)]

def can_ssh(ip, port=22, timeout=0.5):
    try:
        socket.create_connection((ip, port), timeout).close()
        return True
    except:
        return False

# Escaneo
reachable = []
with ThreadPoolExecutor(max_workers=20) as pool:
    futures = {pool.submit(can_ssh, ip): ip for ip in clients}
    for f in as_completed(futures):
        ip = futures[f]
        if f.result():
            reachable.append(ip)

# Inventario dinámico
inventory = {
    "clients": { "hosts": reachable },
    "_meta": { "hostvars": {} }
}

# Variables para cada cliente (de momento solo funciona con uno)
for ip in reachable:
    inventory["_meta"]["hostvars"][ip] = {
        "ansible_host":               ip,
        "ansible_user":               "vagrant",
        "ansible_python_interpreter": "/usr/bin/python3",
        "ansible_ssh_common_args":    "-o StrictHostKeyChecking=accept-new",
        "ansible_ssh_private_key_file": "/vagrant/.vagrant/machines/client/virtualbox/private_key"
    }

if "--list" in sys.argv:
    print(json.dumps(inventory, indent=2))
elif "--host" in sys.argv:
    tgt = sys.argv[sys.argv.index("--host")+1]
    print(json.dumps(inventory["_meta"]["hostvars"].get(tgt, {}), indent=2))
else:
    print(json.dumps(inventory, indent=2))
