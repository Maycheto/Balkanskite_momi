import asyncio
from bleak import BleakClient, BleakScanner
import binascii
import struct
import math
import numpy as np
from scipy.spatial.transform import Rotation as R

# async def scan():
#     devices = await BleakScanner.discover()
#     for device in devices:
#         print(device)

# asyncio.run(scan())

DEVICE_UUID = "BD445A8F-424C-F5E0-4E95-A506B39AC8D7" 
CHARACTERISTIC_UUID = "6e400003-c352-11e5-953d-0002a5d5c51b"

async def connect():
     async with BleakClient(DEVICE_UUID) as client:
        print(f"Connected to {DEVICE_UUID}: {client.is_connected}")

asyncio.run(connect())

async def find_services():
    async with BleakClient(DEVICE_UUID) as client:
        print(f"Connected to {DEVICE_UUID}")
        for service in client.services:
            print(f"\n🔹 Service: {service.uuid}")
            for char in service.characteristics:
                print(f"  ↳ Characteristic: {char.uuid} | Properties: {char.properties}")

asyncio.run(find_services())

def decode_data(raw_data):
    for i in range(len(raw_data) - 10):  
        if raw_data[i] == 0x55 and raw_data[i + 1] == 0x53:
            buffer = raw_data[i:i + 11] 
            for j in range(i + 11, len(raw_data) - 10): 
                if raw_data[j] == 0x55 and raw_data[j + 1] == 0x53:
                    return [buffer, raw_data[j:j + 11]] 
            
    return []  

              
    
def hex_packet(raw_data):
    b = binascii.hexlify(raw_data).decode()
    return b

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
    
def magic(data1, data2, degrees=True):
    # roll_raw = abs(data1[0] - data2[0])
    # pitch_raw =  abs(data1[1] - data2[1])
    # yaw_raw =  abs(data1[2] - data2[2])
    # return roll_raw + pitch_raw + yaw_raw
    R1 = R.from_euler('xyz', data1, degrees=degrees).as_matrix()
    R2 = R.from_euler('xyz', data2, degrees=degrees).as_matrix()
    
    R_rel = R1.T @ R2
    
    theta = np.arccos((np.trace(R_rel) - 1) / 2)
    
    if degrees:
        theta = np.degrees(theta)
    
    return theta


async def notification_handler(sender, data):
    # print(f"Received from {sender}: {data}")
    # print(hex_packet(data))
    angle_packet = decode_data(data)
    # rint(angle_packet)
    # print(hex_packet(data))
    # print(len(angle_packet))
    # print(angle_packet[0])
    # print(angle_packet[1])
    hihi = angle_output_decode(angle_packet[0])
    hihi2 = angle_output_decode(angle_packet[1])
    # print(hihi[0])
    # print(hihi[1])
    # print(hihi[2])
    # angle_output_decode(data) 
    print(magic(hihi, hihi2))

        
     

async def subscribe():
    async with BleakClient(DEVICE_UUID) as client:
        print(f"Connected to {DEVICE_UUID}: {client.is_connected}")
        await client.start_notify(CHARACTERISTIC_UUID, notification_handler)
        print(f"Subscribed to notifications from {CHARACTERISTIC_UUID}")
        await asyncio.sleep(60)
        await client.stop_notify(CHARACTERISTIC_UUID)
        print(f"Unsubscribed from {CHARACTERISTIC_UUID}")

asyncio.run(subscribe())