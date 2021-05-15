import subprocess



subprocess.call(["ifconfig","wlan0","down"])

subprocess.call(["airmon-ng","check","kill"])

subprocess.call(["iwconfig","wlan0","mode","monitor"])

subprocess.call(["ifconfig","wlan0","up"])

subprocess.call(["iwconfig"])