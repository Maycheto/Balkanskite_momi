import asyncio
from bleak import BleakClient, BleakScanner
import binascii
import struct
from backyendy import insert_data  # Импортираме функцията

# async def scan():
#     devices = await BleakScanner.discover()
#     for device in devices:
#         print(device)

# asyncio.run(scan())

DEVICE_UUID = "00:18:DA:40:6A:49"
CHARACTERISTIC_UUID = "6e400003-c352-11e5-953d-0002a5d5c51b"


def decode_data(raw_data):
    for i in range(len(raw_data) - 10):
        if raw_data[i] == 0x55 and raw_data[i + 1] == 0x53:
            buffer = raw_data[i:i + 11]
            for j in range(i + 11, len(raw_data) - 10):
                if raw_data[j] == 0x55 and raw_data[j + 1] == 0x53:
                    return [buffer, raw_data[j:j + 11]]
    return []


def angle_output_decode(angle_data_packet):
    if len(angle_data_packet) != 11 or angle_data_packet[0] != 0x55 or angle_data_packet[1] != 0x53:
        raise ValueError("Invalid packet")

    roll_raw = struct.unpack('<h', bytes(angle_data_packet[2:4]))[0]
    pitch_raw = struct.unpack('<h', bytes(angle_data_packet[4:6]))[0]
    yaw_raw = struct.unpack('<h', bytes(angle_data_packet[6:8]))[0]
    roll_raw = (roll_raw / 32768) * 180
    pitch_raw = (pitch_raw / 32768) * 180
    yaw_raw = (yaw_raw / 32768) * 180

    return [roll_raw, pitch_raw, yaw_raw]


def magic(data1, data2):
    roll_raw = abs(data1[0] - data2[0])
    pitch_raw = abs(data1[1] - data2[1])
    yaw_raw = abs(data1[2] - data2[2])
    return roll_raw + pitch_raw + yaw_raw


async def notification_handler(sender, data):
    angle_packet = decode_data(data)

    if len(angle_packet) < 2:
        return

    hihi = angle_output_decode(angle_packet[0])
    hihi2 = angle_output_decode(angle_packet[1])
    coefficient = magic(hihi, hihi2)

    print(f"[BLE] Received coefficient: {coefficient}")

    # Записваме коефициента в базата
    insert_data(coefficient)


async def subscribe():
    async with BleakClient(DEVICE_UUID) as client:
        print(f"[BLE] Connected to {DEVICE_UUID}: {client.is_connected}")

        await client.start_notify(CHARACTERISTIC_UUID, notification_handler)
        print(f"[BLE] Subscribed to {CHARACTERISTIC_UUID}")

        await asyncio.sleep(60)  # Слуша за 60 секунди
        await client.stop_notify(CHARACTERISTIC_UUID)
        print("[BLE] Unsubscribed from notifications")


if __name__ == "__main__":
    asyncio.run(subscribe())
