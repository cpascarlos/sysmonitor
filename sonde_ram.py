import psutil

ram_globale = psutil.virtual_memory().percent
print("{ram_globale}")
