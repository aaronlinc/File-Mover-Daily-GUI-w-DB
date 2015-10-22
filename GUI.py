import wx, os, shutil, datetime, recordDB

class Frame(wx.Frame):
    def __init__(self, title):

        wx.Frame.__init__(self, None, title=title, size=(600,300))
        self.panel = wx.Panel(self)

        #Setting Source and Destination paths to empty strings.
        self.source = ''
        self.destination = ''


        instructions = wx.StaticText(self.panel, label='All files created or modified today are'
                      '             moved to destination folder.', pos=(175,20))
        instructions.Wrap(250)
        
        #Files to check box
        wx.StaticText(self.panel, label='Choose a Folder for Source', pos=(50,70))
        self.browseBox = wx.TextCtrl(self.panel, size=(500, -1), pos=(50,90))
        self.browse = wx.Button(self.panel, label = 'Browse', pos = (460,120))

        #Destination for files
        wx.StaticText(self.panel, label='Choose a Folder for destination', pos=(50,150))
        self.browseBox2 = wx.TextCtrl(self.panel, size=(500, -1), pos=(50,170))
        self.browse2 = wx.Button(self.panel, label = 'Browse', pos = (460,200))

        self.browseBox.AppendText(self.source)
        self.browseBox2.AppendText(self.destination)

        #Button to initialize
        self.start = wx.Button(self.panel, label = 'Check', pos = (250,235))

        #Binding Buttons to File Functions
        self.browse.Bind(wx.EVT_BUTTON, self.sourcePath)
        self.browse2.Bind(wx.EVT_BUTTON, self.destPath)
        self.start.Bind(wx.EVT_BUTTON, self.moveFiles)

        #Display last time transfer happened
        self.time = recordDB.viewLast()
        self.timestr = wx.StaticText(self.panel, label= self.time, pos=(150,200))
        


    #Gets User Chosen Source Path       
    def sourcePath(self, event):
        self.browseBox.Clear()
        dirBox = wx.DirDialog(self, "Choose Folder")
        if dirBox.ShowModal() == wx.ID_OK:
            self.source = (dirBox.GetPath())
            self.browseBox.AppendText(self.source)
            


    #Gets User Chosen Destination Path
    def destPath(self, event):
        self.browseBox2.Clear()
        dirBox = wx.DirDialog(self, "Choose Folder")
        if dirBox.ShowModal() == wx.ID_OK:
            self.destination = (dirBox.GetPath())
            self.browseBox2.AppendText(self.destination)
            
        

    # Moving only files made/modified today from Source to Destination
    def moveFiles(self, event):
        #Error Checking
        if self.source == '' and self.destination == '':
            return
        if self.source == self.destination:
            return
        
        sourceFiles = os.listdir(self.source)
        counter = 0
        for files in sourceFiles:
            if self.fileModDate(os.path.join(self.source, files)):
                shutil.move(os.path.join(self.source, files),
                            os.path.join(self.destination, files))
                print("Moved to Home Office: {}/{}".format(self.source, files))
                counter += 1
        self.timestr.Destroy()

        if counter == 0:
            self.time = "No Transfers were made. {}".format(recordDB.viewLast())
            self.timestr = wx.StaticText(self.panel, label= self.time, pos=(170,200)
                                         ,style = wx.ALIGN_CENTRE)
        else:
            recordDB.newRecordTime()
            self.time = recordDB.viewLast()
            self.timestr = wx.StaticText(self.panel, label= self.time, pos=(150,200)
                                         ,style = wx.ALIGN_CENTRE)
        self.timestr.Wrap(300)

        #Clear textCtrl
        self.browseBox.Clear()
        self.browseBox2.Clear()


    # Returns whether a file was modified today (true) or not (false)    
    def fileModDate(self, filename):
        date = os.path.getmtime(filename)

        locTime = datetime.datetime.now().strftime("%y%d")
        fileDate = datetime.datetime.fromtimestamp(date).strftime("%y%d")

        if locTime == fileDate:
            return True
        else:
            return False
    

def main():
        
    app = wx.App()
    frame = Frame("Move Files")
    frame.Show()
    app.MainLoop()

if __name__ == "__main__": main()
