import RPi.GPIO as GPIO
import time
from datetime import datetime
import statistics

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 6
SPIMISO = 13
SPIMOSI = 19
SPICS = 26
mq7_apin = 0
Buzzer = 17

#Set Voltage Lists and Varables
Volt_list = []
Volt_read = []



#port init
def init():
         GPIO.setwarnings(False)
         GPIO.cleanup()			#clean up at the end of your script
         GPIO.setmode(GPIO.BCM)		#to specify whilch pin numbering system
         # set up the SPI interface pins
         GPIO.setup(SPIMOSI, GPIO.OUT)
         GPIO.setup(SPIMISO, GPIO.IN)
         GPIO.setup(SPICLK, GPIO.OUT)
         GPIO.setup(SPICS, GPIO.OUT)
         GPIO.setup(Buzzer, GPIO.OUT)

#read SPI data from MCP3008(or MCP3204) chip,8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)	

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1

        GPIO.output(cspin, True)
        
        adcout >>= 1       # first bit is 'null' so drop it
        return adcout
#main ioop
Graph_repeat=120
Read_repeat=5

def main():
         init()

         while True:
                 for x in range(Graph_repeat):
                         #read volt modifier file
                         with open('volt_modifier.txt') as f:
                                 volt_modifier = f.read()

                         for x in range(Read_repeat):
                                Voltage=readadc(mq7_apin, SPICLK, SPIMOSI, SPIMISO, SPICS)
                                VoltageOutput=(Voltage*(3.3/1024)*5.05)
                                Volt_read.append(VoltageOutput) #append volt_read list
                                time.sleep(1)
                         Voltage = statistics.mean(Volt_read) #store average of list
                         Voltage = float(Voltage)+float(volt_modifier)
                         Voltage = (round(Voltage, 1)) #rount to 2 decimal places
                         Volt_read.clear() # clear list
                        
                         Volt_list.append(Voltage) 
                         now = datetime.now()
                         dt_string = now.strftime("%d/%m/%Y %H:%M")
                         print(str(dt_string) + str(' -> ')+ str(Voltage),file=open("../readings/voltage.txt", "w"))
                        
                 Voltage_graph = statistics.mean(Volt_list)
                 Voltage_graph_round=(round(Voltage_graph, 2)) 
                 print(str(dt_string) + str(' -> ')+ str(Voltage_graph_round),file=open("../readings/voltage_graph.txt", "a"))
                 Volt_list.clear()
                 
                 #Alert if voltage is between 1 and 11.5
                 is_between = 1 <= Voltage_graph_round <= 11.5
                 Shall_Alert = is_between
                 if Shall_Alert==True:
                         GPIO.output(Buzzer,GPIO.HIGH)
                         time.sleep(0.3)
                         GPIO.output(Buzzer,GPIO.LOW)
                         time.sleep(0.5)
                         GPIO.output(Buzzer,GPIO.HIGH)
                         time.sleep(0.3)
                         GPIO.output(Buzzer,GPIO.LOW)
                         time.sleep(0.5)
                         GPIO.output(Buzzer,GPIO.HIGH)
                         time.sleep(0.3)
                         GPIO.output(Buzzer,GPIO.LOW)




#file=open("readings/battery.txt", "w")

if __name__ =='__main__':
         try:
                 main()
                 pass
         except KeyboardInterrupt:
                 pass

GPIO.cleanup()
         
         
