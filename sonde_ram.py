import psutil

ram_globale = psutil.virtual_memory().percent
print(f"{ram_globale}")
