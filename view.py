# -'''- coding: utf-8 -'''-

"""
    AnonymousWatcher
    Copyright (C) 2019  Ardyn von Eizbern, SeaBao(tony24862486@gmail.com)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import wx
import cv2
import os.path
import datetime
import imutils
import presentation


class MainWindow(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="防盜監視器", size=(1600, 1200))
        self.CreateStatusBar()
        xmenu = wx.Menu()
        self.panel = wx.Panel(self)
        menuLogin = xmenu.Append(wx.ID_ANY, "&登入", "登入電子信箱與電話")
        xmenu.AppendSeparator()
        menuSendMail = xmenu.Append(wx.ID_ANY, "&發送訊息", "發送電子郵件")
        xmenu.AppendSeparator()
        menuAbout = xmenu.Append(wx.ID_ABOUT, "&關於", "程式資訊")
        xmenu.AppendSeparator()
        menuExit = xmenu.Append(wx.ID_EXIT, "&退出", "終止程式")

        self.fSizer = wx.BoxSizer()
        menuBar = wx.MenuBar()
        menuBar.Append(xmenu, "&選單")
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnLogin, menuLogin)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnSendMail, menuSendMail)

        self.capture = cv2.VideoCapture(0)
        self.cap = ShowCapture(self.panel, self.capture)

        self.panel.SetSizer(self.fSizer)
        self.fSizer.Fit(self.panel)
        self.Show(True)

    def OnExit(self, e):
        self.Close(True)     
        self.capture.release()
        cv2.destroyAllWindows()

    def OnAbout(self, e):
        dig = wx.MessageDialog(self, "一個防盜監視器", "關於防盜監視器")
        dig.ShowModal()
        dig.Destroy()

    def OnLogin(self, e):
        dig = MultiInputDialog(parent = self.panel)
    
    def OnSendMail(self, e):
        presentation.sendWarningMail(self.cap.nstr)


class MultiInputDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, title = "輸入資料", size = (800, 300))
        self.panel = wx.Panel(self,wx.ID_ANY)
        self.elabel = wx.StaticText(self.panel, label="電子郵件：", size = (300, -1))
        self.einpuline = wx.TextCtrl(self.panel, size = (250, -1))
        #self.dlabel = wx.StaticText(self.panel, label="電話號碼：", size = (300, -1))
        #self.dinpuline = wx.TextCtrl(self.panel, size = (250, -1))
        self.confirmBtn = wx.Button(self.panel, wx.ID_ANY, "確認")
        self.cancelBtn = wx.Button(self.panel, wx.ID_ANY, '取消')
        self.Bind(wx.EVT_BUTTON, self.OnConfirm, self.confirmBtn)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, self.cancelBtn)

        self.xSizer = wx.BoxSizer()
        self.fSizer = wx.GridSizer(rows = 2, cols = 2, vgap = 1, hgap = 1)
        self.fSizer.Add(self.elabel, 1, wx.ALIGN_CENTER)
        self.fSizer.Add(self.einpuline, 1, wx.ALIGN_CENTER)
        #self.fSizer.Add(self.dlabel, 1, wx.ALIGN_CENTER)
        #self.fSizer.Add(self.dinpuline, 1, wx.ALIGN_CENTER)
        self.fSizer.Add(self.confirmBtn, 1, wx.ALIGN_CENTER)
        self.fSizer.Add(self.cancelBtn, 1, wx.ALIGN_CENTER)
        self.xSizer.Add(self.fSizer, 1, wx.ALIGN_CENTER)
        self.panel.SetSizer(self.xSizer)
        self.xSizer.Fit(self.panel)
        self.Show(True)

    def OnConfirm(self, e):
        self.evalue = self.einpuline.GetValue()
        presentation.setData(self.evalue)
        self.Close(True)

    def OnCancel(self, e):
        self.Close(True)

class ShowCapture(wx.Panel):
    def __init__(self, parent, capture):
        wx.Panel.__init__(self, parent, wx.ID_ANY, size=(1600,1200))
        self.prevFrame = None
        self.detectedTime = None

        self.capture = capture
        ret, frame = self.capture.read()

        frame = imutils.resize(frame, height = (1000))

        height, width = frame.shape[:2]
        parent.SetSize((width, height))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.bmp = wx.Bitmap.FromBuffer(width, height, frame)
        self.timer = wx.Timer(self)
        self.timer.Start(1000./24)
        self.nstr = ""
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.NextFrame)

    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self)
        dc.DrawBitmap(self.bmp, 0, 0)

    def NextFrame(self, event):
        ret, frame = self.capture.read()
        frame = imutils.resize(frame, height = (1000))
        text = "Safe"
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        if (self.prevFrame is None):
            self.prevFrame = gray
        diffFrame = cv2.absdiff(self.prevFrame, gray)
        threshold = cv2.threshold(diffFrame, 25, 255, cv2.THRESH_BINARY)[1]
        threshold = cv2.dilate(threshold, None, iterations=5)
        contours = cv2.findContours(
            threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
                
        

        for c in contours:
            if cv2.contourArea(c) < 20000:
                continue
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = "Detected!"
            if (self.detectedTime is None or (datetime.datetime.now() - self.detectedTime).seconds > 10):
                self.detectedTime = datetime.datetime.now()
                self.extension = self.detectedTime.strftime("%Y-%m-%d %H:%M:%S") + ".jpg"
                cv2.imwrite(os.path.abspath(self.extension), frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
                self.nstr = self.extension
        
        cv2.putText(frame, "Room Status: {}".format(text), (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, datetime.datetime.now().strftime("Current Time: %Y-%m-%d %H:%M:%S"),
                    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.bmp.CopyFromBuffer(frame)
            self.Refresh()
        
        self.prevFrame = gray

