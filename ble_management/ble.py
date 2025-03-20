import asyncio
from bleak import BleakClient, BleakScanner

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
    temperature = int.from_bytes(raw_data[8:10], byteorder='little') / 100
    humidity = int.from_bytes(raw_data[4:8], byteorder='little') / 100 
    pressure = int.from_bytes(raw_data[13:16], byteorder='little') / 1000

    print(f"Temperature: {temperature} °C")
    print(f"Humidity: {humidity} %")
    print(f"Pressure: {pressure} kPa")

async def notification_handler(sender, data):
    print(f"Received from {sender}: {data}")
    decode_data(data)  

async def subscribe():
    async with BleakClient(DEVICE_UUID) as client:
        print(f"Connected to {DEVICE_UUID}: {client.is_connected}")
        await client.start_notify(CHARACTERISTIC_UUID, notification_handler)
        print(f"Subscribed to notifications from {CHARACTERISTIC_UUID}")
        await asyncio.sleep(60)
        await client.stop_notify(CHARACTERISTIC_UUID)
        print(f"Unsubscribed from {CHARACTERISTIC_UUID}")

asyncio.run(subscribe())