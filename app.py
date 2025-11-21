from src.scripts.port_forwarding import VirtualServer
import json
import sys

config = {}

try:
    with open("config.json", 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
        print(f"Błąd: Nie znaleziono pliku config.json")
        sys.exit()
except json.JSONDecodeError:
        print(f"Błąd: Plik config.json zawiera błędy składniowe JSON")
        sys.exit()

server = VirtualServer(config["device_ip"], config["username"], config["password"])

current_ports = server.get_all_forwarded_ports()

for rule in current_ports.get("cur_port_forwarding_tbl"):
    if rule.get("remote_port") == config["port_forwarding"]["remote_port"] and rule.get("local_port") == config["port_forwarding"]["local_port"] and rule.get("local_ip") == config["port_forwarding"]["local_ip"]:
        print("Forwarding rule already exists")
        sys.exit()


print("[Device Info Start]")
print(json.dumps(server.send_get({"module": "dev_info"}), indent=4))
print(json.dumps(server.send_get({"module":"port_forwarding"}), indent=4))
print("[Device Info End]")
server.add_port_forwarding(config["port_forwarding"]["local_port"], config["port_forwarding"]["remote_port"], config["port_forwarding"]["local_ip"], config["port_forwarding"]["comment"], config["port_forwarding"]["method"])