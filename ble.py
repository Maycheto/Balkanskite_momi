import asyncio
from bleak import BleakClient, BleakScanner
import binascii
import struct
import math
import numpy as np
from scipy.spatial.transform import Rotation as R
from backyendy import insert_data 

DEVICE_UUID = "00:18:DA:40:6A:49" 
CHARACTERISTIC_UUID = "6e400003-c352-11e5-953d-0002a5d5c51b"

async def connect():
     async with BleakClient(DEVICE_UUID) as client:
        print(f"Connected to {DEVICE_UUID}: {client.is_connected}")

asyncio.run(connect())

async def find_services():
    async with BleakClient(DEVICE_UUID) as client:
        print(f"Connected to {DEVICE_UUID}")
        for service in client.services:
            # Use .encode('utf-8', 'ignore') to handle the Unicode symbol safely
            print(f"\n{'🔹'.encode('utf-8', 'ignore').decode('utf-8')} Service: {service.uuid}")
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
    R1 = R.from_euler('xyz', data1, degrees=degrees).as_matrix()
    R2 = R.from_euler('xyz', data2, degrees=degrees).as_matrix()
    
    R_rel = R1.T @ R2
    
    theta = np.arccos((np.trace(R_rel) - 1) / 2)
    
    if degrees:
        theta = np.degrees(theta)
    
    return theta

async def notification_handler(sender, data):
    angle_packet = decode_data(data)
    hihi = angle_output_decode(angle_packet[0])
    hihi2 = angle_output_decode(angle_packet[1])
    print(magic(hihi, hihi2))

    if len(angle_packet) < 2:
        return

    hihi = angle_output_decode(angle_packet[0])
    hihi2 = angle_output_decode(angle_packet[1])
    angle = magic(hihi, hihi2)

    print(f"[BLE] Received coefficient: {angle}")

    # Записваме ъгъла в базата
    insert_data(angle)

async def subscribe():
    async with BleakClient(DEVICE_UUID) as client:
        print(f"Connected to {DEVICE_UUID}: {client.is_connected}")
        await client.start_notify(CHARACTERISTIC_UUID, notification_handler)
        print(f"Subscribed to notifications from {CHARACTERISTIC_UUID}")
        await asyncio.sleep(180)
        await client.stop_notify(CHARACTERISTIC_UUID)
        print(f"Unsubscribed from {CHARACTERISTIC_UUID}")

asyncio.run(subscribe())
