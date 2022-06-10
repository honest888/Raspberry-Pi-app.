import json
import os, os.path
import datetime
import subprocess
from time import sleep
from traceback import print_exc
from flask import Flask, request, flash
from flask import jsonify, render_template

import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ''))
try:
    from . import config
    from .jsonFileReader import ConfigFileReader,WPA_Supplicant_Reader
    from . import weather
except:
    import config
    from jsonFileReader import ConfigFileReader,WPA_Supplicant_Reader
    import weather
    pass
     
import json,requests





app = Flask(__name__)
#app.config["DEBUG"] = True
app.config["internal_config"] = config
app.secret_key = 'flasksecretkey'

ORIGINAL_DIR = os.getcwd()
SCRIPT_DIR = os.path.join(ORIGINAL_DIR, config.INPUT_BASE)

def sidebar_run_python_file(file_name): 
    file_path = ConfigFileReader().getMenuPythonFilePath(file_name=file_name)
    if os.path.exists(file_path):
        print((file_path)) 
        try:
            subprocess.Popen(["python", file_path])
        except:
            subprocess.Popen(["python3", file_path])
        #flash('File '+file_name+' run') message won't appear immediately as no page refresh
    return jsonify({})

@app.route("/")
def index():
    config_vars = dict()

    for var in dir(config):
        if not var.startswith("__"):
            config_vars[var] = getattr(config, var)

    # call weather function to get lat lon and weather info
    weather.weatherFunction()

    return render_template("main.html", data=get_data().json, config=config_vars)






@app.route("/sidebar_run_python_file")
def start_sidebar_run_python_file():
    file_name = request.args.get('file_name')
    return sidebar_run_python_file(file_name=file_name)

@app.route("/save_color_value")
def save_color_value():
    base_class = request.args.get('base_class')
    shade1_class = request.args.get('shade1_class')
    shade2_class = request.args.get('shade2_class')
    color_values = {
        'base_class':base_class,
        'shade1_class':shade1_class,
        'shade2_class':shade2_class,
    }
    
    # print(color_values)
    reader = ConfigFileReader()
    reader.setBackgroundColor(new_colors=color_values) 
    return jsonify({})


@app.route("/save_tile_info")
def save_tile_info():
    index = int(request.args.get('index'))-1
    # tile_icon = request.args.get('tile_icon')
    tile_name = request.args.get('tile_name')
    # tile_file_mapping = request.args.get('tile_file_mapping')
    reader = ConfigFileReader()
    tile_icon = reader.getSpecificTileIcon(tile_name)
    reader.setTileIcon(index=index,file_name=tile_icon)
    reader.setTileName(index=index,tile_name=tile_name)
    # reader.setTileMappedPythonFile(index=index,file_name=tile_file_mapping)
    
    # print(index)
    # print(tile_icon)
    # print(tile_file_mapping)
    return jsonify({'tile_icon':tile_icon})

@app.route("/save_total_title_to_display")
def save_total_title_to_display(): 
    total_title_to_display = request.args.get('total_title_to_display') 
    reader = ConfigFileReader()
    reader.setTotalTilesToDisplay(new_count=total_title_to_display) 
    return jsonify({})


@app.route("/save_geo_location_city")
def save_geo_location_city(): 
    city = request.args.get('city') 
    print('city:',city)
    reader = ConfigFileReader()
    reader.set_geo_location_city(city=city) 

    # call weather function to get lat lon and weather info
    weather.weatherFunction()

    return jsonify({})






@app.route("/settings-page")
def settings_page():  
    data = { } 
    reader = ConfigFileReader()
    data['weather_widget_display_status'] = reader.get_weather_widget_display_status() #deleted_item
    data['tilesList'] = reader.getTilesListing()
    data['total_title_to_display'] = reader.getTotalTilesToDisplay()
    data['max_total_title_to_display'] = reader.getMaxTotalTilesToDisplay()
    data['images_list'] = reader.getImagesList()
    data['mapped_python_files'] = reader.getPythonFileListing()
    data['menu_python_files'] = reader.getMenuPythonFiles()
    data['avaliable_tiles'] = reader.getAvaliableTileNames()
    data['tile_colors'] = reader.getTilesBackgroundColorClasses()
    data['all_color_classes'] = reader.getAllColorClasses()
     

    data['paragraph'] = reader.getParagraphText()
    
    data['battery_tile_display_status'] = reader.getBatteryTileDisplayStatus() # deleted_item
    data['display_external_link_icon'] = reader.display_external_link_icon()
    data['email_value'] = reader.getEmail()
    return render_template("settings.html",data = data)

@app.route("/title-page")
def title_page():
    data = { }
    reader = ConfigFileReader()
    data['tile_colors'] = reader.getTilesBackgroundColorClasses()
    data['battery_tile_display_status'] = reader.getBatteryTileDisplayStatus()
    data['battery_types'] = reader.getBatteryTypes()
    data['current_battery_index'] = reader.getCurrentBatteryIndex()
    data['fine_tune'] = reader.getFineTune()
    data['weather_widget_display_status'] = reader.get_weather_widget_display_status()
    return render_template("/title.html", data = data)

@app.route("/add_email")
def add_email():
    email = request.args.get('email')
    reader = ConfigFileReader()
    reader.setEmail(email = email)
    print(email , file=open("../../emailadd.txt", "w"))
    return jsonify({})

@app.route("/wifi-settings-page")
def wifi_settings_page():  
    data = { } 
    reader = ConfigFileReader() 
    data['menu_python_files'] = reader.getMenuPythonFiles()
    data['tile_colors'] = reader.getTilesBackgroundColorClasses()

    data['network_ssids'] = WPA_Supplicant_Reader().getNetworkSSID()
    data['display_external_link_icon'] = reader.display_external_link_icon()
    return render_template("wifi_settings.html",data = data)




@app.route("/set_battery_tile_display_status")
def set_battery_tile_display_status():  
    reader = ConfigFileReader() 
    status = request.args.get('status') 
    reader.setBatteryTileDisplayStatus(status)
    # print(status)
    return jsonify({})

@app.route('/set_battery_type')
def set_battery_types():
    reader = ConfigFileReader()
    battery_type_index = request.args.get('battery_type_index')
    reader.setBatteryType(current_index = battery_type_index)
    return jsonify({})

@app.route('/set_fine_tune')
def set_fine_tune():
    reader = ConfigFileReader()
    fine_tune = request.args.get('fine_tune')
    reader.setFineTune(fine_tune = fine_tune)
    print(fine_tune , file=open("../../scripts/volt_modifier.txt", "w"))
    return jsonify({})

@app.route("/set_weather_widget_display_status")
def set_weather_widget_display_status():  
    reader = ConfigFileReader() 
    status = request.args.get('status') 
    reader.set_weather_widget_display_status(status)
    # print(status)
    return jsonify({})

@app.route("/delete_ssid")
def delete_ssid():  
    print('SSID Deleted, Please Commit Changes')  
    flash('SSID Deleted, Please Commit Changes')
    ssid = request.args.get('ssid') 
    print('ssid:',ssid)
    WPA_Supplicant_Reader().deleteGivenSSID(ssid=ssid)
    return jsonify({})

@app.route("/save_netwrok")
def save_netwrok():
    print('SSID Saved, Please Commit Changes')  
    flash('SSID Saved, Please Commit Changes')
    ssid = request.args.get('ssid') 
    password = request.args.get('password')  
    WPA_Supplicant_Reader().addNewNetwrok(ssid=ssid,password=password)
    return jsonify({})

@app.route("/get_weather_data") 
def get_weather_data():    
    reader = ConfigFileReader()
    weather_data = reader.get_weather_data() 
    return jsonify({'weather_data':weather_data})

@app.route("/get-data") 
def get_data():
    print('get_data')
    data = dict()  
    reader = ConfigFileReader() 
    data['weather_widget_display_status'] = reader.get_weather_widget_display_status()
    data['battery_level'] = get_battery_level().json['battery_level']
    data['battery_color'] = get_battery_level().json['battery_color']
    data['refresh_interval'] = reader.getBatteryRefreshInterval()
    data['menu_python_files'] = reader.getMenuPythonFiles()
    data['tilesList'] = reader.getTilesListing()
    data['total_title_to_display'] = reader.getTotalTilesToDisplay()
    data['tile_colors'] = reader.getTilesBackgroundColorClasses()
    data['battery_tile_display_status'] = reader.getBatteryTileDisplayStatus()
    data['battery_min_max'] = reader.getBatteryMinMax()
    data['battery_flash'] = reader.getBatteryFlashValue()
    data['weather_data_api_key'] = reader.get_weather_data_api_key()
    data['display_external_link_icon'] = reader.display_external_link_icon()
    data["time"] = datetime.datetime.now().strftime("%H:%M") # Passing from the server as Python has better date/time formatting options

    # Temperature and humidity
    data["temp"] = dict()
    fpath = os.path.join(config.INPUT_BASE, config.READ_TEMP)
    if os.path.exists(fpath):
        with open(fpath, "r") as f:
            data["temp"].update(parse_kvs(f.read().split())) # Converts Temp=X Humidity=Y -> {"Temp": "X", "Humidity": "Y"}

    # Battery
    data["battery"] = dict()
    fpath = os.path.join(config.INPUT_BASE, config.READ_BATTERY)
    if os.path.exists(fpath):
        with open(fpath, "r") as f:
            #data["battery"].update(parse_kvs(f.read().split())) # Converts Temp=X Humidity=Y -> {"Temp": "X", "Humidity": "Y"}
            try:
                data["battery"]["volts"] = float(f.read())
                #print('Volts:',data["battery"]["volts"])
            except ValueError:
                print('Error getting volts')

    # Gas
    data["gas"] = dict()
    fpath = os.path.join(config.INPUT_BASE, config.READ_GAS)
    if os.path.exists(fpath):
        with open(fpath, "r") as f:
            #data["gas"].update(parse_kvs(f.read())) # Converts Co2=X Gas=Y -> {"Co2": "X", "Gas": "Y"}
            gas_data = parse_kvs(f.read().splitlines())
            co2_info = gas_data["CO2"].split()
            gas_info = gas_data["Gas"].split()
            data["gas"]["co2_ok"] = co2_info[0] == "Good"
            #data["gas"]["co2_text"] = gas_data["CO2"]
            #data["gas"]["co2_text"] = ("%s" if data["gas"]["co2_ok"] else "! %s !") % co2_info[1]
            data["gas"]["co2_text"] = ("OK %s" % co2_info[1]) if data["gas"]["co2_ok"] else "Detected!!"
            data["gas"]["gas_ok"] = gas_info[0] == "Good"
            #data["gas"]["gas_text"] = gas_data["Gas"]
            data["gas"]["gas_text"] = ("OK %s" % gas_info[1]) if data["gas"]["gas_ok"] else "Detected!!"

    # GPIO states
    data["gpio"] = dict()
    for eid in config.ON_OFF_SCRIPTS:
        fpath = os.path.join(config.GPIO_BASE, "GPIO%d.txt" % config.ON_OFF_SCRIPTS[eid])
        val = get_sensor_info(fpath)
        if val in ("0", "1"):
            data["gpio"][eid] = val == "0" # 0 = on, 1 = off
        else:
            data["gpio"][eid] = val

    # Other measurements
    data["measurements"] = dict()
    for eid in config.SENSORS:
        fpath = os.path.join(config.INPUT_BASE, config.SENSORS[eid])
        
        data["measurements"][eid] = get_sensor_info(fpath)

    # Done
    # print("-"*100)
    # print(data)
    return jsonify(data)

@app.route("/run_mapped_python_file")
def run_mapped_python_file():
    tile_file_mapping = request.args.get('tile_file_mapping') 
    tile_index = int(request.args.get('index')) 
    mapped_file_path = ConfigFileReader().getMappedPythonFilePath(file_path=tile_file_mapping)
    # print(mapped_file_path) 
    stat_folder = ConfigFileReader().getGPIOStatFolderPath()
    stat_file = [os.path.join(stat_folder, x) for x in os.listdir(stat_folder) if str(x).lower().split('.txt')[0] in str(tile_file_mapping).lower()]
    print("-> Running Python File = ",mapped_file_path)
    try:
        subprocess.Popen(["python", mapped_file_path])
    except:
        subprocess.Popen(["python3", mapped_file_path])
        
    state = None
    if stat_file and os.path.exists(stat_file[0]):
        stat_file = stat_file[0] 
        state = int(open(stat_file,'r',encoding="utf-8").read()) 
    ConfigFileReader().set_is_active_tile(index=tile_index,state=state)
    return jsonify({'state':state})




@app.route("/get_tiles_states")
def get_tiles_states():
    stat_folder = ConfigFileReader().getGPIOStatFolderPath()
    data = json.loads(request.args.get('data') )
    
    for id,file_mapping in data.items():
        stat_file = [os.path.join(stat_folder, x) for x in os.listdir(stat_folder) if str(x).lower().split('.txt')[0] in str(file_mapping).lower()]
        if stat_file and os.path.exists(stat_file[0]):
            stat_file = stat_file[0] 
            state = int(open(stat_file,'r',encoding="utf-8").read()) 
            data[id] = state

        
 
    
    
    
    return jsonify({'states':data})




@app.route("/get_battery_level")
def get_battery_level():
    reader = ConfigFileReader()
    battery_level = 0
    battery_color = None
    battery_level_file_path = reader.getBatteryDataFilePath()
    battery_level = open(battery_level_file_path,'r').readlines()[-1].split('->')[-1]
    #print('battery_level a',battery_level)
    battery_level = reader.generateBatteryLevel(float(battery_level))
    print('battery_level b',battery_level)
    battery_color = str(reader.getBatteryColor(level=float(battery_level['percentage'])))
    
    # print("---")
    # print( battery_level )
    return jsonify({'battery_level':battery_level,"battery_color":str(battery_color)})


@app.route("/get_battery_tile_chart_data")
def get_battery_tile_chart_data(): 
    reader = ConfigFileReader()
    data = reader.getChartData()
    return jsonify({'data':data})




@app.route("/wifi_settings_page_run_py_file")
def wifi_settings_page_run_py_file():
    flash('Changes Commited') 
    reader = ConfigFileReader()
    path = reader.get_wifi_settings_page_run_py_file()
    print("-> Running python file = ",path)
    try:
        subprocess.Popen(["python", path])
    except:
        subprocess.Popen(["python3", path])
    return jsonify({})







@app.route("/run-onoff", methods=["POST"])
def run_onoff():
    gpio = int(request.form.get("gpio"))
    fpath = os.path.join(config.INPUT_BASE, "RelayGPIO%d.py" % gpio)

    if os.path.exists(fpath):
        os.chdir(SCRIPT_DIR)
        try:
            #os.system("python3 " + fpath)
            #os.spawnl(os.P_DETACH, "python3 " + fpath)
            subprocess.Popen(["python3", fpath])
            sleep(0.05) # Time for quick scripts to update GPIO pins and other data
        except Exception:
            print_exc()
        os.chdir(ORIGINAL_DIR)

        return get_data()
    else:
        return "Script %r not found" % fpath, 400

@app.route("/run-other", methods=["POST"])
def run_other():
    script = request.form.get("script")
    fpath = os.path.join(config.INPUT_BASE, script)
    if os.path.exists(fpath):
        os.chdir(SCRIPT_DIR)
        try:
            #os.system("python3 " + fpath)
            #os.spawnl(os.P_DETACH, "python3 " + fpath)
            subprocess.Popen(["python3", fpath])
            sleep(0.05) # Time for quick scripts to update GPIO pins and other data
        except Exception:
            print_exc()
        os.chdir(ORIGINAL_DIR)

        return get_data()
    else: 
        print("*** Script %r not found" % fpath)
        return "Script %r not found" % fpath, 400

def parse_kvs(skv):
    out = dict()
    entries = [x for x in skv if x] # Split the file across whitespace and skip any empty ones
                                                            # "Temp=X Humidity=Y" -> ["Temp=X", "Humidity=Y"]

    for entry in entries:
        try:
            kv = entry.split("=") # "Temp=X" -> "Temp", "X"
            out[kv[0]] = kv[1] # Add to our grand list of data
        except Exception:
            print(entry)
            print_exc()

    return out

def get_sensor_info(fpath):
    if os.path.exists(fpath):
        with open(fpath, "r") as f:
            return f.read().strip()
    else:
        return


@app.after_request
def add_header(r):
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers["Cache-Control"] = "public, max-age=0"
    return r


def main():
    app.run(host="localhost", port=3001,debug=True)


if __name__ == "__main__":
    main()
