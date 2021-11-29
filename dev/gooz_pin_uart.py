from machine import UART,Pin
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
uart_dic = []
saved_uarts = []
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
    uart_name = ""
    uart_baudrate = ""
    uart_rx = ""
    uart_tx = ""
    uart_type = ""
    
    for pairs in key_list:
        if pairs == "name":
            uart_name = value_list[temp_counter]
            temp_counter += 1
        elif pairs == "baudrate":
            uart_baudrate = value_list[temp_counter]
            temp_counter += 1
        elif pairs == "rx":
            uart_rx = value_list[temp_counter]
            temp_counter += 1
        elif pairs == "tx":
            uart_tx = value_list[temp_counter]
            temp_counter += 1
        elif pairs == "type":
            uart_type = value_list[temp_counter]
            temp_counter += 1
    
    #Saving
    temp = {}
    temp["name"] = uart_name
    temp["type"] = uart_type
    temp["baudrate"] = uart_baudrate
    temp["rx"] = uart_rx
    temp["tx"] = uart_tx
    saved_uarts.append(temp)
    
    print(saved_uarts)
    


def uart_dic_converter():
    global uart_dic
    counter = 0
    temp = {"name": "asd","type": "asd","baudrate": "asd", "rx": "asd","tx": "asd"}
    for link in registered_key:
        for i in range(0,len(link)):
            if link[i] == "name":
                temp["name"] = registered_value[counter][i]
            elif link[i] == "baudrate":
                temp["baudrate"] = registered_value[counter][i]
            elif link[i] == "rx":
                temp["rx"] = registered_value[counter][i]
            elif link[i] == "tx":
                temp["tx"] = registered_value[counter][i]
            elif link[i] == "type":
                temp["type"] = registered_value[counter][i]
        counter += 1
        uart_dic.append(temp)
        temp = {"name": "asd","type": "asd","baudrate": "asd", "rx": "asd","tx": "asd"}
                
        
def show_registered_uart():
    uart_dic_converter()
    print(uart_dic)
    
def uart_delete(cmd_arr):
    global uart_dic
    uart_dic_converter()
    for uarts in uart_dic:
        if uarts["name"] == cmd_arr[3]:
            uart_dic.remove(uarts)
            
def write(cmd_arr):
    for uarts in saved_uarts:
        if cmd_arr[3] == uarts["name"]:
            uart_name = uarts["name"]
            uart_type = uarts["type"]
            uart_baudrate = uarts["baudrate"]
            uart_rx = uarts["rx"]
            uart_tx = uarts["tx"]
            uart_t = UART(int(uart_type),baudrate=int(uart_baudrate),tx=Pin(int(uart_tx)),rx=Pin(int(uart_rx)))
            txData = cmd_arr[4]
            uart_t.write(txData)
            time.sleep(0.1)

def listen_thread(uart_type,uart_baudrate,uart_rx,uart_tx):
    uart_t = UART(int(uart_type),baudrate=int(uart_baudrate),tx=Pin(int(uart_tx)),rx=Pin(int(uart_rx)))
    global exiting_uart_flag
    while True:
        rxData = bytes()
        utime.sleep(1)
        while uart_t.any() > 0:
            rxData += uart_t.read(1)
        print(rxData.decode('utf-8'))
        if exiting_uart_flag == 1:
            break
    return 0
        

def listen(cmd_arr):
    global exiting_uart_flag
    if cmd_arr[3] == "stop":
        exiting_uart_flag = 1
        return exiting_uart_flag
    for uarts in saved_uarts:
        if cmd_arr[3] == uarts["name"]:
            uart_name = uarts["name"]
            uart_type = uarts["type"]
            uart_baudrate = uarts["baudrate"]
            uart_rx = uarts["rx"]
            uart_tx = uarts["tx"]
            _thread.start_new_thread(listen_thread,(uart_type,uart_baudrate,uart_rx,uart_tx))

def p2p(cmd_arr):
    for uarts in saved_uarts:
        if cmd_arr[3] == uarts["name"]:
            uart_name = uarts["name"]
            uart_type = uarts["type"]
            uart_baudrate = uarts["baudrate"]
            uart_rx = uarts["rx"]
            uart_tx = uarts["tx"]
            uart_t = UART(int(uart_type),baudrate=int(uart_baudrate),tx=Pin(int(uart_tx)),rx=Pin(int(uart_rx)))
            txData = cmd_arr[4]
            uart_t.write(txData)
            time.sleep(0.1)
            rxData = bytes()
            while uart_t.any() > 0:
                rxData += uart_t.read(1)
            print(rxData.decode('utf-8'))


    