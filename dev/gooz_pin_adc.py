import machine
import utime

key = ""
value = ""
key_list = []
value_list = []
registered_key = []
registered_value = []
adc_dic = []
saved_adc = []

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
    print(key_list)
    print(value_list)
    temp_counter = 0
    adc_name = ""
    adc_pin = ""
    for pairs in key_list:
        if pairs == "name":
            adc_name = value_list[temp_counter]
            temp_counter += 1
        elif pairs == "pin":
            adc_pin = value_list[temp_counter]
            temp_counter += 1
    temp = {}
    temp["name"] = adc_name
    temp["pin"] = adc_pin
    saved_adc.append(temp)
    print(saved_adc)

def adc_delete(cmd_arr):
    for adcs in saved_adc:
        if adcs["name"] == cmd_arr[3]:
            saved_adc.remove(adcs)
            
def adc_read(cmd_arr):
    for adcs in saved_adc:
        if adcs["name"] == cmd_arr[3]:
            adc_pin_t = int(adcs["pin"])
            adc_temp = machine.ADC(adc_pin_t)
            try:
                counter_temp = int(cmd_arr[4])
                for i in range(0,counter_temp):
                    reading = adc_temp.read_u16()
                    print(reading)
            except:
                reading = adc_temp.read_u16()
                print(reading)
        else:
            print("ADC pin does not read")