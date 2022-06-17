
# Enable the below to make this script power off the Raspberry Pi
import os
os.system("truncate -s 0 ../readings/voltage_graph.txt")
