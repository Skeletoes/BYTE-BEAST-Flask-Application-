import psutil

cpu_cores = psutil.cpu_count(logical=True)
cpu_physicalCores = psutil.cpu_count(logical=False)
print(cpu_cores, cpu_physicalCores)