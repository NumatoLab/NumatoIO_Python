#License
#-------
#This code is published and shared by Numato Systems Pvt Ltd under GNU LGPL 
#license with the hope that it may be useful. Read complete license at 
#http://www.gnu.org/licenses/lgpl.html or write to Free Software Foundation,
#51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA
 
#Simplicity and understandability is the primary philosophy followed while
#writing this code. Sometimes at the expence of standard coding practices and
#best practices. It is your responsibility to independantly assess and implement
#coding practices that will satisfy safety and security necessary for your final
#application.
 
#This demo code demonstrates how to set, clear, and read a GPIO and read an analog channel.

'''Prerequisites : Python 3.x , install serial module using pip'''

import serial
 
def send_command(ser_port, command):
    """Send command to the serial port and read the response."""
    ser_port.write(command.encode())
    response = ser_port.read(25).decode()
    return response
 
def main():
    port_name = "COM1"  # Replace with your actual COM port
    baud_rate = 19200
    timeout = 1
 
    try:
        with serial.Serial(port_name, baud_rate, timeout=timeout) as ser_port:
            try: 
                # ADC channel
                adc_channel = 0
                
                if isinstance(adc_channel, int) and 0 <= adc_channel <= 5:
                
                    # Example 1: Read from ADC channel 0
                    adc_command = f"adc read {adc_channel}\r"
                    adc_response = send_command(ser_port, adc_command)
                    adc_value = adc_response[12:-3]
                    print(f"ADC Read {adc_channel} is: {adc_value}")
                    
                else:
                    print(f"Error: adc_channel must be one of the digits between 0 and 5.")
            except Exception as e:
                print(f"Error: adc_channel must be one of the digits between 0 and 5.")
                
            try:
                # GPIO number
                gpio_number = 5

                if isinstance(gpio_number, int) and 0 <= gpio_number <= 7:
                    # Example 2: Set GPIO pin 5
                    gpio_set_command = f"gpio set {gpio_number}\r"
                    send_command(ser_port, gpio_set_command)
                    print(f"GPIO {gpio_number} set successfully.")
             
                    # Example 3: Read GPIO pin 5
                    gpio_read_command = f"gpio read {gpio_number}\r"
                    gpio_response = send_command(ser_port, gpio_read_command)
                    gpio_state = gpio_response[-4:-3]
                    print(f"GPIO {gpio_number} state is: {gpio_state}")
                        
                    # Example 4: Clear GPIO pin 5
                    gpio_clear_command = f"gpio clear {gpio_number}\r"
                    send_command(ser_port, gpio_clear_command)
                    print(f"GPIO {gpio_number} cleared successfully.")
                        
                    # Example 5: Read GPIO pin 5
                    gpio_read_command = f"gpio read {gpio_number}\r"
                    gpio_response = send_command(ser_port, gpio_read_command)
                    gpio_state = gpio_response[-4:-3]
                    print(f"GPIO {gpio_number} state is: {gpio_state}")
                else:
                    print(f"Error: GPIO number must be one of the digits between 0 and 7.")
            except Exception as e:
                print(f"Error: GPIO number must be one of the digits between 0 and 7.")
        
    except serial.SerialException as e:
        print(f"Error opening or communicating with serial port: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
 
if __name__ == "__main__":
    main()
