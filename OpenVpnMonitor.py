from rich.console import Console
from rich.table import Table
import requests
import os
import time

os.system('cls' if os.name == 'nt' else 'clear')
while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    rows = []
    with open("openvpn-status.log", "r") as f:
        log = f.readlines()
        for i in range(3, len(log)):
            if log[i] == 'ROUTING TABLE\n':
                break
            data = log[i].split(',')
            mbytesR = str(round(int(data[2]) / 1048576, 1)) + " Mb"
            mbytesS = str(round(int(data[3]) / 1048576, 1)) + " Mb"
            ip = data[1].split(":")[0]
            result = requests.get("http://ip-api.com/json/" + ip).json()
            rows.append([str(i - 2), data[0], data[1], mbytesR , mbytesS, data[4], f"{result['country']} {result['city']}", result['isp']])
    table = Table(title="VPN Log View")
    columns = ["num", "Name", "IP", "Received", "Sent", "Connected Since", "Location", "ISP"]
    for column in columns:
        table.add_column(column)
    for row in rows:
        table.add_row(*row, style='bright_green')
    console = Console()
    console.print(table)
    time.sleep(10)