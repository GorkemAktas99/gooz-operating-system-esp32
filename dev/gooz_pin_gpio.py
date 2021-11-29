from machine import Pin
import time
import _thread
import utime
import dev.gooz_thread

exiting_uart_flag = 0

#UART Library
key = ""
value = ""
key_list = []
value_list = []
registered_key = []
registered_value = []
gpio_dic = []
saved_gpio = []
def register(cmd_arr):
    global key
    global value
    global key_list
    global value_list
    global registered_key
    global registered_value
    for i in cmd_arr:
        if i[0] == "-":
            for a in range(1,len(i)):
                if i[a] == "=":
                    break
                key += i[a]
            key_list.append(key)
            door = 0
            for index in range(1,len(i)):
                if i[index] == ")":
                    door = 0
                if door == 1:
                    value += i[index]
                elif i[index] == "(":
                    door = 1
            value_list.append(value)
            key = ""
            value = ""
    registered_key.append(key_list)
    registered_value.append(value_list)
    temp_counter = 0
    gpio_name = ""
    gpio_type = ""
    gpio_in_type = ""
    gpio_pin = ""
    
    
    for pairs in key_list:
        if pairs == "name":
            gpio_name = value_list[temp_counter]
            temp_counter += 1
        elif pairs == "type":
            gpio_type = value_list[temp_counter]
            temp_counter += 1
        elif pairs == "mode":
            gpio_in_type = value_list[temp_counter]
            temp_counter += 1
        elif pairs == "pin":
            gpio_pin = value_list[temp_counter]
            temp_counter += 1
    
    #Saving
    temp = {}
    temp["name"] = gpio_name
    temp["type"] = gpio_type
    temp["mode"] = gpio_in_type
    temp["pin"] = gpio_pin
    saved_gpio.append(temp)
    
    print(saved_gpio)

def gpio_delete(cmd_arr):
    for gpios in saved_gpio:
        if gpios["name"] == cmd_arr[3]:
            saved_gpio.remove(gpios)
#pin gpio write mypin HIGH
def gpio_write(cmd_arr):
    for gpios in saved_gpio:
        if gpios["name"] == cmd_arr[3]:
            gpio_name = gpios["name"]
            gpio_type = gpios["type"]
            gpio_in_type = gpios["mode"]
            gpio_pin = gpios["pin"]
            global type_pin
            global in_type_pin
            global gpio_t
            if gpio_type == "out":
                type_pin = Pin.OUT
            elif gpio_type == "in":
                type_pin = Pin.IN
            elif gpio_type == "alt":
                type_pin = Pin.ALT
            elif gpio_type == "opendrain":
                type_pin = Pin.OPEN_DRAIN
            elif gpio_tpye == "altopendrain":
                type_pin = Pin.ALT_OPEN_DRAIN
            if gpio_in_type == "pullup":
                in_type_pin = Pin.PULL_UP
            elif gpio_in_type == "pulldown":
                in_type_pin = Pin.PULL_DOWN
            try:
                gpio_t = Pin(int(gpio_pin),type_pin,in_type_pin)
            except:
                gpio_t = Pin(int(gpio_pin),type_pin)
            try:
                if cmd_arr[4] == "HIGH":
                    gpio_t.value(1)
                elif cmd_arr[4] == "LOW":
                    gpio_t.value(0)
            except:
                print("Your Pin:"+gpio_name+" didn't work")

def gpio_read(cmd_arr):
    for gpios in saved_gpio:
        if gpios["name"] == cmd_arr[3]:
            gpio_name = gpios["name"]
            gpio_type = gpios["type"]
            gpio_in_type = gpios["mode"]
            gpio_pin = gpios["pin"]
            global type_pin
            global in_type_pin
            global gpio_t
            if gpio_type == "out":
                type_pin = Pin.OUT
            elif gpio_type == "in":
                type_pin = Pin.IN
            elif gpio_type == "alt":
                type_pin = Pin.ALT
            elif gpio_type == "opendrain":
                type_pin = Pin.OPEN_DRAIN
            elif gpio_tpye == "altopendrain":
                type_pin = Pin.ALT_OPEN_DRAIN
            if gpio_in_type == "pullup":
                in_type_pin = Pin.PULL_UP
            elif gpio_in_type == "pulldown":
                in_type_pin = Pin.PULL_DOWN
            try:
                gpio_t = Pin(int(gpio_pin),type_pin,in_type_pin)
            except:
                gpio_t = Pin(int(gpio_pin),type_pin)
            try:
                print(gpio_t.value())
            except:
                print("Your Pin:"+gpio_name+" didn't work")
            
            

            

