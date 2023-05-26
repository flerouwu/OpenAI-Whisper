import sounddevice as sd

if __name__ == "__main__":
    devices = sd.query_devices()

    if not isinstance(devices, sd.DeviceList):
        raise Exception("No devices found")

    print(devices)
