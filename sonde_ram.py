import psutil
import time
from datetime import datetime

while True:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ram_globale = psutil.virtual_memory().percent
    print(f"[{now}] [RAM] Global: {ram_globale}%")
    time.sleep(60)