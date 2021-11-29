import os

def register(_name,_val):
    variable_temp = "name "+_name+" "+"value "+_val
    name_txt = "system/config.gooz"
    with open(name_txt,'w',encoding='utf-8') as f:
        f.write(variable_temp)
        f.close()
def getenv(cmd, verbose="0"):
    if verbose == "0":
        counter = 0
        path = "system/config.gooz"
        f = open(path,'r',encoding='utf-8')
        commands = f.readlines()
        f.close()
        print(cmd[3])
    elif verbose == "1":
        print("Variable Name ",cmd[1])
        print("Variable Value")
        print(cmd[3])

def new_register(_name,_val):
    os.putenv(_name,_val)
    
def show(_name):
    print(os.getenv(_name))