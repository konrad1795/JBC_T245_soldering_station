#The MIT License (MIT)
#
# Copyright (c) 2025 Konrad Peter
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import time
from machine import I2C, ADC, Pin, WDT
from SH1106 import SH1106_I2C
import framebuf
import writer
import freesans40
import input_buttons

#pin init

#power stage control output
Control_pin = Pin(20,Pin.OUT)
#soldering iron temperature measurement input
soldering_temp_adc = ADC(0)
#generate button object
input_buttons_obj = input_buttons.input_buttons()
SMPS_FWPM_Pin = Pin(23,Pin.OUT)
SMPS_FWPM_Pin.value(1)

#system constants

#duration of the whole control loop (power phase + measurement phase, should be slightly shorter than needed to wait for ZC
control_loop_duration = 60
#duration of an AC cycle
cycle_duration = 20
#duration between display updates
display_update_time = 500
#absolute duration for temperature measurement start since control loop start
temp_meas_time_start = 45
#duration of temp measurement (each ms one measurement is taken)
temp_meas_time_duration = 5
#duration between button polling
button_polling_time = 10

#PID defs

P_val = 1.65
I_val = 0.01
I_integ = 0

#misc var init

heating_time = 0
calc_control_loop = True
heating_done = False

first_heating_limit = 30

#mean measured temp
temp_mean = 0
#temperature setpoint
set_temp = 370
#variable to store button states
button_pushed_idx = -1

#variable to store if power is switched on or not
POWER_ON = False
first_power_on = True

#display init
WIDTH  = 128                                            # oled display width
HEIGHT = 64                                             # oled display height

i2c = I2C(0, sda = Pin(8), scl = Pin(9))                # Init I2C using I2C0 defaults, SCL=Pin(GP9), SDA=Pin(GP8), freq=400000
oled = SH1106_I2C(WIDTH, HEIGHT, i2c)                   # Init oled display
oled.rotate(True)
font_writer = writer.Writer(oled, freesans40)           #init lib for bigger fonts

#timer inits
curr_time = time.ticks_ms()
time_heater_on = curr_time
time_control_loop = curr_time
time_visualisation = curr_time
time_display_update = curr_time
time_temp_meas = curr_time
time_button_poll = curr_time

#watchdog with 150ms timeout; control loop duration
#wdt = WDT(timeout=150)
#main loop
while True:
    
    curr_time = time.ticks_ms()
    
    if calc_control_loop == True:
        
        #feed watchdog
        #wdt.feed()
        
        #calculate heater on time
        if POWER_ON == True:
            
            #PID calc
            temp_error = set_temp - temp_mean
            
            if temp_error <= 0 and first_power_on == True:
                first_power_on = False
        
            P_res = temp_error * P_val
            I_integ = I_integ + temp_error * I_val
        
            #anti-windup
            if I_integ > 3:
                I_integ = 3
            elif I_integ < 0:
                I_integ = 0
            
            #PID result
            PI_res = P_res + I_integ
        
            
            
            if PI_res <= 0:
               heating_time = 0
            elif PI_res > 40:
                heating_time = 40
                #limit on-time if heating up to lower overshoot
                if first_power_on == True:
                   heating_time = first_heating_limit
                   #print("limited")
            else:
                heating_time = round(PI_res)
                #limit on-time if heating up to lower overshoot
                if first_power_on == True and heating_time > first_heating_limit:
                   heating_time = first_heating_limit
                   #print("limited")
        
            #switch heater on, set timers
            if heating_time > 0:
                #heating off - debug
                Control_pin.value(1)
                pass
            else:
                Control_pin.value(0)
        else:
            heating_time = 0
            first_power_on = True
        #set heater timer
        time_heater_on = time.ticks_ms()
        heating_done = False
        
        #set temp meas timer
        time_temp_meas = time.ticks_ms()
        temp_measured = False
        
        #set control loop timer
        time_control_loop = time.ticks_ms()
        calc_control_loop = False
        
        #print(heating_time)
        #print(first_power_on)
        
        
    #heating time over, heating finished    
    if curr_time - time_heater_on >= heating_time and heating_done == False:
        
        Control_pin.value(0)
        heating_done = True
    
    #temperature measurement time reached
    if curr_time - time_temp_meas >= temp_meas_time_start and temp_measured == False:
        
        #allow the measurement input to settle
        time.sleep(0.005)
        
        #measure mean temperature over several samples
        temp_measurement_sum = 0
        for i in range(temp_meas_time_duration):
            temp_measurement_sum = temp_measurement_sum + soldering_temp_adc.read_u16()
            #time.sleep(0.001)
        
        #temperature scaling; this has to be calibrated!
        temp_mean = ((temp_measurement_sum/temp_meas_time_duration)/65536)*1000*0.6451+20
        #print(temp_mean)
        
        if temp_mean < 0:
            temp_mean = 0
            
        temp_measured = True
    
    #the controll loop is restarted
    if curr_time - time_control_loop >= control_loop_duration:
        
        #check if power is really off, else throw error (pin state cannot be directly checked)
        if heating_done == False or temp_measured == False:
            raise Exception("heater not turned off or temp not measured!")
        else:
            calc_control_loop = True
       
        
    #update display if control loop is finished only to not interveine with heater control
    if curr_time - time_display_update >= display_update_time and calc_control_loop == True:
        
        #visual output power inducator
        if heating_time <= 40:
            power_str = "|" * round(heating_time/5) #sum(power_4_mean) * "|"
        else:
            power_str = "||||||||"
        
        #update display
        oled.fill(0)

        font_writer.set_textpos(5, 10)
        font_writer.printstring(str(int(temp_mean)) + " C")
        oled.text("Power: " + power_str,5,50)
        if POWER_ON == True:
            oled.text("Set: " + str(int(set_temp)) + " C " + "ON",5,0)
        else:
            oled.text("Set: " + str(int(set_temp)) + " C " + "OFF",5,0)
        
        oled.show()
        
        time_display_update = time.ticks_ms()
    
    #read button states
    if curr_time - time_button_poll >= button_polling_time and calc_control_loop == False:
        
        button_pushed_idx = input_buttons_obj.get_button_pushed()
        
        if button_pushed_idx == 0 and set_temp < 430:
            set_temp = set_temp + 10
            #print("up")
        if button_pushed_idx == 2 and set_temp > 60:
            set_temp = set_temp - 10
            #print("down")
        if button_pushed_idx == 1:
            #print("middle")
            if POWER_ON == True:
                POWER_ON = False
            else:
                POWER_ON = True
        
        time_button_poll = time.ticks_ms()
        