# -*- coding: utf-8 -*-
import os,wx,subprocess,ntpath,glob,threading,sys,collections,time,base64
from wx.lib.embeddedimage import PyEmbeddedImage

icon="""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"""

_ntuple_diskusage = collections.namedtuple('usage', 'total used free')

if hasattr(os, 'statvfs'):  # POSIX
    def disk_usage(path):
        st = os.statvfs(path)
        free = st.f_bavail * st.f_frsize
        total = st.f_blocks * st.f_frsize
        used = (st.f_blocks - st.f_bfree) * st.f_frsize
        return _ntuple_diskusage(total, used, free)

elif os.name == 'nt':       # Windows
    import ctypes
    import sys

    def disk_usage(path):
        _, total, free = ctypes.c_ulonglong(), ctypes.c_ulonglong(), \
                           ctypes.c_ulonglong()
        if sys.version_info >= (3,) or isinstance(path, unicode):
            fun = ctypes.windll.kernel32.GetDiskFreeSpaceExW
        else:
            fun = ctypes.windll.kernel32.GetDiskFreeSpaceExA
        ret = fun(path, ctypes.byref(_), ctypes.byref(total), ctypes.byref(free))
        if ret == 0:
            raise ctypes.WinError()
        used = total.value - free.value
        return _ntuple_diskusage(total.value, used, free.value)
else:
    raise NotImplementedError("platform not supported")

def bytes2human(n):
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i+1)*10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n


class RedirectText(object):
    def __init__(self, aWxTextCtrl):
        self.out = aWxTextCtrl

    def write(self, string):
        self.out.WriteText(string)

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
        self.labelFile = wx.StaticText(self, wx.ID_ANY, "File List (must be *.mp4 or *.MP4):")
        self.icon = PyEmbeddedImage(icon)
        self.icon = self.icon.GetIcon()
        self.listCtrlFile = wx.ListCtrl(self, wx.ID_ANY, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.listCtrlFile.InsertColumn(0, "Name", width=320)
        self.listCtrlFile.InsertColumn(1, "Info",width=125)
        self.buttonAccept = wx.Button(self, wx.ID_ANY, "JOIN")
        self.buttonAccept.Disable()
        self.buttonExit = wx.Button(self, wx.ID_ANY, "EXIT")
        self.log = wx.TextCtrl(self, wx.ID_ANY, size=(300, 100),style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.OnButtonPath, self.button_1)
        self.Bind(wx.EVT_BUTTON, self.OnButtonAccept, self.buttonAccept)
        self.Bind(wx.EVT_BUTTON, self.OnButtonExit, self.buttonExit)

    def __set_properties(self):
        self.SetTitle("MP4joiner")
        self.textCtrlPath.SetBackgroundColour(wx.Colour(255, 255, 255))

    def check_ffmpeg(self):
        version = subprocess.Popen("ffmpeg -version", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output, error = version.communicate()
        while True:
            out = version.stderr.read()
            if not out:
                break
            print (out)
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
        str_files='|'.join(inFiles)
        process = subprocess.Popen(
            'ffmpeg -i "concat:%s" -vcodec copy -bsf:a aac_adtstoasc "%s/%s"' % (str_files.encode('mbcs'), self.path.decode('utf-8').encode('mbcs'), outFile), shell=True,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        inp,output, error = process.communicate()
        while True:
            output = process.stderr.read()
            if not output:
                print ('[End join]')
                break
            print (output)
        if 'failed' in error:
            self.info.SetLabel("Fail on join(((")
            self.info.SetForegroundColour(wx.GREEN)
        self.End=True

    def prepare(self,file,indexWork):
        process = subprocess.Popen(
            'ffmpeg -i "%s" -vcodec copy -bsf:v h264_mp4toannexb -f mpegts "%s/tmp_%s.ts"' % ( file.encode('mbcs'),self.path.decode('utf-8').encode('mbcs'), indexWork), shell=True,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        #stdin,stdout, stderr, = process.communicate()
        while True:
            output = process.stderr.read()
            if not output:
                print ('[End prepare]')
                break
            print (output)
        self.prepDict[indexWork] = False

    def remove_tmp(self):
        for tmp in glob.glob("%s/tmp_*.ts" % self.path.decode('utf-8')):
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
            if os.path.isfile("%s/tmp_%s.ts" % (self.path.decode('utf-8'), indexWork)):
                self.gauge.SetValue(indexWork+1)
                self.listCtrlFile.SetItem(indexWork, 1, "Prepared")
            else:
                self.listCtrlFile.SetItem(indexWork, 1, "Error")
            indexWork += 1
            if len(glob.glob("%s/tmp_*.ts" % self.path.decode('utf-8')))==len(self.files):
                self.info.SetLabel("Joining, pleasewait")
                outfile="outFile_%s.mp4"%time.strftime("%Y-%m-%d_%H-%M-%S")
                th = threading.Thread(target=self.joiner, args=[glob.glob("%s/tmp_*.ts" % self.path.decode('utf-8')), outfile])
                th.daemon = True
                th.start()
                while not self.End:
                    time.sleep(1)
                if os.path.isfile("%s/%s" % (self.path.decode('utf-8'), outfile)):
                    if not 'Fail' in self.info.GetLabel():
                        self.info.SetLabel("All DONE!!!")
                        self.info.SetForegroundColour(wx.GREEN)
                    self.gauge.SetValue(0)
                    self.buttonAccept.Enable()
                else:
                    self.info.SetLabel("Fail on join(((")
                    self.info.SetForegroundColour(wx.RED)
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
        self.SetIcon(self.icon)
        pathSizer.Add(self.labelPath, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 2)
        pathSizer.Add(self.textCtrlPath, 1, wx.LEFT | wx.RIGHT | wx.EXPAND, 3)
        pathSizer.Add(self.button_1, 0, 0, 0)
        mainSizer.Add(pathSizer, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 4)
        mainSizer.Add(self.ffmpeg, 0, wx.ALL, 6)
        mainSizer.Add(self.info, 0,wx.ALL, 7)
        mainSizer.Add(self.gauge, 0, wx.ALL, 8)
        mainSizer.Add(self.labelFile, 0, wx.ALL, 9)
        mainSizer.Add(self.listCtrlFile, 10, wx.ALL | wx.EXPAND, 4)
        mainSizer.Add(self.log, 5, wx.ALL | wx.EXPAND, 4)
        footerSizer.Add(self.buttonAccept, 1, wx.LEFT | wx.RIGHT | wx.EXPAND, 3)
        footerSizer.Add(self.buttonExit, 1, wx.LEFT | wx.RIGHT | wx.EXPAND, 3)
        mainSizer.Add(footerSizer, 1, wx.ALL | wx.EXPAND | wx.ALIGN_RIGHT, 2)
        self.SetSizer(mainSizer)
        mainSizer.Fit(self)
        self.Layout()
        redir = RedirectText(self.log)
        sys.stdout = redir
        sys.stderror = redir
        self.version=self.check_ffmpeg()
        if self.version:
            self.change_ffmpeg(self.version.split("Copyright")[0],wx.BLACK)
            self.button_1.Enable()
        else:
            self.change_ffmpeg("Unknown,please install or put bin in main folder", wx.RED)

    def checkNeedSize(self):
        if os.name != 'nt':
            usage = disk_usage(self.path[0])
        else:
            usage = disk_usage('%s:\\' % self.path[0])
        need=sum(map(os.path.getsize, self.files))*2
        if need>usage.free:
            self.info.SetLabel("No need free disk space (need %s, free %s)" %(bytes2human(need),bytes2human(usage.free)))
            self.info.SetForegroundColour(wx.RED)
            self.buttonAccept.Disable()

    def OnButtonPath(self, event):
        self.listCtrlFile.DeleteAllItems()
        self.index = 0
        self.info.SetLabel("")
        self.gauge.SetValue(0)
        dlg = wx.DirDialog(self, "Choose a directory:")
        if dlg.ShowModal() == wx.ID_OK:
            self.path=dlg.GetPath().encode('utf-8')
            self.files=glob.glob("%s/*.mp4"%self.path.decode('utf-8'))
            if os.name != 'nt':
                self.files=self.files+glob.glob("%s/*.MP4" % self.path.decode('utf-8'))
            self.textCtrlPath.Value = self.path.decode('utf-8')
            if len(self.files):
                self.buttonAccept.Enable()
                for file in self.files:
                    self.add_line(ntpath.basename(file))
            else:
                self.buttonAccept.Disable()
            self.checkNeedSize()
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
