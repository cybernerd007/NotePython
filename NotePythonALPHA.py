#!/usr/bin/python
import wx
import wx.lib.dialogs
import wx.stc as stc
import os

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        self.dirname = ''
        self.filename = ''
        self.leftMarginWidth = 25
        self.lineNumbersEnabled = True
        
        wx.Frame.__init__(self, parent, title=title, size=(800,600))
        self.control = stc.StyledTextCtrl(self, style=wx.TE_MULTILINE | wx.TE_WORDWRAP)
        
        self.control.Bind(stc.EVT_STC_UPDATEUI, self.Scroll)
        
        self.control.CmdKeyAssign(ord('='), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMIN)
        self.control.CmdKeyAssign(ord('-'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMOUT)
        
        self.control.SetViewWhiteSpace(False)
        self.control.SetMargins(5, 0)
        self.control.SetMarginType(1, stc.STC_MARGIN_NUMBER)
        self.control.SetMarginWidth(1, self.leftMarginWidth)
        
        self.CreateStatusBar()
        self.UpdateLineCol(self)
        self.StatusBar.SetBackgroundColour((220, 220, 220))
        
        filemenu = wx.Menu()
        menuNew = filemenu.Append(wx.ID_NEW, "&Novo", " Criar um novo documento")
        menuOpen = filemenu.Append(wx.ID_OPEN, "&Abrir", " Abrir um documento existente")
        menuSave = filemenu.Append(wx.ID_SAVE, "&Salvar", " Salvar o documento atual")
        menuSaveAs = filemenu.Append(wx.ID_SAVEAS, "Salvar &Como", " Salvar novo documento")
        filemenu.AppendSeparator()
        menuClose = filemenu.Append(wx.ID_EXIT, "&Fechar", "Fecha o programa")
        
        editmenu = wx.Menu()
        menuUndo = editmenu.Append(wx.ID_UNDO, "&Desfazer", "Desfazer a ultima ação")
        menuRedo = editmenu.Append(wx.ID_UNDO, "&Refazer", "Refazer a ultima ação")
        editmenu.AppendSeparator()
        menuSelectAll = editmenu.Append(wx.ID_SELECTALL, "&Selecionar Tudo", "Seleciona o texto todo")
        menuCopy = editmenu.Append(wx.ID_COPY, "&Copiar", "Copia o texto selecionado")
        menuCut = editmenu.Append(wx.ID_CUT, "&Recortar", "Recorta o texto selecionado")
        menuPaste = editmenu.Append(wx.ID_PASTE, "&Colar", "Cola o texto copiado")
        
        prefmenu = wx.Menu()
        menuLineNumbers = prefmenu.Append(wx.ID_ANY, "Alternar &números de linha", "Mostrar/Ocultar o número de linhas")
        
        helpmenu = wx.Menu()
        menuHowTo = helpmenu.Append(wx.ID_ANY, "&Como...", "Obtenha ajuda usando o editor de texto")
        helpmenu.AppendSeparator()
        menuAbout = helpmenu.Append(wx.ID_ABOUT, "&Sobre", "Leia sobre o editor e sua criação")
        
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&Arquivo")
        menuBar.Append(editmenu, "&Editar")
        menuBar.Append(prefmenu, "&Preferências")
        menuBar.Append(helpmenu, "&Ajuda")
        self.SetMenuBar(menuBar)
        
        self.Bind(wx.EVT_MENU, self.OnNew, menuNew)
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnSave, menuSave)
        self.Bind(wx.EVT_MENU, self.OnSaveAs, menuSaveAs)
        self.Bind(wx.EVT_MENU, self.OnClose, menuClose)
        
        self.Bind(wx.EVT_MENU, self.OnUndo, menuUndo)
        self.Bind(wx.EVT_MENU, self.OnRedo, menuRedo)
        self.Bind(wx.EVT_MENU, self.OnSelectAll, menuSelectAll)
        self.Bind(wx.EVT_MENU, self.OnCopy, menuCopy)
        self.Bind(wx.EVT_MENU, self.OnCut, menuCut)
        self.Bind(wx.EVT_MENU, self.OnPaste, menuPaste)
        
        self.Bind(wx.EVT_MENU, self.OnToggleLineNumbers, menuLineNumbers)
        
        self.Bind(wx.EVT_MENU, self.OnHowTo, menuHowTo)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        
        self.control.Bind(wx.EVT_KEY_UP, self.UpdateLineCol)
        self.control.Bind(wx.EVT_CHAR, self.OnCharEvent)
        
        self.Show()

    def Scroll(self,event):
        x = self.control.GetFirstVisibleLine()
        y = self.control.LinesOnScreen()
        x = x+y
        x = len(str(x))
        self.control.SetMarginWidth(1, x*16)
    
    def OnNew(self, e):
        self.filename = ''
        self.control.SetValue("")
    
    def OnOpen(self, e):
        try:
            dlg = wx.FileDialog(self, "Abrir arquivo", self.dirname, "", "*.*", wx.FD_OPEN)
            if (dlg.ShowModal() == wx.ID_OK):
                self.filename = dlg.GetFilename()
                self.dirname = dlg.GetDirectory()
                f = open(os.path.join(self.dirname, self.filename), 'r')
                self.control.SetValue(f.read())
                f.close()
            dlg.Destroy()
        except:
            dlg = wx.MessgeDialog(self, "Não foi possivel abrir o arquivo", "Erro", wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            
    def OnSave(self, e):
        try:
            f = open(os.path.join(self.dirname, self.filename), 'w')
            f.write(self.control.GetValue())
            f.close()
        except:
            try:
                 dlg = wx.FileDialog(self, "Salvar arquivo como", self.dirname, "Sem Titulo", "*.*", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
                 if (dlg.ShowModal() == wx.ID_OK):
                     self.filename = dlg.GetFilename()
                     self.dirname = dlg.GetDirectory()
                     f = open(os.path.join(self.dirname, self.filename), 'w')
                     f.write(self.control.GetValue())
                     f.close()
                 dlg.Destroy()
            except:
                pass
            
    def OnSaveAs(self, e):
        try:
            dlg = wx.FileDialog(self, "Salvar arquivo como", self.dirname, "Sem Titulo", "*.*", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
            if (dlg.ShowModal() == wx.ID_OK):
                self.filename = dlg.GetFilename()
                self.dirname = dlg.GetDirectory()
                f = open(os.path.join(self.dirname, self.filename), 'w')
                f.write(self.control.GetValue())
                f.close()
            dlg.Destroy()
        except:
            pass
                
    def OnClose(self, e):
        self.Close(True)
        
    def OnUndo(self, e):
        self.control.Undo()
        
    def OnRedo(self, e):
        self.control.Redo()
        
    def OnSelectAll(self, e):
       self.control.SelectAll()
        
    def OnCopy(self, e):
        self.control.copy()
        
    def OnCut(self, e):
        self.control.Cut()
        
    def OnPaste(self,e):
        self.control.Paste()
        
    def OnToggleLineNumbers(self, e):
        if(self.lineNumbersEnabled):
           self.control.SetMarginWidth(1, 0)
           self.lineNumbersEnabled = False
        else:
           self.control.SetMarginWidth(1, self.leftMarginWidth)
           self.lineNumbersEnabled = True
           
    def OnHowTo(self, e):
        dlg = wx.lib.dialogs.ScrolledMessageDialog(self, "Aqui e como", "Como...")
        dlg.ShowModal()
        dlg.Destroy()
        
    def OnAbout(self, e):
        dlg = wx.MessageDialog(self, "Meu avançado editor de texto foi feito com python e wx", "Sobre")
        dlg.ShowModal()
        dlg.Destroy()
    
    def UpdateLineCol(self, e):
        line = self.control.GetCurrentLine() + 1
        col = self.control.GetColumn(self.control.GetCurrentPos())
        stat = "Linha %s, Coluna %s" % (line, col)
        self.StatusBar.SetStatusText(stat, 0)
    
    def OnCharEvent(self, e):
        keycode = e.GetKeyCode()
        altDown = e.AltDown()
        if (keycode == 14): # Ctrl + N
            self.OnNew(self)
        elif (keycode == 15): # Ctrl + O
            self.OnOpen(self)
        elif (keycode == 19): # Ctrl + S
            self.Save(self)
        elif (AltDown and (keycode == 115)): # Alt + S
            self.OnSaveAs(self)
        elif (keycode == 23): # Ctrl + W
            self.OnClose(self)
        elif (keycode == 340): # F1
            self.OnHowTo(self)
        elif (keycode == 341): # F2
            self.OnAbout(self)
        else:
            e.Skip()
    
app = wx.App()
frame = MainWindow(None, "NotePython")
app.MainLoop()