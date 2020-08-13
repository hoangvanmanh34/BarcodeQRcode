import cv2
import time
import numpy as np
import pyzbar.pyzbar as pyzbar
#from pyzbar.pyzbar import ZBarSymbol
import INI_r_w
from threading import Thread
import tempfile

ftemp = tempfile.TemporaryDirectory()
ini_cfg_path = 'config.ini'

def decode(im):
    decodeObjects=pyzbar.decode(im)
    return decodeObjects

def decode_Danny():
    # ---------Read config--------
    #cam_id = INI_r_w.Read_Value(ini_cfg_path, 'CAMERA', 'Index', 'int')
    #Camera_ID = cam_id#"/dev/v4l/by-id/USB\VID_0BDA&PID_58B0&MI_00\7&25249C4A&0&0000"#INI_r_w.Read_Value(ini_cfg_path, 'CAMERA', 'Index', 'int')
    # get webcam
    font = cv2.FONT_HERSHEY_SIMPLEX
    cab = cv2.VideoCapture(0)
    print(cab.get(15))
    #set resolution & open video
    cab.set(3,640)
    cab.set(4,480)
    print('aaaaa')
    time.sleep(2)
    while(cab.isOpened()):
        #print('bbb')
        #Capture frame by frame
        ret,frame = cab.read()
        #get image & convert to gray
        im = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        #cv2.imshow('Decode___TE:Danny___2019(Press q to Quit and Press s to save image)', im)
        #get code
        decodeObjects=decode(im)
        code_list = ''

        for decodeObject in decodeObjects:
            #get polygon
            points = decodeObject.polygon
            # if the points do not form the quad, find convex hull
            if len(points)>4:
                hull = cv2.convexHull(np.array([point for point in points],dtype=np.float32))
                hull = list(map(tuple,np.squeeze(hull)))
            else:
                hull=points
            #number of points in the convex hull
            n = len(hull)
            #draw the convex hull
            for i in range(0,n):
                cv2.line(frame,hull[i],hull[(i+1)%n],(0,0,255),2)
            #coordinates
            x=decodeObject.rect.left
            y=decodeObject.rect.top
            #print('+'+str(x)+'+'+str(y))
            typecode=decodeObject.type
            code = str(decodeObject.data,'utf-8')
            print(typecode)
            print(code)
            #draw text
            cv2.putText(frame,str(code),(x,y),font,1,(255,0,0),2,cv2.LINE_AA)
            if len(code) > 0:
                code_list += code + ','
        #display result
        cv2.imshow('Decode___TE:Danny___2019(Press q to Quit and Press s to save image)',frame)
        # ----Save data-----
        SN_file = open('D:/barcode.txt', 'w+')
        SN_file.write(str(code_list))
        SN_file.close()
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break
        elif key & 0xFF == ord('s'):  # wait for 's' key to save
            cv2.imwrite('Code.jpg', frame)
        time.sleep(0)
        ftemp.cleanup()
Thread(target=decode_Danny).start()

'''zreader = zxing.BarCodeReader()
zbarcode = zreader.decode(r'D:\Documents\Images\Code\code93.jpg')
print(zbarcode)'''

'''from pyzbar.pyzbar import decode
import cv2
import numpy as np


def barcodeReader(image, bgr):
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    barcodes = decode(gray_img)

    for decodedObject in barcodes:
        points = decodedObject.polygon

        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(image, [pts], True, (0, 255, 0), 3)

    for bc in barcodes:
        cv2.putText(frame, bc.data.decode("utf-8") + " - " + bc.type, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    bgr, 2)

        return "Barcode: {} - Type: {}".format(bc.data.decode("utf-8"), bc.type)


bgr = (8, 70, 208)

cap = cv2.VideoCapture(0)
while (True):
    ret, frame = cap.read()
    barcode = barcodeReader(frame, bgr)
    print(barcode)
    cv2.imshow('Barcode reader', frame)
    code = cv2.waitKey(10)
    if code == ord('q'):
        break'''

# import the necessary packages
'''import numpy as np
import argparse
import imutils
import cv2
import pyzbar.pyzbar as pyzbar
import time
from PIL import Image

def decode(im):
    decodeObjects=pyzbar.decode(im)
    return decodeObjects

im='images\\linear.jpg'#NIMG.png'
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=False,
                help="path to the image file")
args = vars(ap.parse_args())
# load the image and convert it to grayscale
image = cv2.imread(im)#(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# compute the Scharr gradient magnitude representation of the images
# in both the x and y direction using OpenCV 2.4
ddepth = cv2.cv.CV_32F if imutils.is_cv2() else cv2.CV_32F
gradX = cv2.Sobel(gray, ddepth=ddepth, dx=1, dy=0, ksize=-1)
gradY = cv2.Sobel(gray, ddepth=ddepth, dx=0, dy=1, ksize=-1)

# subtract the y-gradient from the x-gradient
gradient = cv2.subtract(gradX, gradY)
gradient = cv2.convertScaleAbs(gradient)

# blur and threshold the image
blurred = cv2.blur(gradient, (9, 9))
(_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)

# construct a closing kernel and apply it to the thresholded image
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

# perform a series of erosions and dilations
closed = cv2.erode(closed, None, iterations = 4)
closed = cv2.dilate(closed, None, iterations = 4)

# find the contours in the thresholded image, then sort the contours
# by their area, keeping only the largest one
cnts = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
c = sorted(cnts, key=cv2.contourArea, reverse=True)[0] #max(cnts, key = cv2.contourArea)#

# compute the rotated bounding box of the largest contour
rect = cv2.minAreaRect(c)
box = cv2.cv.BoxPoints(rect) if imutils.is_cv2() else cv2.boxPoints(rect)
box = np.int0(box)

# draw a bounding box arounded the detected barcode and display the
# image
cv2.drawContours(image, [box], -1, (0, 255, 0), 3)

decode(Image.open(im), symbols=[pyzbar.ZBarSymbol.CODE93])


cv2.imshow("Image", image)
cv2.waitKey(0)'''

'''
from pyzbar.pyzbar import decode,ZBarConfig,ZBarSymbol
from PIL import Image

im='images\\code93.gif'#code9.jpg'
d = decode(Image.open(im), symbols=[ZBarSymbol.CODE93,ZBarConfig.CFG_ASCII])

print(d)'''

'''from zxing import *

zxing_location = ".."
testimage = "images\\barcode.jpg"


def test_barcode_parser():
    text = """
file:/home/oostendo/Pictures/datamatrix/4-contrastcrop.bmp (format: DATA_MATRIX, type: TEXT):
Raw result:
36MVENBAEEAS04403EB0284ZB
Parsed result:
36MVENBAEEAS04403EB0284ZB
Also, there were 4 result points.
  Point 0: (24.0,18.0)
  Point 1: (21.0,196.0)
  Point 2: (201.0,198.0)
  Point 3: (205.23952,21.0)
"""

    barcode = BarCode(text)
    if (barcode.format != "DATA_MATRIX"):
        return 0

    if (barcode.raw != "36MVENBAEEAS04403EB0284ZB"):
        return 0

    if (barcode.data != "36MVENBAEEAS04403EB0284ZB"):
        return 0

    if (len(barcode.points) != 4 and barcode.points[0][0] != 24.0):
        return 0

    return 1


def test_codereader():
    # ~ zx = BarCodeReader(zxing_location)
    zx = BarCodeReader('/var/opt/zxing')

    barcode = zx.decode(testimage)
    print(barcode)
    #if re.match("http://", barcode.data):
    #    return 1

    #return 0

test_codereader()
'''
#!/usr/bin/env python

# python-gphoto2 - Python interface to libgphoto2
# http://github.com/jim-easterbrook/python-gphoto2
# Copyright (C) 2014-19  Jim Easterbrook  jim@jim-easterbrook.me.uk
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# "object oriented" version of camera-summary.py

'''from __future__ import print_function

import logging
import six
import sys

import gphoto2 as gp

def main():
    logging.basicConfig(
        format='%(levelname)s: %(name)s: %(message)s', level=logging.WARNING)
    callback_obj = gp.check_result(gp.use_python_logging())
    # make a list of all available cameras
    camera_list = []
    for name, addr in gp.check_result(gp.gp_camera_autodetect()):
        camera_list.append((name, addr))
    if not camera_list:
        print('No camera detected')
        return 1
    camera_list.sort(key=lambda x: x[0])
    # ask user to choose one
    for index, (name, addr) in enumerate(camera_list):
        print('{:d}:  {:s}  {:s}'.format(index, addr, name))
    if six.PY3:
        choice = input('Please input number of chosen camera: ')
    else:
        choice = raw_input('Please input number of chosen camera: ')
    try:
        choice = int(choice)
    except ValueError:
        print('Integer values only!')
        return 2
    if choice < 0 or choice >= len(camera_list):
        print('Number out of range')
        return 3
    # initialise chosen camera
    name, addr = camera_list[choice]
    camera = gp.Camera()
    # search ports for camera port name
    port_info_list = gp.PortInfoList()
    port_info_list.load()
    idx = port_info_list.lookup_path(addr)
    camera.set_port_info(port_info_list[idx])
    camera.init()
    text = camera.get_summary()
    print('Summary')
    print('=======')
    print(str(text))
    try:
        text = camera.get_manual()
        print('Manual')
        print('=======')
        print(str(text))
    except Exception as ex:
        print(str(ex))
    camera.exit()
    return 0

if __name__ == "__main__":
    sys.exit(main())'''


'''import subprocess
import re

device_re = re.compile("Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
df = subprocess.check_output("lsusb", shell=True)
for i in df.split('\n'):
    if i:
        info = device_re.match(i)
        if info:
            dinfo = info.groupdict()
            if "Logitech, Inc. Webcam C270" in dinfo['tag']:
                print("Camera found.")
                bus = dinfo['bus']
                device = dinfo['device']
                break'''


'''import win32com.client
objSWbemServices = win32com.client.Dispatch("WbemScripting.SWbemLocator").ConnectServer(".","root\cimv2")
for item in objSWbemServices.ExecQuery("SELECT * FROM Win32_PnPEntity"):
    print('-'*60)
    for name in ('Availability', 'Caption', 'ClassGuid', 'ConfigManagerUserConfig',
                 'CreationClassName', 'Description', 'DeviceID', 'ErrorCleared', 'ErrorDescription',
                 'InstallDate', 'LastErrorCode', 'Manufacturer', 'Name', 'PNPDeviceID', 'PowerManagementCapabilities ',
                 'PowerManagementSupported', 'Service', 'Status', 'StatusInfo', 'SystemCreationClassName',
                 'SystemName'):
        a = getattr(item, name, None)
        #if a == 'FULL HD 1080P Webcam':
        #    print(a)
        if a is not None:
            print('%s: %s' % (name, a))'''

'''------------------------------------------------------------
Caption: FULL HD 1080P Webcam
ClassGuid: {6bdd1fc6-810f-11d0-bec7-08002be2092f}
ConfigManagerUserConfig: False
CreationClassName: Win32_PnPEntity
Description: USB Video Device
DeviceID: USB\VID_0BDA&PID_58B0&MI_00\7&25249C4A&0&0000
Manufacturer: Microsoft
Name: FULL HD 1080P Webcam
PNPDeviceID: USB\VID_0BDA&PID_58B0&MI_00\7&25249C4A&0&0000
Service: usbvideo
Status: OK
SystemCreationClassName: Win32_ComputerSystem
SystemName: V0916166-TE
------------------------------------------------------------'''
'''------------------------------------------------------------
Caption: HD Webcam C525
ClassGuid: {6bdd1fc6-810f-11d0-bec7-08002be2092f}
ConfigManagerUserConfig: False
CreationClassName: Win32_PnPEntity
Description: USB Video Device
DeviceID: USB\VID_046D&PID_0826&MI_02\7&378F8C43&0&0002
Manufacturer: Microsoft
Name: HD Webcam C525
PNPDeviceID: USB\VID_046D&PID_0826&MI_02\7&378F8C43&0&0002
Service: usbvideo
Status: OK
SystemCreationClassName: Win32_ComputerSystem
SystemName: V0916166-TE
------------------------------------------------------------'''
'''------------------------------------------------------------
Caption: FULL HD 1080P Webcam
ClassGuid: {6bdd1fc6-810f-11d0-bec7-08002be2092f}
ConfigManagerUserConfig: False
CreationClassName: Win32_PnPEntity
Description: USB Video Device
DeviceID: USB\VID_0BDA&PID_58B0&MI_00\7&25249C4A&0&0000
Manufacturer: Microsoft
Name: FULL HD 1080P Webcam
PNPDeviceID: USB\VID_0BDA&PID_58B0&MI_00\7&25249C4A&0&0000
Service: usbvideo
Status: OK
SystemCreationClassName: Win32_ComputerSystem
SystemName: V0916166-TE
------------------------------------------------------------'''