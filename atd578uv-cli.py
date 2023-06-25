import serial
import time
from datetime import date
import threading
import queue

output_queue = queue.Queue()

# Define the serial port settings
port = "COM4"  # Change this to the appropriate serial port
baud_rate = 115200
pollinterval = 1
response = None
ser = None
serial_thread = None

# #Change Freq VFOA
# VFOAFREQ = "14700010"
# #Change Freq VFOB
# VFOBFREQ = "14405000"

# Create a threading event to signal when to stop the thread
stop_event = threading.Event()
ser_stop_event = threading.Event()
pause_event = threading.Event()

def serial_thread_function():
    # Check if serial port is open
    global ser
    if ser is not None and ser.is_open:
        while ser.is_open and not ser_stop_event.is_set():
            if stop_event.is_set():
                break

            if pause_event.is_set():
                time.sleep(0.1)
                continue

            # Send Keep-Alive
            IRP_MJ_WRITE = "2b41444154413a30302c3030310d0a610d0a"
            IRP_MJ_WRITE = bytes.fromhex(IRP_MJ_WRITE)
            ser.write(IRP_MJ_WRITE)
            #print(f"IRP_MJ_WRITE: {IRP_MJ_WRITE.hex()}")

            # Wait for the response
            start_time = time.time()
            while time.time() - start_time < 1:
                if ser.in_waiting > 0:
                    # Read the response
                    response = ser.read(ser.in_waiting)
                    if response is not None:
                        #print(f"IRP_MJ_READ (hex): {response.hex()}")
                        #ascii_response = ''.join(chr(byte) for byte in response)
                        #print(f"IRP_MJ_READ (ascii): {ascii_response}")
                        pass


                time.sleep(0.1)

        # Close the serial port
        ser.close()
        print("Serial port closed")
    else:
        print(f"Failed to connect to {port}")

def serial_connect():
    global ser, response, VFO_mode_status
    
    # Timeout previous connection
    # time.sleep(2.5)

    # Open the serial port
    ser = serial.Serial(port, baud_rate, timeout=1, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
    print(f"{ser}")
    print(f"Connected to {port}")

    # Define the list of hex commands
    startup_commands = [
    ## Standard
    # Check VFO A/B
    #"4100000028000006",
    
    ## COM MODE Startup
    "2b41444154413a30302c3030310d0a610d0a",
    "2b41444154413a30302c3031360d0a0144353738555620434f4d204d4f44450d0a",
    
    #######################
    # "2b41444154413a30302c3030360d0a0402000000000d0a",
    # "2b41444154413a30302c3030360d0a0405000000000d0a",
    # "2b41444154413a30302c3030360d0a0407000000000d0a",
    # "2b41444154413a30302c3030360d0a0409000000000d0a",
    # "2b41444154413a30302c3030360d0a040e000000000d0a",
    # "2b41444154413a30302c3030360d0a0410000000000d0a",
    # "2b41444154413a30302c3030360d0a040a000000000d0a",
    # "2b41444154413a30302c3030360d0a040c000000000d0a",
    # "2b41444154413a30302c3030360d0a0411000000000d0a",
    # "2b41444154413a30302c3030360d0a0412000000000d0a",
    # "2b41444154413a30302c3030360d0a0414000000000d0a",
    # "2b41444154413a30302c3030360d0a0415000000000d0a",
    # "2b41444154413a30302c3030360d0a041b000000000d0a",
    # "2b41444154413a30302c3030360d0a0416000000000d0a",
    # "2b41444154413a30302c3030360d0a0417000000000d0a",
    # "2b41444154413a30302c3030360d0a0418000000000d0a",
    # "2b41444154413a30302c3030360d0a041a000000000d0a",
    # "2b41444154413a30302c3030360d0a041d000000000d0a",
    # "2b41444154413a30302c3030360d0a041e000000000d0a",
    # "2b41444154413a30302c3030360d0a0422000000000d0a",
    # "2b41444154413a30302c3030360d0a0423000000000d0a",
    # "2b41444154413a30302c3030360d0a0424000000000d0a",
    # "2b41444154413a30302c3030360d0a0426000000000d0a",
    # "2b41444154413a30302c3030360d0a0426010000000d0a",
    # "2b41444154413a30302c3030360d0a0426050000000d0a",
    # "2b41444154413a30302c3030360d0a0426060000000d0a",
    # "2b41444154413a30302c3030360d0a0426070000000d0a",
    # "2b41444154413a30302c3030360d0a0429070000000d0a",
    # "2b41444154413a30302c3030360d0a042a070000000d0a",
         
    "2b41444154413a30302c3030360d0a042c070000000d0a",
    "2b41444154413a30302c3030360d0a042d070000000d0a",

    # "2b41444154413a30302c3030360d0a0430070000000d0a",
    # "2b41444154413a30302c3030360d0a0433070000000d0a",
     
    ## guesses
    # "2b41444154413a30302c3030360d0a042b070000000d0a",
    # "2b41444154413a30302c3030360d0a042e070000000d0a",
    # "2b41444154413a30302c3030360d0a042f070000000d0a",
    # "2b41444154413a30302c3030360d0a0420070000000d0a",
    # "2b41444154413a30302c3030360d0a0421070000000d0a",
    # "2b41444154413a30302c3030360d0a0422070000000d0a",
    # "2b41444154413a30302c3030360d0a0424070000000d0a",
    # "2b41444154413a30302c3030360d0a0425070000000d0a",
    # "2b41444154413a30302c3030360d0a0426070000000d0a",
    # "2b41444154413a30302c3030360d0a0427070000000d0a",
    # "2b41444154413a30302c3030360d0a0428070000000d0a",
    # "2b41444154413a30302c3030360d0a0429070000000d0a",
    #######################

    #Completes COM Check
    "2b41444154413a30302c3031340d0a64434f4d20434845434b20454e440d0a",
    "2b41444154413a30302c3030300d0a0d0a",
    ]

    # Iterate startup commands
    for startup_command in startup_commands:
        # Convert the hex string to bytes
        hex_bytes = bytes.fromhex(startup_command.replace(" ", ""))

        # Send the bytes over the serial port
        ser.write(hex_bytes)
        #print(f"Command - hex: {hex_bytes.hex()}")
        #ascii_command = ''.join(chr(byte) for byte in hex_bytes)
        #print(f"Command - ascii: {ascii_command}")
        time.sleep(.1)

        # Wait for 1 second and check for a response
        start_time = time.time()
        while time.time() - start_time < .4:
            if ser.in_waiting > 0:
                # Read the response
                response = ser.read(ser.in_waiting)
                #print(f" Debug 1: {response}")
                if response is not None:
                    # print(f"Response - hex: {response.hex()}")
                    print(f"{response.hex()}")
                    # ascii_response = ''.join(chr(byte) for byte in response)
                    # print(f"Response - ascii: {ascii_response}")
                    # print("Syncing...")
                    
                    #Current VFO
                    # if startup_command == "4100000028000006":
                    #     VFO_mode = response.hex()
                    #     if VFO_mode == "aa53000000000000000010000000000006":
                    #         VFO_mode_status = "VFOA"
                    #         print(f"Current VFO: {VFO_mode_status}")
                    #     if VFO_mode == "aa53000000000000010010000000000006":
                    #         VFO_mode_status = "VFOB"
                    #         print(f"Current VFO: {VFO_mode_status}")

                else:
                    print("No response received")
            time.sleep(.1)
        else:
            if response is None:
                print("Syncing")


def start_serial_thread():
    global serial_thread 
    # Create and start the serial thread
    serial_thread = threading.Thread(target=serial_thread_function)
    serial_thread.daemon = True
    serial_thread.start()
    return serial_thread

#listening = True

def listen_serial_traffic():
    global ser, listening, vfoa_signal
    while listening:
        if ser.in_waiting > 0:
            response = ser.read(ser.in_waiting)
            #Experimental
            if response is not None:
                print(f"Response - hex: {response.hex()}")
                ascii_response = ''.join(chr(byte) for byte in response)
                print(f"Response - ascii: {ascii_response}")
                if response == bytes.fromhex("2b41444154413a30302c3030350d0a03610000640d0a2b41444154413a30302c3031360d0a5a04001a4000ff8b00000000000000420d0a") or response == bytes.fromhex("2b41444154413a30302c3030330d0a5b015c0d0a2b41444154413a30302c3031360d0a5a00041c4004ff8b00000000000100490d0a") or response == bytes.fromhex("2b41444154413a30302c3031360d0a5a00041c4004ff8b00000000000100490d0a2b41444154413a30302c3030330d0a5b015c0d0a2b41444154413a30302c3031360d0a5a00041c4004ff8b00000000000100490d0a"):
                    print("VFOA: Signal Recieved")
                    vfoa_signal = 1
                if response == bytes.fromhex("2b41444154413a30302c3030350d0a03610000640d0a2b41444154413a30302c3031360d0a5a0000184000ff8b000000000000003c0d0a") or response == bytes.fromhex("2b41444154413a30302c3030330d0a5b005b0d0a2b41444154413a30302c3031360d0a5a0000184000ff8b000000000000003c0d0a"):
                    print("VFOA: Signal Stopped")
                    vfoa_signal = 0
                if response == bytes.fromhex("2b41444154413a30302c3030350d0a03610000640d0a2b41444154413a30302c3031360d0a5a04001a4002ff8b00000000000100450d0a") or response == bytes.fromhex("2b41444154413a30302c3030330d0a5b015c0d0a2b41444154413a30302c3031360d0a5a04001a4002ff8b00000000000100450d0a"):
                    print("VFOB: Signal Recieved")
                    vfob_signal = 1
                if response == bytes.fromhex("2b41444154413a30302c3031360d0a5a0000184000ff8b000000000000003c0d0a2b41444154413a30302c3030350d0a03610000640d0a"):
                    print("VFOB: Signal Stopped")
                    vfob_signal = 0
        time.sleep(0.1)

def get_vfo():
    global current_vfo
    pause_event.set() # Pause the serial thread			
    time.sleep(1)			
    get_vfo_command = "2b41444154413a30302c3030360d0a0405000000000d0a"			
    get_vfo_bytes = bytes.fromhex(get_vfo_command)			
    ser.write(get_vfo_bytes)			
    #print(f"Sent command: {get_vfo_command}")			
                
    start_time = time.time()			
    while time.time() - start_time < .2:			
        if ser.in_waiting > 0:		
            # Read the response	
            response = ser.read(ser.in_waiting)	
            if response is not None:	
                #print(f"Response (hex): {response.hex()}")
                # response_ascii = ''.join(chr(byte) for byte in response)
                # print(f"Response (ascii): {response_ascii}")
                get_vfo_response = response.hex()
                get_vfo = get_vfo_response[104:106]
                #print(get_vfo)
                if get_vfo == "00":
                    current_vfo = "VFOA"
                if get_vfo == "01":
                    current_vfo = "VFOB"
                print(f"VFO: {current_vfo}")
                #print("debug 1 - get vfo")
        time.sleep(0.1)	
    pause_event.clear()	

def get_vfoa_power():
    global current_vfoa_power
    pause_event.set() # Pause the serial thread
    time.sleep(.1)
    get_vfoa_power_command = "2b41444154413a30302c3030360d0a042c070000000d0a"
    get_vfoa_power_bytes = bytes.fromhex(get_vfoa_power_command)
    ser.write(get_vfoa_power_bytes)
    # print(f"Sent command: {get_power_command}")
    
    start_time = time.time()
    while time.time() - start_time < .2:
        if ser.in_waiting > 0:
            # Read the response
            response = ser.read(ser.in_waiting)
            if response is not None:
                # print(f"Response (hex): {response.hex()}")
                # response_ascii = ''.join(chr(byte) for byte in response)
                # print(f"Response (ascii): {response_ascii}")
                get_vfoa_power_response = response.hex()
                get_vfoa_power = get_vfoa_power_response[50:52]
                #Different between VFO and Memory
                if get_vfoa_power == "01":
                    current_vfoa_power = "L"
                if get_vfoa_power == "05":
                    current_vfoa_power = "M"
                if get_vfoa_power == "09":
                    current_vfoa_power = "H"
                if get_vfoa_power == "0d":
                    current_vfoa_power = "T"
                if get_vfoa_power == "40":
                    current_vfoa_power = "L"
                if get_vfoa_power == "44":
                    current_vfoa_power = "M"
                if get_vfoa_power == "48":
                    current_vfoa_power = "H"
                if get_vfoa_power == "4c":
                    current_vfoa_power = "T"
                print(f"Power: {current_vfoa_power}")
        time.sleep(0.1)
    pause_event.clear()
    return current_vfoa_power

def get_vfob_power():
    global current_vfob_power
    pause_event.set() # Pause the serial thread
    time.sleep(.1)
    get_vfob_power_command = "2b41444154413a30302c3030360d0a042d070000000d0a"
    get_vfob_power_bytes = bytes.fromhex(get_vfob_power_command)
    ser.write(get_vfob_power_bytes)
    # print(f"Sent command: {get_power_command}")
    
    start_time = time.time()
    while time.time() - start_time < .2:
        if ser.in_waiting > 0:
            # Read the response
            response = ser.read(ser.in_waiting)
            if response is not None:
                # print(f"Response (hex): {response.hex()}")
                # response_ascii = ''.join(chr(byte) for byte in response)
                # print(f"Response (ascii): {response_ascii}")
                get_vfob_power_response = response.hex()
                get_vfob_power = get_vfob_power_response[50:52]
                #Different between VFO and Memory
                if get_vfob_power == "00":
                    current_vfob_power = "L"
                if get_vfob_power == "04":
                    current_vfob_power = "M"
                if get_vfob_power == "08":
                    current_vfob_power = "H"
                if get_vfob_power == "0c":
                    current_vfob_power = "T"
                if get_vfob_power == "80":
                    current_vfob_power = "L"
                if get_vfob_power == "84":
                    current_vfob_power = "M"
                if get_vfob_power == "88":
                    current_vfob_power = "H"
                if get_vfob_power == "8c":
                    current_vfob_power = "T"
                print(f"Power: {current_vfob_power}")
        time.sleep(0.1)
    pause_event.clear()
    return current_vfob_power

def get_zone_a():
    pause_event.set() # Pause the serial thread
    time.sleep(1)
    vfoa_zone_command = "2b41444154413a30302c3030360d0a0429070000000d0a"
    vfoa_zone_bytes = bytes.fromhex(vfoa_zone_command)
    ser.write(vfoa_zone_bytes)
    #print(f"Sent command: {vfoa_zone_command}")
    
    start_time = time.time()
    while time.time() - start_time < 1:
        if ser.in_waiting > 0:
            # Read the response
            response = ser.read(ser.in_waiting)
            if response is not None:
                # print(f"Response (hex): {response.hex()}")
                # response_ascii = ''.join(chr(byte) for byte in response)
                # print(f"Response (ascii): {response_ascii}")
                vfoa_z = response.hex()
                vfoa_zone = vfoa_z[34:98]
                vfoa_zone_ascii = bytes.fromhex(vfoa_zone).decode('ascii')
                print(f"VFOA Zone: {vfoa_zone_ascii}")
                current_vfoa_zone = vfoa_zone_ascii

        time.sleep(0.1)
    pause_event.clear()
    return current_vfoa_zone

def get_freq_a():
    pause_event.set() # Pause the serial thread
    time.sleep(1)
    vfoa_freq_command = "2b41444154413a30302c3030360d0a042c070000000d0a"
    vfoa_freq_bytes = bytes.fromhex(vfoa_freq_command)
    ser.write(vfoa_freq_bytes)
    #print(f"Sent command: {vfoa_freq_command}")
    
    start_time = time.time()
    while time.time() - start_time < 1:
        if ser.in_waiting > 0:
            # Read the response
            response = ser.read(ser.in_waiting)
            if response is not None:
                # print(f"Response (hex): {response.hex()}")
                # response_ascii = ''.join(chr(byte) for byte in response)
                # print(f"Response (ascii): {response_ascii}")
                VFOA_freq = response.hex()
                VFOA_mhz = VFOA_freq[34:37]
                VFOA_hz = VFOA_freq[37:42]
                print(f"VFOA: {VFOA_mhz}.{VFOA_hz} MHz")
        time.sleep(0.1)
    pause_event.clear()

def get_channel_a():
    pause_event.set() # Pause the serial thread
    time.sleep(1)
    vfoa_channel_command = "2b41444154413a30302c3030360d0a042c070000000d0a"
    vfoa_channel_bytes = bytes.fromhex(vfoa_channel_command)
    ser.write(vfoa_channel_bytes)
    #print(f"Sent command: {vfoa_channel_command}")
    
    start_time = time.time()
    while time.time() - start_time < .2:
        if ser.in_waiting > -1:
            # Read the response
            response = ser.read(ser.in_waiting)
            if response is not None:
                # print(f"Response (hex): {response.hex()}")
                # response_ascii = ''.join(chr(byte) for byte in response)
                # print(f"Response (ascii): {response_ascii}")
                VFOA_chan = response
                VFOA_channel = VFOA_chan[52:68]
                VFOA_channel = VFOA_channel.decode()
                #print(f"VFO A Channel: {VFOA_channel}")
                if len(VFOA_channel) > 0:
                    print(f"VFO A Channel: {VFOA_channel}")
        time.sleep(0.1)
    pause_event.clear()

def get_zone_b():
    pause_event.set() # Pause the serial thread
    time.sleep(1)
    vfob_zone_command = "2b41444154413a30302c3030360d0a042a070000000d0a"
    vfob_zone_bytes = bytes.fromhex(vfob_zone_command)
    ser.write(vfob_zone_bytes)
    #print(f"Sent command: {vfob_zone_command}")

    start_time = time.time()
    while time.time() - start_time < 1:
        if ser.in_waiting > 0:
            # Read the response
            response = ser.read(ser.in_waiting)
            if response is not None:
                # print(f"Response (hex): {response.hex()}")
                # response_ascii = ''.join(chr(byte) for byte in response)
                # print(f"Response (ascii): {response_ascii}")
                vfob_z = response.hex()
                vfob_zone = vfob_z[34:98]
                vfob_zone_ascii = bytes.fromhex(vfob_zone).decode('ascii')
                print(f"VFOA Zone: {vfob_zone_ascii}")

        time.sleep(0.1)
    pause_event.clear()

def get_freq_b():
    pause_event.set() # Pause the serial thread
    time.sleep(1)
    vfob_freq_command = "2b41444154413a30302c3030360d0a042d070000000d0a"
    vfob_freq_bytes = bytes.fromhex(vfob_freq_command)
    ser.write(vfob_freq_bytes)
    #print(f"Sent command: {vfob_freq_command}")
    
    start_time = time.time()
    while time.time() - start_time < .5:
        if ser.in_waiting > 0:
            # Read the response
            response = ser.read(ser.in_waiting)
            if response is not None:
                # print(f"Response (hex): {response.hex()}")
                # response_ascii = ''.join(chr(byte) for byte in response)
                # print(f"Response (ascii): {response_ascii}")
                VFOB_freq = response.hex()
                VFOB_mhz = VFOB_freq[34:37]
                VFOB_hz = VFOB_freq[37:42]
                print(f"VFOB: {VFOB_mhz}.{VFOB_hz} MHz")
        time.sleep(0.1)
    pause_event.clear()

def get_channel_b():
    pause_event.set() # Pause the serial thread
    time.sleep(1)
    vfob_channel_command = "2b41444154413a30302c3030360d0a042d070000000d0a"
    vfob_channel_bytes = bytes.fromhex(vfob_channel_command)
    ser.write(vfob_channel_bytes)
    #print(f"Sent command: {vfob_channel_command}")
    
    start_time = time.time()
    while time.time() - start_time < .2:
        if ser.in_waiting > -1:
            # Read the response
            response = ser.read(ser.in_waiting)
            if response is not None:
                # print(f"Response (hex): {response.hex()}")
                # response_ascii = ''.join(chr(byte) for byte in response)
                # print(f"Response (ascii): {response_ascii}")
                VFOB_chan = response
                VFOB_channel = VFOB_chan[52:68]
                VFOB_channel = VFOB_channel.decode()
                if len(VFOB_channel) > 0:
                    print(f"VFO B Channel: {VFOB_channel}")
        time.sleep(0.1)
    pause_event.clear()

def get_gps_loc():
    pause_event.set() # Pause the serial thread							
    time.sleep(1)							
    get_gps_loc_command = "2b41444154413a30302c3030360d0a0452070000000d0a"							
    get_gps_loc_bytes = bytes.fromhex(get_gps_loc_command)							
    ser.write(get_gps_loc_bytes)							
    #print(f"Sent command: {get_gps_loc_command}")							
                                
    start_time = time.time()							
    while time.time() - start_time < .1:							
        if ser.in_waiting > 0:						
            # Read the response					
            response = ser.read(ser.in_waiting)					
            if response is not None:					
                # print(f"Response (hex): {response.hex()}")				
                # response_ascii = ''.join(chr(byte) for byte in response)				
                # print(f"Response (ascii): {response_ascii}")				
                get_gps_lat_response = response				
                get_gps_lat = get_gps_lat_response[17:27]				
                get_gps_lat = get_gps_lat.decode()				
                get_gps_long_response = response				
                get_gps_long = get_gps_long_response[32:46]				
                get_gps_long = get_gps_long.decode()				
                print(f"GPS location: {get_gps_lat} {get_gps_long}")		
            time.sleep(0.1)					
        pause_event.clear()

def get_gps_lat():
    pause_event.set() # Pause the serial thread							
    time.sleep(1)							
    get_gps_lat_command = "2b41444154413a30302c3030360d0a0452070000000d0a"							
    get_gps_lat_bytes = bytes.fromhex(get_gps_lat_command)							
    ser.write(get_gps_lat_bytes)							
    #print(f"Sent command: {get_gps_lat_command}")
                                
    start_time = time.time()							
    while time.time() - start_time < .1:							
        if ser.in_waiting > 0:						
            # Read the response					
            response = ser.read(ser.in_waiting)					
            if response is not None:					
                # print(f"Response (hex): {response.hex()}")				
                # response_ascii = ''.join(chr(byte) for byte in response)				
                # print(f"Response (ascii): {response_ascii}")				
                get_gps_lat_response = response				
                get_gps_lat = get_gps_lat_response[17:27]				
                get_gps_lat = get_gps_lat.decode()				
                print(f"GPS lat: {get_gps_lat}")				
            time.sleep(0.1)					
        pause_event.clear()

def get_gps_long():
    pause_event.set() # Pause the serial thread							
    time.sleep(1)							
    get_gps_long_command = "2b41444154413a30302c3030360d0a0452070000000d0a"							
    get_gps_long_bytes = bytes.fromhex(get_gps_long_command)							
    ser.write(get_gps_long_bytes)							
    #print(f"Sent command: {get_gps_long_command}")							
                                
    start_time = time.time()							
    while time.time() - start_time < .1:							
        if ser.in_waiting > 0:						
            # Read the response					
            response = ser.read(ser.in_waiting)					
            if response is not None:					
                # print(f"Response (hex): {response.hex()}")				
                # response_ascii = ''.join(chr(byte) for byte in response)				
                # print(f"Response (ascii): {response_ascii}")				
                get_gps_long_response = response				
                get_gps_long = get_gps_long_response[32:46]				
                get_gps_long = get_gps_long.decode()				
                print(f"GPS long: {get_gps_long}")		
            time.sleep(0.1)					
        pause_event.clear()

def get_gps_vel():
    pause_event.set() # Pause the serial thread			
    time.sleep(1)			
    get_gps_vel_command = "2b41444154413a30302c3030360d0a0452070000000d0a"			
    get_gps_vel_bytes = bytes.fromhex(get_gps_vel_command)			
    ser.write(get_gps_vel_bytes)			
    #print(f"Sent command: {get_gps_vel_command}")			
                
    start_time = time.time()			
    while time.time() - start_time < .1:			
        if ser.in_waiting > 0:		
            # Read the response	
            response = ser.read(ser.in_waiting)	
            if response is not None:	
                # print(f"Response (hex): {response.hex()}")
                # response_ascii = ''.join(chr(byte) for byte in response)
                # print(f"Response (ascii): {response_ascii}")
                get_gps_vel_response = response
                get_gps_vel = get_gps_vel_response[47:56]
                get_gps_vel = get_gps_vel.decode()
                print(f"GPS {get_gps_vel}")
            time.sleep(0.1)	
        pause_event.clear()

def get_gps_alt():
    pause_event.set() # Pause the serial thread			
    time.sleep(1)			
    get_gps_alt_command = "2b41444154413a30302c3030360d0a0452070000000d0a"			
    get_gps_alt_bytes = bytes.fromhex(get_gps_alt_command)			
    ser.write(get_gps_alt_bytes)			
    #print(f"Sent command: {get_gps_alt_command}")			
                
    start_time = time.time()			
    while time.time() - start_time < 1:			
        if ser.in_waiting > -1:		
            # Read the response	
            response = ser.read(ser.in_waiting)	
            if response is not None:	
                # print(f"Response (hex): {response.hex()}")
                # response_ascii = ''.join(chr(byte) for byte in response)
                # print(f"Response (ascii): {response_ascii}")
                get_gps_alt_response = response
                get_gps_alt = get_gps_alt_response[56:79]
                get_gps_alt = get_gps_alt.decode()
                if "ft" in get_gps_alt:
                    print(f"GPS Alt: {get_gps_alt}")
                else:
                    pass
            time.sleep(0.1)	
        pause_event.clear()		

def get_gps_date():
    pause_event.set() # Pause the serial thread			
    time.sleep(1)			
    get_gps_date_command = "2b41444154413a30302c3030360d0a0452070000000d0a"			
    get_gps_date_bytes = bytes.fromhex(get_gps_date_command)			
    ser.write(get_gps_date_bytes)			
    #print(f"Sent command: {get_gps_date_command}")			
                
    start_time = time.time()			
    while time.time() - start_time < .2:			
        if ser.in_waiting > -1:		
            # Read the response	
            response = ser.read(ser.in_waiting)	
            if response is not None:	
                # print(f"Response (hex): {response.hex()}")
                # response_ascii = ''.join(chr(byte) for byte in response)
                # print(f"Response (ascii): {response_ascii}")
                get_gps_date_response = response
                get_gps_date = get_gps_date_response[82:90]
                get_gps_date = get_gps_date.decode()
                if len(get_gps_date) > 5:
                    print(f"GPS Date: 20{get_gps_date}")
            time.sleep(0.1)	
        pause_event.clear()		

def get_gps_time():
    pause_event.set() # Pause the serial thread			
    time.sleep(1)			
    get_gps_time_command = "2b41444154413a30302c3030360d0a0452070000000d0a"			
    get_gps_time_bytes = bytes.fromhex(get_gps_time_command)			
    ser.write(get_gps_time_bytes)			
    #print(f"Sent command: {get_gps_time_command}")			
                
    start_time = time.time()			
    while time.time() - start_time < .2:			
        if ser.in_waiting > -1:		
            # Read the response	
            response = ser.read(ser.in_waiting)	
            if response is not None:	
                # print(f"Response (hex): {response.hex()}")
                # response_ascii = ''.join(chr(byte) for byte in response)
                # print(f"Response (ascii): {response_ascii}")
                get_gps_time_response = response
                get_gps_time = get_gps_time_response[92:100]
                get_gps_time = get_gps_time.decode()
                if len(get_gps_time) > 5:
                    print(f"GPS Time: {get_gps_time} UTC")
            time.sleep(0.1)	
        pause_event.clear()		

def set_vfo_a():
    global current_vfo
    get_vfo()
    #time.sleep(1)
    if current_vfo == "VFOA":
        #print (f"VFO bypass: {current_vfo}")
        pass
    else:
        pause_event.set()  # Pause the serial thread
        #time.sleep(.1)

        set_vfo_a_commands = [
        "2b41444154413a30302c3032330d0a081900881f00207102000851060008450400084d0600080d0a",
        "2b41444154413a30302c3030360d0a045a070000000d0a",
        "2b41444154413a30302c3030360d0a045e070000000d0a",
        ]

        for command in set_vfo_a_commands:
            set_vfo_a_bytes = bytes.fromhex(command)
            ser.write(set_vfo_a_bytes)
            #print(f"Sent command: {command}")

            start_time = time.time()
            while time.time() - start_time < .2:
                if ser.in_waiting > 0:
                    # Read the response
                    response = ser.read(ser.in_waiting)
                    if response is not None:
                        # print(f"Response (hex): {response.hex()}")
                        # response_ascii = ''.join(chr(byte) for byte in response)
                        # print(f"Response (ascii): {response_ascii}")
                        pass
        pause_event.clear()
        time.sleep(0.1)
        get_vfo()
    #print("debug 2 - set vfo")

def set_vfo_b():
    global current_vfo
    get_vfo()
    #time.sleep(.1)
    #print("debug 1 - set vfo")
    if current_vfo == "VFOB":
        #print (f"VFO: {current_vfo}")
        pass
    else:
        pause_event.set()  # Pause the serial thread
        #time.sleep(.1)

        set_vfo_b_commands = [
        "2b41444154413a30302c3032330d0a081901881f00207102000851060008450400084d0600080d0a",
        "2b41444154413a30302c3030360d0a045a070000000d0a",
        "2b41444154413a30302c3030360d0a045e070000000d0a",
        ]

        for command in set_vfo_b_commands:
            set_vfo_b_bytes = bytes.fromhex(command)
            ser.write(set_vfo_b_bytes)
            #print(f"Sent command: {command}")

            start_time = time.time()
            while time.time() - start_time < .2:
                if ser.in_waiting > 0:
                    # Read the response
                    response = ser.read(ser.in_waiting)
                    if response is not None:
                        # print(f"Response (hex): {response.hex()}")
                        # response_ascii = ''.join(chr(byte) for byte in response)
                        # print(f"Response (ascii): {response_ascii}")
                        pass
        pause_event.clear()
        time.sleep(0.1)
        get_vfo()
    #print("debug 2 - set vfo")

def set_vfo_a_vfo():
    set_vfo_a()
    pause_event.set()  # Pause the serial thread
    # time.sleep(1)

    set_vfo_a_vfo_commands = [
    ##Switch VFOA VFO/M(VFO)
    "2b41444154413a30302c3134350d0a573d010000881f00207102000851060008450400084d06000859030008e10c000800000000000000000000000000000000870b00080d04000800000000d5090008f90b00088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200080d0a",
    "2b41444154413a30302c3030360d0a042c010000000d0a",
    ]

    for command in set_vfo_a_vfo_commands:
        set_vfo_a_vfo_bytes = bytes.fromhex(command)
        ser.write(set_vfo_a_vfo_bytes)
        #print(f"Sent command: {command}")

        start_time = time.time()
        while time.time() - start_time < .1:
            if ser.in_waiting > 0:
                # Read the response
                response = ser.read(ser.in_waiting)
                if response is not None:
                    # print(f"Response (hex): {response.hex()}")
                    # response_ascii = ''.join(chr(byte) for byte in response)
                    # print(f"Response (ascii): {response_ascii}")
                    pass
                time.sleep(0.1)
        pause_event.clear()
    set_vfo_a_vfo_status = "VFO"
    print (f"VFOA VFO/MEM: {set_vfo_a_vfo_status}")
    

def set_vfo_a_mem():
    set_vfo_a()
    pause_event.set()  # Pause the serial thread
    # time.sleep(1)

    set_vfo_a_mem_commands = [
    ##Switch VFOA VFO/M(MEM)
    "2b41444154413a30302c3134350d0a573d000000881f00207102000851060008450400084d06000859030008e10c000800000000000000000000000000000000870b00080d04000800000000d5090008f90b00088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200080d0a",
    "2b41444154413a30302c3030360d0a042c010000000d0a",
    ]

    for command in set_vfo_a_mem_commands:
        set_vfo_a_mem_bytes = bytes.fromhex(command)
        ser.write(set_vfo_a_mem_bytes)
        #print(f"Sent command: {command}")

        start_time = time.time()
        while time.time() - start_time < .1:
            if ser.in_waiting > 0:
                # Read the response
                response = ser.read(ser.in_waiting)
                if response is not None:
                    # print(f"Response (hex): {response.hex()}")
                    # response_ascii = ''.join(chr(byte) for byte in response)
                    # print(f"Response (ascii): {response_ascii}")
                    pass
                time.sleep(0.1)
        pause_event.clear()
    # else:
    #     command_bytes = bytes.fromhex(command.replace(" ", ""))
    #     ser.write(command_bytes)
    #     print(f"Sent command: {command}")
    set_vfo_a_mem_status = "MEM"
    print (f"VFOA VFO/MEM: {set_vfo_a_mem_status}")

def set_vfo_b_vfo():
    set_vfo_b()    
    pause_event.set()  # Pause the serial thread
    # time.sleep(1)

    set_vfo_b_vfo_commands = [
    ##Switch VFOB VFO/M(VFO)
    "2b41444154413a30302c3134350d0a573d010000881f00207102000851060008450400084d06000859030008e10c000800000000000000000000000000000000870b00080d04000800000000d5090008f90b00088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200080d0a",
    "2b41444154413a30302c3030360d0a042d010000000d0a",
    ]

    for command in set_vfo_b_vfo_commands:
        set_vfo_b_vfo_bytes = bytes.fromhex(command)
        ser.write(set_vfo_b_vfo_bytes)
        #print(f"Sent command: {command}")

        start_time = time.time()
        while time.time() - start_time < .1:
            if ser.in_waiting > 0:
                # Read the response
                response = ser.read(ser.in_waiting)
                if response is not None:
                    # print(f"Response (hex): {response.hex()}")
                    # response_ascii = ''.join(chr(byte) for byte in response)
                    # print(f"Response (ascii): {response_ascii}")
                    pass
                time.sleep(0.1)
        pause_event.clear()
    # else:
    #     command_bytes = bytes.fromhex(command.replace(" ", ""))
    #     ser.write(command_bytes)
    #     print(f"Sent command: {command}")
    set_vfo_b_vfo_status = "VFO"
    print (f"VFOB VFO/MEM: {set_vfo_b_vfo_status}")    

def set_vfo_b_mem():
    set_vfo_b()
    pause_event.set()  # Pause the serial thread
    # time.sleep(1)

    set_vfo_b_mem_commands = [
    ##Switch VFOB VFO/M(Memory)
    "2b41444154413a30302c3134350d0a573d000000881f00207102000851060008450400084d06000859030008e10c000800000000000000000000000000000000870b00080d04000800000000d5090008f90b00088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200088b0200080d0a",
    "2b41444154413a30302c3030360d0a042d010000000d0a",
    ]

    for command in set_vfo_b_mem_commands:
        set_vfo_b_mem_bytes = bytes.fromhex(command)
        ser.write(set_vfo_b_mem_bytes)
        #print(f"Sent command: {command}")

        start_time = time.time()
        while time.time() - start_time < .1:
            if ser.in_waiting > 0:
                # Read the response
                response = ser.read(ser.in_waiting)
                if response is not None:
                    # print(f"Response (hex): {response.hex()}")
                    # response_ascii = ''.join(chr(byte) for byte in response)
                    # print(f"Response (ascii): {response_ascii}")
                    pass
                time.sleep(0.1)
        pause_event.clear()
    # else:
    #     command_bytes = bytes.fromhex(command.replace(" ", ""))
    #     ser.write(command_bytes)
    #     print(f"Sent command: {command}")
    set_vfo_b_mem_status = "MEM"
    print (f"VFOB VFO/MEM: {set_vfo_b_mem_status}")

def set_vfo_a_freq(argument):
    set_vfo_a_vfo()

    pause_event.set()  # Pause the serial thread
    # time.sleep(1)

    set_vfo_a_freq_commands = [
    # #Change Freq VFOA
    "2b 41 44 41 54 41 3a 30 30 2c 30 30 35 0d 0a 5a 02 00 00 00 0d 0a",
    f"2b41444154413a30302c3032330d0a2f0300{argument}155000000c00000000000000cf0900000d0a",
    ]

    for command in set_vfo_a_freq_commands:
        set_vfo_a_freq_bytes = bytes.fromhex(command)
        ser.write(set_vfo_a_freq_bytes)
        #print(f"Sent command: {command}")

        start_time = time.time()
        while time.time() - start_time < .1:
            if ser.in_waiting > 0:
                # Read the response
                response = ser.read(ser.in_waiting)
                if response is not None:
                    # print(f"Response (hex): {response.hex()}")
                    # response_ascii = ''.join(chr(byte) for byte in response)
                    # print(f"Response (ascii): {response_ascii}")
                    pass
                time.sleep(0.1)
        pause_event.clear()
    # else:
    #     command_bytes = bytes.fromhex(command.replace(" ", ""))
    #     ser.write(command_bytes)
    #     print(f"Sent command: {command}")
    get_freq_a()

def set_vfo_b_freq(argument):
    set_vfo_b_vfo()
    pause_event.set()  # Pause the serial thread
    # time.sleep(1)

    set_vfo_b_freq_commands = [
    # #Change Freq VFOB
    "2b 41 44 41 54 41 3a 30 30 2c 30 30 35 0d 0a 5a 01 00 00 00 0d 0a",
    f"2b41444154413a30302c3032330d0a2f0300{argument}155000000000000000000000cf0900000d0a",
    ]

    for command in set_vfo_b_freq_commands:
        set_vfo_b_freq_bytes = bytes.fromhex(command)
        ser.write(set_vfo_b_freq_bytes)
        #print(f"Sent command: {command}")

        start_time = time.time()
        while time.time() - start_time < .1:
            if ser.in_waiting > 0:
                # Read the response
                response = ser.read(ser.in_waiting)
                if response is not None:
                    # print(f"Response (hex): {response.hex()}")
                    # response_ascii = ''.join(chr(byte) for byte in response)
                    # print(f"Response (ascii): {response_ascii}")
                    pass
                time.sleep(0.1)
        pause_event.clear()
    # else:
    #     command_bytes = bytes.fromhex(command.replace(" ", ""))
    #     ser.write(command_bytes)
    #     print(f"Sent command: {command}")
    get_freq_b()

def prompt_interface():
    global response, listening # VFO_mode_status
    while True:
        try:
            user_input = input("Enter a command ('help' to list commands): ")
            split_input = user_input.split(' ')
            command = split_input[0]
            argument = split_input[1] if len(split_input) > 1 else None

            if command.lower() == 'q' or command.lower() == 'quit' or command.lower() == 'exit':
                stop_event.set()
                break
            elif command == 'help':
                print("Commands:")
                print("q: quit")
                print("get-zone-a:      VFO A Zone")
                print("get-zone-b:      VFO B Zone")
                print("get-channel-a:   VFO A Channel")
                print("get-channel-b:   VFO B Channel")
                print("get-freq-a:      VFO A Frequency")
                print("get-freq-b:      VFO B Frequency")
                print("get-gps-loc:")
                print("get-gps-lat:")
                print("get-gps-long:")
                print("get-gps-vel")
                print("get-gps-alt")
                print("get-gps-date")
                print("get-gps-time")
                print("get-vfo:         Current VFO")
                print("set-vfo-a:       Set VFO to A")
                print("set-vfo-b:       Set VFO to B")
                print("set-vfo-a-vfo:")
                print("set-vfo-b-vfo:")
                print("set-vfo-a-mem:")
                print("set-vfo-b-mem:")
                print("set-freq-a:")
                print("set-freq-b:")
                print("monitor-serial-enable:")
            
            elif command == 'monitor-serial-enable':
                listening = True
                listen_serial_traffic()
            elif command == 'monitor-serial-disable':
                listening = False
            ##VFOA Zone
            elif command == 'get-zone-a':
                get_zone_a()
            ##VFOA Frequency
            elif command == 'get-freq-a':
                get_freq_a()
            ##VFOA Channel
            elif command == 'get-channel-a':
                get_channel_a()
            ##VFOB Zone
            elif command == 'get-zone-b':
               get_zone_b()
            ##VFOB Frequency
            elif command == 'get-freq-b':
                get_freq_b()
            ##VFOB Channel
            elif command == 'get-channel-b':
                get_channel_b()
            ## get-gps-loc
            elif command == 'get-gps-loc':
                get_gps_loc()
            ## get-gps-lat								
            elif command == 'get-gps-lat':	
                get_gps_lat()
            ## get-gps-long								
            elif command == 'get-gps-long':
                get_gps_long()
            ## get-gps-vel				
            elif command == 'get-gps-vel':
                get_gps_vel()
            ## get-gps-alt				
            elif command == 'get-gps-alt':
                get_gps_alt()
            ## get-gps-date				
            elif command == 'get-gps-date':
                get_gps_date()
            ## get-gps-time				
            elif command == 'get-gps-time':
                get_gps_time()
            # elif command == 'get-vfo-legacy':
            #     print (f"VFO: {VFO_mode_status}")
            elif command == 'get-vfoa-power':
                get_vfoa_power()
            elif command == 'get-vfob-power':
                get_vfob_power()
            elif command == 'get-vfo':
                get_vfo()
            ## set-vfo-a				
            elif command == 'set-vfo-a':
                set_vfo_a()
            ## set-vfo-b
            elif command == 'set-vfo-b':
                set_vfo_b()
            elif command == 'set-vfo-a-vfo':
                set_vfo_a_vfo()
            elif command == 'set-vfo-b-vfo':
                set_vfo_b_vfo()
            elif command == 'set-vfo-a-mem':
                set_vfo_a_mem()
            elif command == 'set-vfo-b-mem':
                set_vfo_b_mem()
            
            elif command == 'set-freq-a':
                if argument is not None:
                    if validate_frequency(argument):
                        set_vfo_a_freq(argument)
                    else:
                        print("Invalid argument for 'set-freq-a' command. Frequency must be within 144-148MHz, 222-225MHz, or 420-450MHz.")
                else:
                    print("Missing argument for 'set-freq-a' command.")

            elif command == 'set-freq-b':
                if argument is not None:
                    if validate_frequency(argument):
                        set_vfo_b_freq(argument)
                    else:
                        print("Invalid argument for 'set-freq-b' command. Frequency must be within 144-148MHz, 222-225MHz, or 420-450MHz.")
                else:
                    print("Missing argument for 'set-freq-b' command.")
            
            else:
                print("Invalid command. Please try again.")
        except:
            print("Invalid command. Please try again. (TRY/EXCEPT)")

def validate_frequency(frequency):
    frequency = int(frequency)
    if (14400000 <= frequency <= 14800000) or (22200000 <= frequency <= 22500000) or (42000000 <= frequency <= 45000000):
        return True
    else:
        return False

serial_connect()
serial_thread = start_serial_thread()

# Start the prompt interface
prompt_interface()

# Wait for the serial thread to finish
serial_thread.join()

##PTT-hold
#"2b41444154413a30302c3032330d0a56010000000000000000000000000000000000000000000d0a"

##PTT-off
#"2b41444154413a30302c3032330d0a56000000000000000000000000000000000000000000000d0a"

# #Change Freq VFOA
# "2b 41 44 41 54 41 3a 30 30 2c 30 30 35 0d 0a 5a 02 00 00 00 0d 0a",
# f"2b41444154413a30302c3032330d0a2f0300{VFOAFREQ}155000000c00000000000000cf0900000d0a",

# #Change Freq VFOB
# "2b 41 44 41 54 41 3a 30 30 2c 30 30 35 0d 0a 5a 01 00 00 00 0d 0a",
# f"2b41444154413a30302c3032330d0a2f0300{VFOBFREQ}155000000000000000000000cf0900000d0a",