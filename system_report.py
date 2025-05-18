import platform 
import psutil

print("System", platform.system())
print("Node Name", platform.node())
print("Release", platform.release())
print("CPU Usage", psutil.cpu_percent(), "%")
print("Memory Usage", psutil.virtual_memory().percent, "%")
