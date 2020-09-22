import serial
import cv2
from tkinter import *
from tkinter import messagebox
import tkinter as tk
import pyzbar.pyzbar as pyzbar
import time
import numpy as np
from threading import Thread
import serial.tools.list_ports
from datetime import datetime
import socket

#Hoang Van Manh
#Danny TE-NPI
#hoangvanmanhpc@gmail.com
#https://www.youtube.com/c/StevenHCode
#https://github.com/hoangvanmanh34

symlist = re.compile('[@_!#$%^&*()<>?/|}{~:]')
#sn+test_time+machine+result+error_Code

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        # self.Load_CFG()
        self.master.title("Check PSU. TE-Danny.2019")
        # , bg="lightskyblue")
        self.Frame1 = Frame(master, highlightcolor="white", highlightthickness=1)
        self.Frame1.grid(rowspan=10, column=0, columnspan=8, sticky=W + E + N + S, pady=0, padx=0)

        self.Frame2 = Frame(master, highlightcolor="white", highlightthickness=1)
        self.Frame2.grid(row=1, rowspan=10, column=10, columnspan=8, sticky=W + E + N + S, pady=0, padx=0)

        # -----------------Result-----------------------------------------------------------
        self.lb_Result1 = Label(self.Frame1, text='Standby', font='serif 42', fg='blue', bg='white', width=9, borderwidth=2, relief="groove")
        self.lb_Result1.grid(row=0, rowspan=2, column=0, columnspan=2, sticky=W)
        self.lb_Result2 = Label(self.Frame1, text='Standby', font='serif 42', fg='blue', bg='white', width=9, borderwidth=2, relief="groove")
        self.lb_Result2.grid(row=0, rowspan=2, column=2, columnspan=2, sticky=W)
        self.lb_Result3 = Label(self.Frame1, text='Standby', font='serif 42', fg='blue', bg='white', width=9, borderwidth=2, relief="groove")
        self.lb_Result3.grid(row=0, rowspan=2, column=4, columnspan=2, sticky=W)
        # ----------------------------------------------------------------------------

        self.txtSN_1 = Text(self.Frame1, height=1, width=23, font='serif 18', fg='red', bg='yellow')
        self.txtSN_1.grid(row=2, rowspan=1, column=0, columnspan=2, sticky=W)
        # self.txtSN_1.tag_config('center',justify=CENTER)
        self.txtSN_2 = Text(self.Frame1, height=1, width=23, font='serif 18', fg='red', bg='yellow')
        self.txtSN_2.grid(row=2, rowspan=1, column=2, columnspan=2, sticky=W)
        self.txtSN_3 = Text(self.Frame1, height=1, width=23, font='serif 18', fg='red', bg='yellow')
        self.txtSN_3.grid(row=2, rowspan=1, column=4, columnspan=2, sticky=W)

        self.txtPre = Text(self.Frame1, height=1, width=7, font='serif 18', fg='black', bg='white')
        self.txtPre.grid(row=2, column=7, columnspan=2, sticky=W, padx=0)
        '''self.txtPre_2 = Text(self.Frame1, height=1, width=23, font='serif 18', fg='black', bg='white')
        self.txtPre_2.grid(row=2, column=2, columnspan=2, sticky=W)
        self.txtPre_3 = Text(self.Frame1, height=1, width=23, font='serif 18', fg='black', bg='white')
        self.txtPre_3.grid(row=2, column=4, columnspan=2, sticky=W)'''

        self.lb_Pre = Label(self.Frame1, text='Pre_Fix :',font='serif 15', fg='blue')
        self.lb_Pre.grid(row=2, column=6, columnspan=2, sticky=W, padx=10)

        comlist = serial.tools.list_ports.comports()
        connected = []
        for element in comlist:
            connected.append(element.device)
            self.vconnected = StringVar(root)
        self.vconnected.set("SFIS")
        lconnected = OptionMenu(self.Frame1, self.vconnected, *connected)
        lconnected.config(width=7)
        lconnected.grid(row=5, column=6, padx=10)

        self.btnOpenCOM = tk.Button(self.Frame1, text="SFIS_Closed", fg='white', bg='red', font='serif 10',
                                    width=11, command=self.COM_Control)
        self.btnOpenCOM.grid(row=5, column=7, sticky=W, padx=0)

        comlist2 = serial.tools.list_ports.comports()
        connected2 = []
        for element in comlist2:
            connected2.append(element.device)
            self.vconnected2 = StringVar(root)
        self.vconnected2.set("Fixture")
        lconnected2 = OptionMenu(self.Frame1, self.vconnected2, *connected2)
        lconnected2.config(width=7)
        lconnected2.grid(row=6, column=6, padx=10)

        self.btnOpenCOM2 = tk.Button(self.Frame1, text="Fixture_Closed", fg='white', bg='red', font='serif 10',
                                    width=11, command=self.COM_Control2)
        self.btnOpenCOM2.grid(row=6, column=7, sticky=W, padx=0)

        # ------------------------------------------------------------------

        camlist1 = [0, 1, 2]
        for element in camlist1:
            connected.append(element)
            self.vcam1 = StringVar(root)
        self.vcam1.set("index")
        lcam1 = OptionMenu(self.Frame1, self.vcam1, *camlist1)
        lcam1.config(height=2, width=5)
        lcam1.grid(row=4, column=1)

        camlist2 = [0, 1, 2]
        for element in camlist2:
            connected.append(element)
            self.vcam2 = StringVar(root)
        self.vcam2.set("index")
        lcam2 = OptionMenu(self.Frame1, self.vcam2, *camlist2)
        lcam2.config(height=2, width=5)
        lcam2.grid(row=4, column=3)

        camlist3 = [0, 1, 2]
        for element in camlist3:
            connected.append(element)
            self.vcam3 = StringVar(root)
        self.vcam3.set("index")
        lcam3 = OptionMenu(self.Frame1, self.vcam3, *camlist3)
        lcam3.config(height=2, width=5)
        lcam3.grid(row=4, column=5)
        # --------------------------------------------------------------

        self.btnOpen1 = tk.Button(self.Frame1, text="Camera_1", fg='black', bg='limegreen', font='serif 14',
                                  width=20, command=self.Open_CAM_1)
        self.btnOpen1.grid(row=4, column=0, sticky=W)
        self.btnOpen2 = tk.Button(self.Frame1, text="Camera_2", fg='black', bg='limegreen', font='serif 14',
                                  width=20, command=self.Open_CAM_2)
        self.btnOpen2.grid(row=4, column=2, sticky=W)
        self.btnOpen3 = tk.Button(self.Frame1, text="Camera_3", fg='black', bg='limegreen', font='serif 14',
                                  width=20, command=self.Open_CAM_3)
        self.btnOpen3.grid(row=4, column=4, sticky=W)

        self.txtContent = Text(self.Frame1, width=83, height=12, font='serif 14', fg='black', bg='white')
        self.txtContent.grid(row=5, rowspan=12, column=0, columnspan=8, sticky=W, pady=10)

        self.txtFixture = Text(self.Frame1, width=20, height=9, font='serif 12', fg='black', bg='white')
        self.txtFixture.grid(row=7, rowspan=10, column=6, columnspan=8, sticky=W, pady=10, padx=10)

        # -----------------------------------------------------------------------------

        self.barCode1 = ""
        self.barCode2 = ""
        self.barCode3 = ""
        self.barCode4 = ""

        # _--------------------
        self.barcode_re_1 = ""
        self.b_barcode_re_1 = False
        self.barcode_re_1_old = ""

        self.barcode_re_2 = ""
        self.b_barcode_re_2 = False
        self.barcode_re_2_old = ""

        self.barcode_re_3 = ""
        self.b_barcode_re_3 = False
        self.barcode_re_3_old = ""
        # ----------------------------
        self.Cam1_Open = False
        self.Cam2_Open = False
        self.Cam3_Open = False

        self.Stared = False
        #self.Open_COM_Fixture()
        Thread(target=self.COM_Receive).start()
        self.Fix_data = ''

        self.Error_Code1 = 'PSU001'
        self.Error_Code2 = 'PSU002'
        self.time1 = 0
        self.time2 = 0
        self.time3 = 0

        self.PC_Name = socket.gethostname()
        print(self.PC_Name)
        print(len(self.PC_Name))

        self.SN_Len = 25



    def COM_Receive(self):
        while True:
            self.Fix_data = '-'
            if self.Stared:
                self.Fix_data = '1'
                self.Fix_data = str(self.Get_in_Fixture())
                if len(self.Fix_data) > 3 :
                    #for f in self.Fix_data:
                    self.txtFixture.insert(1.0, self.Fix_data + '\r\n')
                time.sleep(0.2)
                #print(self.Fix_data)
            time.sleep(0.2)


    def Open_CAM_1(self):
        if self.txtPre.get(1.0, 'end-1c').strip() != "":
            if self.btnOpen1['bg'] == 'limegreen':
                self.Cam1_Open = True
                self.CAM1_Start = Thread(target=self.Camera_1)
                self.CAM1_Start.start()
                self.btnOpen1.configure(bg='red')
                self.Stared = True
            else:
                self.Cam1_Open = False
                cv2.destroyWindow('CAM_1')
                self.btnOpen1.configure(bg='limegreen')
                self.CAM1_Start.join()
                print(self.CAM1_Start.is_alive())
                cv2.destroyAllWindows()
        else:
            messagebox.showinfo('Pre_Fix request', 'Check Pre_Fix CAM_1')

    def Open_CAM_2(self):
        if self.txtPre.get(1.0, 'end-1c').strip() != "":
            if self.btnOpen2['bg'] == 'limegreen':
                self.Cam2_Open = True
                Thread(target=self.Camera_2).start()
                self.btnOpen2.configure(bg='red')
                self.Stared = True
            else:
                self.Cam2_Open = False
                cv2.destroyWindow('CAM_2')
                self.btnOpen2.configure(bg='limegreen')

        else:
            messagebox.showinfo('Pre_Fix request', 'Check Pre_Fix CAM_2')


    def Open_CAM_3(self):
        if self.txtPre.get(1.0, 'end-1c').strip() != "":
            if self.btnOpen3['bg'] == 'limegreen':
                self.Cam3_Open = True
                Thread(target=self.Camera_3).start()
                self.btnOpen3.configure(bg='red')
                self.Stared = True
            else:
                self.Cam3_Open = False
                cv2.destroyWindow('CAM3')
                self.btnOpen3.configure(bg='limegreen')
        else:
            messagebox.showinfo('Pre_Fix request', 'Check Pre_Fix CAM_3')

    def re1(self):
        self.txtSN_1.delete(1.0, END)
        self.lb_Result1.config(text='Running', fg='gold')
        if self.barcode_re_1 != self.barCode1 and self.b_barcode_re_1 == False:
            self.barcode_re_1 = self.barCode1
        self.b_barcode_re_1 = True
        for i in range(0, 15):
            if i >= 8:
                #Fix_re = str(self.Get_in_Fixture())
                #print((Fix_re))
                if self.barcode_re_1 == self.barCode1 and self.Fix_data.find('FIX1_PASS') > 0:
                    print('OK')
                    self.b_barcode_re_1 = False
                    self.lb_Result1.config(text='PASS', fg='green')
                    test_time = '%02d' %(datetime.now() - self.time1).seconds
                    strSend = self.Build_Value(self.barcode_re_1,self.SN_Len) + 'PASS' + test_time + self.PC_Name
                    try:
                        if self.Send_COM(strSend+'\r\n'):
                            self.txtSN_1.insert(1.0, self.barcode_re_1)
                            self.txtContent.insert(1.0, str(datetime.now()) + '  -->  CAM_1 : ' + strSend + '\r\n')
                        else:
                            messagebox.showinfo('Please Open SFC COM', 'Please Open SFC COM')
                    except:
                        messagebox.showinfo('Please Open SFC COM', 'Please Open SFC COM')
                        break
                    break
                elif (self.barcode_re_1 == self.barCode1 and self.Fix_data.find('FIX1_FAIL') > 0):
                    self.Send_Result_1(self.Error_Code1)
                    break
                elif i >= 14:
                    self.Send_Result_1(self.Error_Code2)
                    break
            time.sleep(0.5)

    def re2(self):
        self.txtSN_2.delete(1.0, END)
        self.lb_Result2.config(text='Running', fg='gold')
        if self.barcode_re_2 != self.barCode2 and self.b_barcode_re_2 == False:
            self.barcode_re_2 = self.barCode2
        self.b_barcode_re_2 = True
        for i in range(0, 15):
            if i >= 8:
                #Fix_re = str(self.Get_in_Fixture())
                #print((Fix_re))
                if self.barcode_re_2 == self.barCode2 and self.Fix_data.find('FIX2_PASS') > 0:
                    print('OK')
                    self.lb_Result2.config(text='PASS', fg='green')
                    test_time = '%02d' % (datetime.now() - self.time2).seconds
                    strSend = self.Build_Value(self.barcode_re_2, self.SN_Len) + 'PASS' + test_time + self.PC_Name
                    try:
                        if self.Send_COM(strSend+'\r\n'):
                            self.txtSN_2.insert(1.0, self.barcode_re_2)
                            self.txtContent.insert(1.0, str(datetime.now()) + '  -->  CAM_2 : ' + strSend + '\r\n')
                        else:
                            messagebox.showinfo('Please Open SFC COM', 'Please Open SFC COM')
                    except:
                        messagebox.showinfo('Please Open SFC COM', 'Please Open SFC COM')
                        break
                    self.b_barcode_re_2 = False
                    break
                elif (self.barcode_re_2 == self.barCode2 and self.Fix_data.find('FIX2_FAIL') > 0):
                    print('------------------------------------------')
                    self.Send_Result_2(self.Error_Code1)
                    break
                elif i >= 14:
                    self.Send_Result_2(self.Error_Code2)
                    break
            time.sleep(0.5)

    def re3(self):
        self.txtSN_3.delete(1.0, END)
        self.lb_Result3.config(text='Running', fg='gold')
        if self.barcode_re_3 != self.barCode3 and self.b_barcode_re_3 == False:
            self.barcode_re_3 = self.barCode3
        self.b_barcode_re_3 = True
        for i in range(0, 15):
            if i >= 8:
                #Fix_re = str(self.Get_in_Fixture())
                #print((Fix_re))
                if self.barcode_re_3 == self.barCode3 and self.Fix_data.find('FIX3_PASS') > 0:
                    print('OK')
                    self.lb_Result3.config(text='PASS', fg='green')
                    test_time = '%02d' % (datetime.now() - self.time3).seconds
                    strSend = self.Build_Value(self.barcode_re_3,self.SN_Len) + 'PASS' + test_time + self.PC_Name
                    try:
                        if self.Send_COM(strSend+'\r\n'):
                            self.txtSN_3.insert(1.0, self.barcode_re_3)
                            self.txtContent.insert(1.0, str(datetime.now()) + '  -->  CAM_3 : ' + strSend + '\r\n')
                        else:
                            messagebox.showinfo('Please Open SFC COM', 'Please Open SFC COM')
                    except:
                        messagebox.showinfo('Please Open SFC COM', 'Please Open SFC COM')
                        break
                    self.b_barcode_re_3 = False
                    break
                elif (self.barcode_re_3 == self.barCode3 and self.Fix_data.find('FIX3_FAIL') > 0):
                    self.Send_Result_3(self.Error_Code1)
                    break
                elif i >= 14:
                    self.Send_Result_3(self.Error_Code2)
                    break
            time.sleep(0.5)

    def Send_Result_1(self, ERROR):
        self.lb_Result1.config(text='FAIL', fg='red')
        #self.txtContent.insert(1.0, str(datetime.now()) + '  -->  CAM_1 : ' + self.barcode_re_1 + ' : fail' + '\r\n')
        self.barcode_re_1_old = self.barcode_re_1
        self.b_barcode_re_1 = False
        test_time = '%02d' % (datetime.now() - self.time1).seconds
        strSend = self.Build_Value(self.barcode_re_1,self.SN_Len) + 'FAIL' + test_time + self.PC_Name + ERROR
        try:
            if self.Send_COM(strSend + '\r\n'):
                self.txtSN_1.insert(1.0, self.barcode_re_1)
                self.txtContent.insert(1.0, str(datetime.now()) + '  -->  CAM_1 : ' + strSend + '\r\n')
            else:
                messagebox.showinfo('Please Open SFC COM', 'Please Open SFC COM')
        except:
            messagebox.showinfo('Please Open SFC COM', 'Please Open SFC COM')

    def Send_Result_2(self, ERROR):
        self.lb_Result2.config(text='FAIL', fg='red')
        #self.txtContent.insert(1.0, str(datetime.now()) + '  -->  CAM_2 : ' + self.barcode_re_2 + ' : fail' + '\r\n')
        self.barcode_re_2_old = self.barcode_re_2
        self.b_barcode_re_2 = False
        test_time = '%02d' % (datetime.now() - self.time2).seconds
        strSend = self.Build_Value(self.barcode_re_2,self.SN_Len) + 'FAIL' + test_time + self.PC_Name +ERROR
        try:
            if self.Send_COM(strSend + '\r\n'):
                self.txtSN_2.insert(1.0, self.barcode_re_2)
                self.txtContent.insert(1.0, str(datetime.now()) + '  -->  CAM_2 : ' + strSend + '\r\n')
            else:
                messagebox.showinfo('Please Open SFC COM', 'Please Open SFC COM')
        except:
            messagebox.showinfo('Please Open SFC COM', 'Please Open SFC COM')

    def Send_Result_3(self, ERROR):
        self.lb_Result3.config(text='FAIL', fg='red')
        #self.txtContent.insert(1.0, str(datetime.now()) + '  -->  CAM_3 : ' + self.barcode_re_3 + ' : fail' + '\r\n')
        self.barcode_re_3_old = self.barcode_re_3
        self.b_barcode_re_3 = False
        test_time = '%02d' % (datetime.now() - self.time3).seconds
        strSend = self.Build_Value(self.barcode_re_3,self.SN_Len) + 'FAIL' + test_time + self.PC_Name + ERROR
        try:
            if self.Send_COM(strSend + '\r\n'):
                self.txtSN_3.insert(1.0, self.barcode_re_3)
                self.txtContent.insert(1.0, str(datetime.now()) + '  -->  CAM_3 : ' + strSend + '\r\n')
            else:
                messagebox.showinfo('Please Open SFC COM', 'Please Open SFC COM')
        except:
            messagebox.showinfo('Please Open SFC COM', 'Please Open SFC COM')

    def Camera_1(self):
        try:
            cam_1_id = int(self.vcam1.get())
            cam_2_id = (self.vcam2.get())
            cam_3_id = (self.vcam3.get())
            if str(cam_1_id) == cam_2_id or str(cam_1_id) == cam_3_id: return False
            self.font = cv2.FONT_HERSHEY_SIMPLEX
            self.cap1 = cv2.VideoCapture(cam_1_id)
            id = self.cap1.get(cam_1_id)
            print('---------')
            print(id)
            #if id >= 0: return False
            #cv2.namedWindow('CAM_1', cv2.WINDOW_NORMAL)
            self.cap1.set(3, 640)
            self.cap1.set(4, 480)
            time.sleep(2)
            while self.cap1.isOpened() and self.Cam1_Open:
                ret, frame = self.cap1.read()
                # Our operations on the frame come here
                im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                try:
                    decodedObjects = pyzbar.decode(im)

                    self.barCode1 = ''.encode()
                    for decodedObject in decodedObjects:
                        points = decodedObject.polygon
                        # If the points do not form a quad, find convex hull
                        if len(points) > 4:
                            hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
                            hull = list(map(tuple, np.squeeze(hull)))
                        else:
                            hull = points;
                        # Number of points in the convex hull
                        n = len(hull)
                        # Draw the convext hull
                        for j in range(0, n):
                            cv2.line(frame, hull[j], hull[(j + 1) % n], (0, 0, 255), 3)
                        x = decodedObject.rect.left
                        y = decodedObject.rect.top
                        # typecode = decodedObject.type
                        # datacode = decodedObject.data
                        try:
                            self.barCode1 = decodedObject.data.decode(errors='ignore')
                            cv2.putText(frame, str(self.barCode1), (x, y), self.font, 1, (0, 0, 255), 2,
                                        cv2.LINE_AA)
                            # self.barCode = str(self.barCode, 'utf-8')
                            if re.search(symlist, str(self.barCode1)) != None: self.barCode1 = 'Wrong code'
                            if self.b_barcode_re_1 == False and self.barcode_re_1 != self.barCode1 and self.barcode_re_1_old != self.barCode1 and len(self.barCode1) >= 10 and self.barCode1.find(self.txtPre.get(1.0, 'end-1c')) == 0:
                                print('start re1')
                                self.time1 = datetime.now()
                                Thread(target=self.re1).start()
                                self.barcode_re_1_old = self.barcode_re_1
                        except Exception as e:
                            self.barCode1 = 'None'
                            print(e)
                            print('CAM_1 111111')
                            #continue

                except Exception as e:
                    decodedObjects = []
                    print(e)
                    print('CAM_1 22222')
                    #continue

                # Display the resulting frame

                cv2.imshow('CAM_1', frame)
                #print('1111111111111111111')
                #cv2.resize(frame, (300, 300))
                key = cv2.waitKey(1)
                if key & 0xFF == ord('s'):  # wait for 's' key to save
                    cv2.imwrite('Code.png', frame)
                # When everything done, release the capture
                # cap.release()
                # cv2.destroyAllWindows()
                time.sleep(0.3)
        except Exception as e:
            print(e)
            messagebox.showinfo('Camera index request', 'Please choose Camera Index')

    def Camera_2(self):
        try:
            cam_1_id = (self.vcam1.get())
            cam_2_id = int(self.vcam2.get())
            cam_3_id = (self.vcam3.get())
            if str(cam_2_id) == cam_1_id or str(cam_2_id) == cam_3_id: return False
            self.font = cv2.FONT_HERSHEY_SIMPLEX
            self.cap2 = cv2.VideoCapture(cam_2_id)
            id = self.cap2.get(cam_2_id)
            print(id)
            #if id >= 0: return False
            #cv2.namedWindow('CAM_2', cv2.WINDOW_NORMAL)
            self.cap2.set(3, 640)
            self.cap2.set(4, 480)
            time.sleep(2)
            while self.cap2.isOpened() and self.Cam2_Open:
                ret, frame2 = self.cap2.read()
                # Our operations on the frame come here
                im = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
                try:
                    decodedObjects = pyzbar.decode(im)
                    self.barCode2 = ''.encode()
                    for decodedObject in decodedObjects:
                        points = decodedObject.polygon
                        # If the points do not form a quad, find convex hull
                        if len(points) > 4:
                            hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
                            hull = list(map(tuple, np.squeeze(hull)))
                        else:
                            hull = points;
                        # Number of points in the convex hull
                        n = len(hull)
                        # Draw the convext hull
                        for j in range(0, n):
                            cv2.line(frame2, hull[j], hull[(j + 1) % n], (0, 0, 255), 3)
                        x = decodedObject.rect.left
                        y = decodedObject.rect.top
                        # typecode = decodedObject.type
                        # datacode = decodedObject.data

                        try:
                            self.barCode2 = decodedObject.data.decode(errors='ignore')
                            cv2.putText(frame2, str(self.barCode2), (x, y), self.font, 1, (0, 0, 255), 2,
                                        cv2.LINE_AA)
                            # self.barCode = str(self.barCode, 'utf-8')
                            if re.search(symlist, str(self.barCode2)) != None: self.barCode2 = 'Wrong code'
                            if self.b_barcode_re_2 == False and self.barcode_re_2 != self.barCode2 and self.barcode_re_2_old != self.barCode2 and len(self.barCode2) >= 10 and self.barCode2.find(self.txtPre.get(1.0, 'end-1c')) == 0:
                                print('start re2')
                                self.time2 = datetime.now()
                                Thread(target=self.re2).start()
                                self.barcode_re_2_old = self.barcode_re_2
                        except:
                            self.barCode2 = 'None'
                            print('CAM_2 111111')
                            #continue
                except Exception as e:
                    decodedObjects = []
                    print(e)
                    print('CAM_2 22222')
                    #continue

                # Display the resulting frame

                cv2.imshow('CAM_2', frame2)
                cv2.resize(frame2, (300, 300))
                key = cv2.waitKey(1)
                if key & 0xFF == ord('s'):  # wait for 's' key to save
                    cv2.imwrite('Code.png', frame2)
                # When everything done, release the capture
                # cap.release()
                # cv2.destroyAllWindows()
                time.sleep(0.3)
        except Exception as e:
            print(e)
            messagebox.showinfo('Camera index request', 'Please choose Camera Index')


    def Camera_3(self):
        try:
            cam_1_id = (self.vcam1.get())
            cam_2_id = (self.vcam2.get())
            cam_3_id = int(self.vcam3.get())
            if str(cam_3_id) == cam_1_id or str(cam_3_id) == cam_2_id: return False
            self.font = cv2.FONT_HERSHEY_SIMPLEX
            self.cap3 = cv2.VideoCapture(cam_3_id)
            id = self.cap3.get(cam_3_id)
            print(id)
            #if id >= 0: return False
            self.cap3.set(3, 640)
            self.cap3.set(4, 480)
            time.sleep(2)
            #cv2.namedWindow('CAM_3', cv2.WINDOW_NORMAL)
            while self.cap3.isOpened() and self.Cam3_Open:
                ret, frame3 = self.cap3.read()
                # Our operations on the frame come here
                im = cv2.cvtColor(frame3, cv2.COLOR_BGR2GRAY)
                try:
                    decodedObjects = pyzbar.decode(im)
                    self.barCode3 = ''.encode()
                    for decodedObject in decodedObjects:
                        points = decodedObject.polygon
                        # If the points do not form a quad, find convex hull
                        if len(points) > 4:
                            hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
                            hull = list(map(tuple, np.squeeze(hull)))
                        else:
                            hull = points;
                        # Number of points in the convex hull
                        n = len(hull)
                        # Draw the convext hull
                        for j in range(0, n):
                            cv2.line(frame3, hull[j], hull[(j + 1) % n], (0, 0, 255), 3)
                        x = decodedObject.rect.left
                        y = decodedObject.rect.top
                        # typecode = decodedObject.type
                        # datacode = decodedObject.data

                        try:
                            self.barCode3 = decodedObject.data.decode(errors='ignore')
                            cv2.putText(frame3, str(self.barCode3), (x, y), self.font, 1, (0, 0, 255), 2,
                                        cv2.LINE_AA)
                            # self.barCode = str(self.barCode, 'utf-8')
                            if re.search(symlist, str(self.barCode3)) != None: self.barCode3 = 'Wrong code'
                            if self.b_barcode_re_3 == False and self.barcode_re_3 != self.barCode3 and self.barcode_re_3_old != self.barCode3 and len(self.barCode3) >= 10 and self.barCode3.find(self.txtPre.get(1.0, 'end-1c')) == 0:
                                print('start re3')
                                self.time3 = datetime.now()
                                Thread(target=self.re3).start()
                                self.barcode_re_3_old = self.barcode_re_3
                        except:
                            self.barCode3 = 'None'
                            print('11111')
                            print(e)
                            #continue
                except Exception as e:
                    decodedObjects = []
                    print(e)
                    print('22222')
                    #continue

                # Display the resulting frame

                cv2.imshow('CAM_3', frame3)
                cv2.resize(frame3, (300, 300))
                key = cv2.waitKey(1)
                if key & 0xFF == ord('s'):  # wait for 's' key to save
                    cv2.imwrite('Code.png', frame3)
                # When everything done, release the capture
                # if key & 0xFF == ord('s'):
                # cap.release()
                # cv2.destroyAllWindows()
                time.sleep(0.3)
        except Exception as e:
            print(e)
            messagebox.showinfo('Camera index request', 'Please choose Camera Index')

    def COM_Control(self):
        if self.btnOpenCOM['text'] == 'SFIS_Closed':
            if len(self.PC_Name)==12:
                self.Open_COM()
            else:
                messagebox.showinfo('COMPUTER NAME', 'Kiểm tra tên máy tính đủ 12 ký tự ?\r\n\r\nCOMPUTER Name is not 12 digit ?')
        elif self.btnOpenCOM['text'] == 'SFIS_Opened':
            self.Close_COM()

    def COM_Control2(self):
        if self.btnOpenCOM2['text'] == 'Fixture_Closed':
            self.Open_COM_Fixture()
        elif self.btnOpenCOM2['text'] == 'Fixture_Opened':
            self.Close_COM_Fixture()

    def Open_COM(self):
        try:
            self.ser = serial.Serial(self.vconnected.get())
            print(self.ser.name)
            time.sleep(0.2)
            self.ser.flush()
            # self.ser.open()
            # self.ser.set_input_flow_control(enable=False)
            # self.ser.set_output_flow_control(enable=False)
            print('COM opened')
            self.btnOpenCOM.configure(fg='white', bg='green', text='SFIS_Opened')
        except Exception as e:
            print(e)
            messagebox.showinfo('Open fail', 'Open COM fail')

    def Close_COM(self):
        try:
            self.ser.flush()
            time.sleep(0.2)
            self.ser.close()
            print('COM closed')
            self.btnOpenCOM.configure(fg='white', bg='red', text='SFIS_Closed')
        except Exception as e:
            print(e)
        return True

    def Get_in(self):
        data_de = ''
        if not self.ser.is_open:
            print('re-open com')
            self.Open_COM()
        # time.sleep(0.1)
        # self.ser.flush()
        time.sleep(0.1)
        data_de = self.ser.read_all().strip()
        # time.sleep(0.1)
        self.ser.flush()
        if data_de != b'':
            print(self.ser.name)
            print('Fixture:' + str(data_de))
        return data_de

    def Send_COM(self, scmd):
        try:
            self.ser.write(scmd.encode())
            print('send to com ' + scmd + '\r\n')
            return True
        except Exception as e:
            print('send to com failed')
            print(e)
            messagebox.showinfo('Send SFC fail', 'Please open COM')
            return False


    def Open_COM_Fixture(self):
        try:
            self.ser_Fixture = serial.Serial(self.vconnected2.get())
            print(self.ser_Fixture.name)
            time.sleep(0.2)
            self.ser_Fixture.flush()
            self.btnOpenCOM2.configure(fg='white', bg='green', text='Fixture_Opened')
            self.Stared = True
            #print(self.Stared)
        except Exception as e:
            print(e)
            messagebox.showinfo('Open fail', 'Open COM_Fixture fail')

    def Close_COM_Fixture(self):
        try:
            self.ser_Fixture.flush()
            time.sleep(0.2)
            self.ser_Fixture.close()
            print('COM_Fixture closed')
            self.btnOpenCOM2.configure(fg='white', bg='red', text='Fixture_Closed')
            self.Stared = False
        except Exception as e:
            print(e)
        return True

    def Get_in_Fixture(self):
        data_de = ''
        if not self.ser_Fixture.is_open:
            print('re-open com_Fixture')
            self.Open_COM_Fixture()
        # time.sleep(0.1)
        # self.ser.flush()
        time.sleep(0.1)
        data_de = self.ser_Fixture.read_all().strip()
        # time.sleep(0.1)
        self.ser_Fixture.flush()
        if data_de != b'':
            print(self.ser_Fixture.name)
            print('Fixture:' + str(data_de))
        return data_de

    def Send_COM_Fixture(self, scmd):
        try:
            self.ser_Fixture.write(scmd.encode())
            print('send to com_Fixture ' + scmd + '\r\n')
            return True
        except Exception as e:
            print('send to com_Fixture failed')
            print(e)
            messagebox.showinfo('Send _Fixture fail', 'Please open COM_Fixture')
            return False

    def Build_Value(self,value, Sumlen):  # ---------modify value to send------------
        Fvalue = value.ljust(Sumlen, ' ')
        return Fvalue

root = Tk()
root.geometry("1130x450+50+50")
root.configure()  # (bg='lightskyblue')
app = Application(master=root)
app.mainloop()
