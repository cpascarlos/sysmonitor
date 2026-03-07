import psutil, subprocess

ram_globale = psutil.virtual_memory().percent
cmd = ["rrdtool", "update", "monitor.rrd", f"N:U:{ram_globale}:U"]
subprocess.run(cmd)