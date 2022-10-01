from rich.console import Console
from rich.table import Table
import os
import requests
import sys 
import time

class Watcher(object):
    running = True
    refresh_delay_secs = 1
    
    def __init__(self, watch_file, call_func_on_change=None, *args, **kwargs):
        self._cached_stamp = 0
        self.filename = watch_file
        self.call_func_on_change = call_func_on_change
        self.args = args
        self.kwargs = kwargs

    def look(self):
        stamp = os.stat(self.filename).st_mtime
        if stamp != self._cached_stamp:
            self._cached_stamp = stamp
            if self.call_func_on_change is not None:
                self.call_func_on_change(*self.args, **self.kwargs)

    def watch(self):
        while self.running: 
            try: 
                time.sleep(self.refresh_delay_secs) 
                self.look() 
            except KeyboardInterrupt: 
                os.system('cls' if os.name == 'nt' else 'clear')
                print('\t-----------------------', '\n\t| Program Was Closed! |\n', '\t-----------------------\n') 
                break 
            except FileNotFoundError:
                os.system('cls' if os.name == 'nt' else 'clear')
                print('\t-----------------------', '\n\t| Log File Not Found! |\n', '\t-----------------------\n')
                break
            except: 
                os.system('cls' if os.name == 'nt' else 'clear')
                print('\t---------------------', '\n\t| Error In Log File! |\n', '\t---------------------\n') 

def getData():
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
            ipContent = requests.get("http://ip-api.com/json/" + ip).json()
            rows.append([str(i - 2), data[0], data[1], mbytesR , mbytesS, data[4], f"{ipContent['country']} {ipContent['city']}", ipContent['isp']])
        f.close()

    table = Table(title="VPN Log View", style='red', header_style='blue')
    columns = ["Num", "Name", "IP", "Received", "Send", "Connected Since", "Location", "ISP"]
    for column in columns:
        table.add_column(column)
    for row in rows:
        table.add_row(*row, style='green', end_section=True)

    console = Console()
    console.print(table)

watch_file = 'openvpn-status.log'

watcher = Watcher(watch_file, getData)
watcher.watch()
