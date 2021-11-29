import sys
import os
import machine
import time
import dev.gooz_pins
import app.edigooz.gooz_text_editor
import dev.cat
import dev.gooz_thread
import app.goozshell.goozshell
import dev.gooz_wlan
import dev.gooz_curl
import app.touch
import system.variables
import app.calculator.calculator

history = []

def command_analyzator(message):
    command_str = ""
    command_array = []
    str_flag = 0
    for i in message:
        if i == "\"":
            if str_flag == 0:
                str_flag = 1
            elif str_flag == 1:
                str_flag = 0
        elif i == " " and str_flag == 0:
            command_array.append(command_str)
            command_str = ""
        else:
            command_str += i
    command_array.append(command_str)
    command_str = ""
    return command_array

def list_function():
    functions = ["print","list","shutdown","doc","history","edigooz","ctrl","help"]
    print("Available functions")
    for i in functions:
        print(i)

def print_function(cmd_array):
    print(cmd_array[1])
    
def add_run_commands(cmd_array):
    if cmd_array[0] == "print":
        if len(cmd_array)<2:
            print("Lack of parameters")
            return 1
        print_function(cmd_array)
    elif cmd_array[0] == "list":
        list_function()
    elif cmd_array[0] == "help":
        print("You can use your Pico with OS")
        print("If you want to learn available functions please type list")
        print("If you want to learn more details about functions please type like")
        print("\t'doc ${function_name}'")
        print("Example 'doc ctrl'")
    elif cmd_array[0] == "history":
        print("----History----")
        str_clean = ""
        for i in history:
            for a in i:
                str_clean += a
                str_clean += " "
            print(str_clean)
            str_clean = ""
    elif cmd_array[0] == "list":
        list_function()
    elif cmd_array[0] == "clear":
        print("\n" * 100)
    elif cmd_array[0] == "mkdir":
        os.mkdir(cmd_array[1])
    elif cmd_array[0] == "pwd":
        print(os.getcwd())
    elif cmd_array[0] == "cd":
        os.chdir(cmd_array[1])
    elif cmd_array[0] == "ls":
        try:
            print(os.listdir(cmd_array[1]))
        except:
            print(os.listdir())
    elif cmd_array[0] == "rm":
        try:
            os.remove(cmd_array[1])
        except:
            print("File couldn't be deleted")
    elif cmd_array[0] == "rmdir":
        try:
            os.rmdir(cmd_array[1])
        except:
            print("Directory couldn't be deleted because folder not empty")
    elif cmd_array[0] == "cat":
        if cmd_array[1][0] == ".":
            break_flag = 0
            str_temp_cat = ""
            pwd = os.getcwd()
            for i in cmd_array[1]:
                if i == "." and break_flag == 0:
                    break_flag = 1
                    continue
                else:
                    str_temp_cat += i
            path = pwd+str_temp_cat
            dev.cat.read(path)
        elif cmd_array[1][0] == "/":
            dev.cat.read(cmd_array[1])
        else:
            pwd = os.getcwd()
            path = pwd+"/"+cmd_array[1]
            dev.cat.read(path)
            
    elif cmd_array[0] == "pin":
        if len(cmd_array)<2:
            print("Lack of parameters")
            return 1
        dev.gooz_pins.init(cmd_array)
    elif cmd_array[0] == "edigooz":
        if len(cmd_array)<2:
            print("Lack of parameters")
            return 1
        if cmd_array[1] == "clean":
            app.edigooz.gooz_text_editor.clean_text()
        elif cmd_array[1] == "ls":
            app.edigooz.gooz_text_editor.show_pages()
        elif cmd_array[1] == "cat":
            try:
                app.edigooz.gooz_text_editor.cat_text(cmd_array)
            except:
                print("This page not found")
        elif cmd_array[1] == "run":
            app.edigooz.gooz_text_editor.text_editor()
        elif cmd_array[1] == "save":
            app.edigooz.gooz_text_editor.save_text_flash(cmd_array[2])
    elif cmd_array[0] == "run":
        if len(cmd_array)<2:
            print("Lack of parameters")
            return 1
        if cmd_array[1] == "stop":
            dev.gooz_thread.exit_flag = 1
            time.sleep(1)
        else:
            print("Running "+ cmd_array[1])
            dev.gooz_thread.start(cmd_array)
    elif cmd_array[0] == "delay":
        time_f = float(cmd_array[1])
        time.sleep(time_f)
    elif cmd_array[0] == "shell":
        if cmd_array[1] == "example":
            app.goozshell.goozshell.example_shell()
        else:
            app.goozshell.goozshell.main(cmd_array[1])
    elif cmd_array[0] == "wifi":
        if cmd_array[1] == "connect":
            dev.gooz_wlan.do_connect(cmd_array[2],cmd_array[3])
        elif cmd_array[1] == "disconnect":
            dev.gooz_wlan.do_disconnect()
        elif cmd_array[1] == "ls":
            dev.gooz_wlan.do_show()
        elif cmd_array[1] == "on":
            dev.gooz_wlan.do_on()
        elif cmd_array[1] == "off":
            dev.gooz_wlan.do_off()
        elif cmd_array[1] == "status":
            dev.gooz_wlan.do_status()
    elif cmd_array[0] == "ifconfig":
        dev.gooz_wlan.ifconfig()
    elif cmd_array[0] == "curl":
        if cmd_array[1] == "json":
            try:
                if cmd_array[3] == ">":
                    temp_response = dev.gooz_curl.get(cmd_array[2],_type="text")
                    app.touch.input_create(cmd_array[4],data=temp_response,_type=".json")
            except:
                temp_response = dev.gooz_curl.get(cmd_array[2],_type="json")
                print(temp_response)
        else:
            temp_response = dev.gooz_curl.get(cmd_array[1])
            try:
                if cmd_array[2] == ">":
                    app.touch.input_create(cmd_array[3],data=temp_response)
            except:
                print(temp_response)
    elif cmd_array[0] == "$":
        if cmd_array[1] == "register":
            system.variables.register(cmd_array[2],cmd_array[3])
        if cmd_array[1] == "show":
            system.variables.show(cmd_array[2])
    elif cmd_array[0] == "calc":
        app.calculator.calculator.calc(cmd_array[1],cmd_array[2],cmd_array[3])
    elif cmd_array[0] == "=":
        value_1=float(cmd_array[1])
        value_2=float(cmd_array[3])
        
        if cmd_array[2]== "+":
            print(value_1 + value_2)
        elif cmd_array[2]== "-":
            print(value_1 - value_2)
        elif cmd_array[2]== "*":
            print(value_1 * value_2)
        elif cmd_array[2]== "/":
            print(value_1 / value_2)
        elif cmd_array[2]== "//":
            print(value_1 // value_2)
        elif cmd_array[2]== "**":
            print(value_1 ** value_2)
        elif cmd_array[2]== "%":
            print(value_1 % value_2)
        else:
            print("Invalid symbol")
    elif cmd_array[0] == "shutdown":
        print(" ")

    else:
        print("This command not found!!")
    