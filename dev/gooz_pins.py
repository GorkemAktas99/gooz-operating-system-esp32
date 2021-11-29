import dev.gooz_pin_uart
import dev.gooz_pin_adc
import dev.gooz_thread
import dev.gooz_pin_gpio
import _thread
def init(cmd_arr):
    if cmd_arr[1] == "uart":
        if cmd_arr[2] == "show":
            dev.gooz_pin_uart.show_registered_uart()
        elif cmd_arr[2] == "write":
            dev.gooz_pin_uart.write(cmd_arr)
        elif cmd_arr[2] == "listen":
            dev.gooz_pin_uart.listen(cmd_arr)
        elif cmd_arr[2] == "p2p":
            dev.gooz_pin_uart.p2p(cmd_arr)
        elif cmd_arr[2] == "del":
            dev.gooz_pin_uart.uart_delete(cmd_arr)
    elif cmd_arr[1] == "adc":
        if cmd_arr[2] == "read":
            dev.gooz_pin_adc.adc_read(cmd_arr)
    elif cmd_arr[1] == "gpio":
        if cmd_arr[2] == "write":
            dev.gooz_pin_gpio.gpio_write(cmd_arr)
        elif cmd_arr[2] == "read":
            dev.gooz_pin_gpio.gpio_read(cmd_arr)
        
    if cmd_arr[1] == "var":
        if cmd_arr[2] == "uart":
            dev.gooz_pin_uart.register(cmd_arr)
        elif cmd_arr[2] == "adc":
            dev.gooz_pin_adc.register(cmd_arr)
        elif cmd_arr[2] == "gpio":
            dev.gooz_pin_gpio.register(cmd_arr)

