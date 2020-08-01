# Remote Control - As The Controller Device
#
# This script configures your OpenMV Cam to remotely control another OpenMV Cam using the RPC
# library. This script can be run by any micropython board implementing the pyb module to
# remotely control an OpenMV Cam.
import json
import struct
import requests
import serial
import rpc

SERIAL_PORT = ""
SERIAL_RATE = 9600
number = 0
interface = rpc.rpc_usb_vcp_master(SERIAL_PORT)


def exe_jpeg_snapshot():
    global number
    result = interface.call("jpeg_snapshot")
    if result is not None:
        name = "snapshot-%05d.jpg" % number
        print("Writing jpeg %s..." % name)
        with open(name, "wb") as snap:
            snap.write(result)


def send_coordinates(cord):
    global number
    result = interface.call("accessed", coordinates)
    if result is not None:
        name = "snapshot-%05d.jpg" % number
        print("Writing jpeg %s..." % name)
        with open(name, "wb") as snap:
            snap.write(result)


def process_ready():
    global number
    result = interface.call("ready")
    result = result.tobytes().decode('utf-8');
    print(result)
    if result is not None:
        return result


def main():
    while True:  # if process_ready() == "True": #uncomment to allow pictures to come in only when the frame shows elevated temperatures
        exe_jpeg_snapshot()
        params = (
            ('version', '2019-02-11'),
        )
        files = {
            'features': (None, 'objects'),
            'threshold': (None, '0.4'),
            'collection_ids': (None, '***********'),
            'images_file': ("snapshot-00000.jpg", open("snapshot-00000.jpg", 'rb')),
        }

        response = requests.post('https://gateway.watsonplatform.net/visual-recognition/api/v4/analyze',
                                 params=params, files=files,
                                 auth=('apikey', '*****************'))
        print(response.json());
        try:
            m = response.json()
            x = m["images"][0]['objects']['collections'][0]["objects"][0]['location']['left']
            y = m["images"][0]['objects']['collections'][0]["objects"][0]['location']['top']
            width = m["images"][0]['objects']['collections'][0]["objects"][0]['location']['width']
            height = m["images"][0]['objects']['collections'][0]["objects"][0]['location']['height']
            coordinates = str(x) + "," + str(y) + "," + str(width) + "," + str(height)
            send_coordinates(coordinates)
            print(coordinates)
        except:
            print("no face data")


if __name__ == "__main__":
    main()
