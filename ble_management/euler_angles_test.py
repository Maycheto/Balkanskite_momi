import struct
import math

DIST = 35/100

packet = [0x55, 0x53, 0x35, 0xc6, 0x83, 0xfe, 0x51, 0x40, 0xd0, 0x46, 0xcb]
packet2 = [0x55, 0x53, 0xce, 0x50, 0x59, 0xdd, 0xa, 0x4e, 0xd0, 0x46, 0x6a]

def angle_output_decode(angle_data_packet):
   if len(angle_data_packet) != 11 or angle_data_packet[0] != 0x55 or angle_data_packet[1] != 0x53:
        raise ValueError("Invalid packet")
   roll_raw = struct.unpack('<h', bytes(angle_data_packet[2:4]))[0]  
   pitch_raw = struct.unpack('<h', bytes(angle_data_packet[4:6]))[0]
   yaw_raw = struct.unpack('<h', bytes(angle_data_packet[6:8]))[0]
   roll_raw = (roll_raw/32768) * 180
   pitch_raw = (pitch_raw/32768) * 180
   yaw_raw = (yaw_raw/32768) * 180
   
   data = [roll_raw, pitch_raw, yaw_raw]
   
   return data

packet1_data = angle_output_decode(packet)
packet2_data = angle_output_decode(packet2)

pitch_delta =  packet1_data[1] - packet2_data[1]
print(pitch_delta)
pitch_delta = math.radians(pitch_delta)
print(pitch_delta)
result = pitch_delta / DIST

print(result)
