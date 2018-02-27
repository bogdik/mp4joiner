# -*- coding: utf-8 -*-
import os,wx,subprocess,ntpath,glob,threading

import time


class MyDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        self.index = 0
        self.prepDict = {}
        self.End=False
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.labelPath = wx.StaticText(self, wx.ID_ANY, "Path : ")
        self.textCtrlPath = wx.TextCtrl(self, wx.ID_ANY, "")
        self.button_1 = wx.Button(self, wx.ID_ANY, "Open...")
        self.button_1.Disable()
        self.ffmpeg = wx.StaticText(self, wx.ID_ANY, "FFMPEG :")
        self.info = wx.StaticText(self, wx.ID_ANY, "")
        self.gauge = wx.Gauge(self, range=20, size=(445, 25), style=wx.GA_HORIZONTAL)
        self.labelFile = wx.StaticText(self, wx.ID_ANY, "File List (mustbe *.mp4 or *.MP4):")
        self.listCtrlFile = wx.ListCtrl(self, wx.ID_ANY, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.listCtrlFile.InsertColumn(0, "Name", width=320)
        self.listCtrlFile.InsertColumn(1, "Info",width=125)
        self.buttonAccept = wx.Button(self, wx.ID_ANY, "JOIN")
        self.buttonAccept.Disable()
        self.buttonExit = wx.Button(self, wx.ID_ANY, "EXIT")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.OnButtonPath, self.button_1)
        self.Bind(wx.EVT_BUTTON, self.OnButtonAccept, self.buttonAccept)
        self.Bind(wx.EVT_BUTTON, self.OnButtonExit, self.buttonExit)

    def __set_properties(self):
        self.SetTitle("MP4joiner")
        self.textCtrlPath.SetBackgroundColour(wx.Colour(255, 255, 255))

    def check_ffmpeg(self):
        version = subprocess.Popen("ffmpeg -version", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        output, error = version.communicate()
        if output:
            return output.decode("utf-8").split("\n")[0]
        else:
            return False

    def change_ffmpeg(self,label,color):
        self.ffmpeg.SetLabel("FFMPEG : %s"%label)
        self.ffmpeg.SetForegroundColour(color)

    def change_info(self,label):
        self.ffmpeg.SetLabel(label)

    def joiner(self,inFiles,outFile):
        process = subprocess.Popen(
            'ffmpeg -i "concat:%s" -vcodec copy -bsf:a aac_adtstoasc "%s/%s"' % ('|'.join(inFiles), self.path, outFile), shell=True,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        output, error = process.communicate()
        self.End=True

    def prepare(self,file,indexWork):
        process = subprocess.Popen(
            u'ffmpeg -i "%s" -vcodec copy -bsf:v h264_mp4toannexb -f mpegts "%s/tmp_%s.ts"' % (file, self.path, indexWork), shell=True,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        output, error = process.communicate()
        self.prepDict[indexWork] = False

    def remove_tmp(self):
        for tmp in glob.glob("%s/tmp_*.ts" % self.path):
            os.remove(tmp)

    def workerPrepare(self):
        self.gauge.SetRange(len(self.files))
        indexWork = 0
        self.remove_tmp()
        for file in self.files:
            self.listCtrlFile.SetItem(indexWork, 1, "Preparing")
            self.prepDict[indexWork] = True
            self.info.SetLabel("Prepare: %s of %s" %(indexWork+1,len(self.files)))
            th = threading.Thread(target=self.prepare, args=[file, indexWork])
            th.daemon = True
            th.start()
            while self.prepDict[indexWork]:
                time.sleep(1)
            if os.path.isfile("%s/tmp_%s.ts" % (self.path, indexWork)):
                self.gauge.SetValue(indexWork+1)
                self.listCtrlFile.SetItem(indexWork, 1, "Prepared")
            else:
                self.listCtrlFile.SetItem(indexWork, 1, "Error")
            indexWork += 1
            if len(glob.glob("%s/tmp_*.ts" % self.path))==len(self.files):
                self.info.SetLabel("Joining, pleasewait")
                outfile="outFile_%s.mp4"%time.strftime("%Y-%m-%d_%H-%M-%S")
                th = threading.Thread(target=self.joiner, args=[glob.glob("%s/tmp_*.ts" % self.path), outfile])
                th.daemon = True
                th.start()
                while not self.End:
                    time.sleep(1)
                if os.path.isfile("%s/%s" % (self.path, outfile)):
                    self.info.SetLabel("All DONE!!!")
                    self.buttonAccept.Enable()
                else:
                    self.info.SetLabel("Fail on join(((")
                self.remove_tmp()


    def change_line(self,index,state):
        self.listCtrlFile.SetItem(index, 1, state)

    def add_line(self,file):
        self.listCtrlFile.InsertItem(self.index, file)
        self.listCtrlFile.SetItem(self.index, 1, "Waiting")
        self.index += 1

    def __do_layout(self):
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        footerSizer = wx.BoxSizer(wx.HORIZONTAL)
        pathSizer = wx.BoxSizer(wx.HORIZONTAL)
        pathSizer.Add(self.labelPath, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 2)
        pathSizer.Add(self.textCtrlPath, 1, wx.LEFT | wx.RIGHT | wx.EXPAND, 3)
        pathSizer.Add(self.button_1, 0, 0, 0)
        mainSizer.Add(pathSizer, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 4)
        mainSizer.Add(self.ffmpeg, 0, wx.ALL, 6)
        mainSizer.Add(self.info, 0,wx.ALL, 7)
        mainSizer.Add(self.gauge, 0, wx.ALL, 8)
        mainSizer.Add(self.labelFile, 0, wx.ALL, 9)
        mainSizer.Add(self.listCtrlFile, 10, wx.ALL | wx.EXPAND, 4)
        footerSizer.Add(self.buttonAccept, 1, wx.LEFT | wx.RIGHT | wx.EXPAND, 3)
        footerSizer.Add(self.buttonExit, 1, wx.LEFT | wx.RIGHT | wx.EXPAND, 3)
        mainSizer.Add(footerSizer, 1, wx.ALL | wx.EXPAND | wx.ALIGN_RIGHT, 2)
        self.SetSizer(mainSizer)
        mainSizer.Fit(self)
        self.Layout()
        self.version=self.check_ffmpeg()
        if self.version:
            self.change_ffmpeg(self.version.split("Copyright")[0],wx.BLACK)
            self.button_1.Enable()
        else:
            self.change_ffmpeg("Unknown,please install or put bin in main folder", wx.RED)

    def OnButtonPath(self, event):
        self.listCtrlFile.DeleteAllItems()
        self.index = 0
        self.info.SetLabel("")
        self.gauge.SetValue(0)
        dlg = wx.DirDialog(self, "Choose a directory:")
        if dlg.ShowModal() == wx.ID_OK:
            self.path=dlg.GetPath()
            self.files=glob.glob("%s/*.mp4"%self.path)
            if os.name != 'nt':
                self.files=self.files+glob.glob("%s/*.MP4" % self.path)
            self.textCtrlPath.Value = self.path
            if len(self.files):
                self.buttonAccept.Enable()
                for file in self.files:
                    self.add_line(ntpath.basename(file))
            else:
                self.buttonAccept.Disable()
        dlg.Destroy()

    def OnButtonAccept(self, event):
        self.buttonAccept.Disable()
        threading.Thread(target=self.workerPrepare).start()
        event.Skip()

    def OnButtonExit(self, event):
        self.Destroy()

if __name__ == "__main__":
    joiner = wx.App(0)
    mainDialog = MyDialog(None, wx.ID_ANY, "")
    joiner.SetTopWindow(mainDialog)
    mainDialog.Show()
    joiner.MainLoop()