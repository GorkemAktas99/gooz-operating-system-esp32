import gooz_basic
import dev.gooz_thread
import os

username = "Gorkem"
password = "1234"
login_flag = False

print("Welcome to GoozOS")
usr = input("Username: ")
if usr == username:
    paswd = input("Password: ")
    if paswd == password:
        login_flag = True
    else:
        print("Wrong Password")
else:
    print("User not found")


while(login_flag):
    print(username+"@RPi_Pico:",end="")
    print(os.getcwd(),end=" ")
    msg = input(">> ")
    cmd_list = gooz_basic.command_analyzator(msg)
    gooz_basic.add_run_commands(cmd_list)
    gooz_basic.history.append(cmd_list)

    if cmd_list[0] == "shutdown":
        os.chdir("/")
        print("System will be shutdown")
        dev.gooz_thread.exit_flag = 1
        break
    


