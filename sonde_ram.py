import psutil
from datetime import datetime

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
ram_globale = psutil.virtual_memory().percent
print(f"[{now}] [RAM] Global: {ram_globale}%")
