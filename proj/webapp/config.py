# Folder that contains all subsequent files
INPUT_BASE = "E:/ControlPanel_lite-main/savvyvan"
#INPUT_BASE = "../sample-data"
# Folder for GPIO files
GPIO_BASE = INPUT_BASE + "/GPIOStats"
# How often to update the stats on the website. 1 = every 1 second. 60 = every 60 seconds aka every 1 minute.
UPDATE_INTERVAL = 0.5
# Interval to flash warnings, at in seconds
FLASH_INTERVAL = 0.5

# Script to update the temperature and humidity
UPDATE_TEMP = "TempSensor.py"
# File to read the current temperature and humidity from
READ_TEMP = "readings/CurrentTemp.txt"
# Interval to RUN the temperature and humidity script.
# The current temperature indicator will be updated at the regular UPDATE_INTERVAL as well as at this interval.
# 1 = every 1 second. 60 = every 60 seconds aka every 1 minute.
HUMIDITY_INTERVAL = 5

# File that stores the battery state
READ_BATTERY = "readings/battery.txt"
# Minimum charge for the battery
BATTERY_MIN = 10.5
# Maximum charge for the battery
BATTERY_MAX = 13 # Volts
# Battery voltage to start flashing the text at
# Voltages AT or BELOW this number will cause flashing text.
BATTERY_FLASH = 11.66
# Battery thresholds
# Maps percent thresholds to hexadecimal colors, starting at 100% and going down
BATTERY_THRESHOLDS = [
    #{"percent": 50, "color": "#71cb72"},
    #{"percent": 30, "color": "#f6d756"},
    #{"percent": 0, "color": "#f23a3a"},
    {"measure": 13.00, "percent": 100, "color": "#71cb72"},
    {"measure": 12.75, "percent": 90, "color": "#71cb72"},
    {"measure": 12.50, "percent": 80, "color": "#71cb72"},
    {"measure": 12.30, "percent": 70, "color": "#71cb72"},
    {"measure": 12.15, "percent": 60, "color": "#71cb72"},
    {"measure": 12.05, "percent": 50, "color": "#71cb72"},
    {"measure": 11.95, "percent": 40, "color": "#f6d756"},
    {"measure": 11.81, "percent": 30, "color": "#f6d756"},
    {"measure": 11.66, "percent": 20, "color": "#f23a3a"},
    {"measure": 11.51, "percent": 10, "color": "#f23a3a"},
    {"measure": 11.50, "percent": 0, "color": "#f23a3a"}
]
BATTERY_THRESHOLDS.sort(key=lambda x: x["measure"]) # Ensures the list is sorted properly

# File to read gas information from
READ_GAS = "readings/gas.txt"

# Relay script maps
# These map GPIO pins to buttons on the webpage
# Specifically, the keys are the IDs of the buttons in the HTML, and the values are the pin numbers
# So `"kitchen": 0` would map the kitchen button to RelayGPIO0.py and GPIOStats/GPIO0.txt
# The button names ("kitchen", "fridge", etc) cannot change unless you update the HTML, but you can freely adjust the pin numbers (0, 1, etc).
ON_OFF_SCRIPTS = {
    "kitchen": 26,
    "fridge": 19,
    "usb": 13,
    "heater": 6,
    "lights": 5,
    "inverter": 0,
}

# Sensors
# Relative to INPUT_BASE. So `power.txt` is at `/home/pi/CamperControl/power.txt`
# The exact contents of the file will be displayed as the current status,
# so if the file contains "4.3Amp" that is what will be displayed.
SENSORS = {
    "power": "readings/power.txt",
}

# Other buttons
# You can map buttons by ID to any scripts here
# Relative to INPUT_BASE. So `power-off.py` is at `/home/pi/CamperControl/power-off.py`
OTHER_BUTTONS = {
    "master-power-off": "power-off.py",
}
