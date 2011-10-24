# -*- coding: utf-8 -*-
"""
Copyright 2009 iACT, universite de Montreal, Jean Piche, Olivier Belanger, Dominic Thibault

This file is part of Cecilia 4.

Cecilia 4 is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Cecilia 4 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Cecilia 4.  If not, see <http://www.gnu.org/licenses/>.
"""

import wx, sys, os
import  wx.lib.scrolledpanel as scrolled
from constants import *
import CeciliaLib
from Widgets import *

PADDING = 10

class PreferenceFrame(wx.Frame):
    def __init__(self, parent):
        style = ( wx.CLIP_CHILDREN | wx.FRAME_NO_TASKBAR | wx.FRAME_SHAPED | wx.NO_BORDER | wx.FRAME_FLOAT_ON_PARENT )
        wx.Frame.__init__(self, parent, title='', style = style)
        self.parent = parent

        self.font = wx.Font(MENU_FONT, wx.NORMAL, wx.NORMAL, wx.NORMAL, face=FONT_FACE)

        if CeciliaLib.getVar("systemPlatform")  in ['win32', 'linux2']:
            self.SetSize((350, 328))
            
        if wx.Platform == '__WXGTK__':
            self.Bind(wx.EVT_WINDOW_CREATE, self.SetRoundShape)
        else:
            self.SetRoundShape()

        panel = wx.Panel(self, -1)
        w, h = self.GetSize()
        panel.SetBackgroundColour(BACKGROUND_COLOUR)
        box = wx.BoxSizer(wx.VERTICAL)

        title = FrameLabel(panel, "Cecilia Preferences", size=(w-2, 24))
        box.Add(title, 0, wx.ALL, 1)

        headerSizer = wx.FlexGridSizer(1,2,5,5)
        self.panelTitles = ['  Paths', '  Audio', '    Midi', 'audioServer', 'Cecilia']
        choice = PreferencesRadioToolBox(panel, size=(125,25), outFunction=self.onPageChange)
        self.panelTitle = wx.StaticText(panel, -1, 'Paths')
        self.panelTitle.SetFont(self.font)
        headerSizer.AddMany([(choice, 0, wx.LEFT, 1), (self.panelTitle, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 90)])
                                        
        box.Add(headerSizer, 0, wx.ALL, 1)
        box.Add(wx.StaticLine(panel, -1, size=(346, 1)), 0, wx.LEFT, 2)
        box.AddSpacer(5)
        
        self.panelsBox = wx.BoxSizer(wx.HORIZONTAL)
        self.panels = []
        pathsPane = self.createPathsPanel(panel)
        audioPane = self.createAudioPanel(panel)
        audioPane.Hide()
        midiPane = self.createMidiPanel(panel)
        midiPane.Hide()
        csoundPane = self.createAudioServerPanel(panel)
        csoundPane.Hide()
        ceciliaPane = self.createCeciliaPanel(panel)
        ceciliaPane.Hide()
        self.panels.append(pathsPane)
        self.panels.append(audioPane)
        self.panels.append(midiPane)
        self.panels.append(csoundPane)
        self.panels.append(ceciliaPane)
        self.currentPane = 0
        self.panelsBox.Add(self.panels[self.currentPane])
        box.Add(self.panelsBox, 0, wx.TOP, 10)
        
        box.AddSpacer(10)
        closerBox = wx.BoxSizer(wx.HORIZONTAL)
        closer = CloseBox(panel, outFunction=self.onClose)
        closerBox.Add(closer, 0, wx.LEFT, 290)
        box.Add(closerBox, 0, wx.TOP, 80)

        panel.SetSizerAndFit(box)

    def SetRoundShape(self, event=None):
        w, h = self.GetSizeTuple()
        self.SetShape(GetRoundShape(350, 328, 1))

    def onClose(self, event=None):
        CeciliaLib.writeVarToDisk()
        self.Destroy()

    def onPageChange(self, index):
        self.panels[self.currentPane].Hide()    
        self.panels[index].Show()        
        self.panels[index].SetPosition(self.panelsBox.GetPosition())
        self.panelsBox.Replace(self.panels[self.currentPane], self.panels[index])
        self.currentPane = index
        self.panelTitle.SetLabel(self.panelTitles[self.currentPane])
        self.Refresh()
                    
    def createPathsPanel(self, panel):
        pathsPanel = wx.Panel(panel)
        pathsPanel.SetBackgroundColour(BACKGROUND_COLOUR)
        gridSizer = wx.FlexGridSizer(2,2,2,5)

        #Soundfile Player
        textSfPlayerLabel = wx.StaticText(pathsPanel, -1, 'Soundfile Player :')
        textSfPlayerLabel.SetFont(self.font)       
        self.textSfPlayerPath = wx.StaticText(pathsPanel, -1, CeciliaLib.getVar("soundfilePlayer"), style=wx.SIMPLE_BORDER)
        self.textSfPlayerPath.SetFont(self.font)       
        self.textSfPlayerPath.SetForegroundColour((50,50,50))
        buttonSfPlayerPath = CloseBox(pathsPanel, outFunction=self.changeSfPlayer, label='Set...')           

        #Soundfile Editor
        textSfEditorLabel = wx.StaticText(pathsPanel, -1, 'Soundfile Editor :')
        textSfEditorLabel.SetFont(self.font)       
        self.textSfEditorPath = wx.StaticText(pathsPanel, -1, CeciliaLib.getVar("soundfileEditor"), style=wx.SIMPLE_BORDER)
        self.textSfEditorPath.SetFont(self.font)       
        self.textSfEditorPath.SetForegroundColour((50,50,50))
        buttonSfEditorPath = CloseBox(pathsPanel, outFunction=self.changeSfEditor, label='Set...')           

        textPrefPathLabel = wx.StaticText(pathsPanel, -1, 'Preferred paths :')
        textPrefPathLabel.SetFont(self.font)       
        self.textPrefPath = wx.TextCtrl(pathsPanel, -1, CeciliaLib.getVar("prefferedPath"), size=(274,16), style=wx.TE_PROCESS_ENTER|wx.NO_BORDER)
        self.textPrefPath.SetFont(self.font)       
        self.textPrefPath.Bind(wx.EVT_TEXT_ENTER, self.handleEditPrefPath)
        self.textPrefPath.SetForegroundColour((50,50,50))
        self.textPrefPath.SetBackgroundColour("#999999")
        buttonPrefPath = CloseBox(pathsPanel, outFunction=self.addPrefPath, label='Add...')           

        gridSizer.AddMany([ 
                            (textSfPlayerLabel, 0, wx.EXPAND | wx.LEFT, PADDING),
                            (wx.StaticText(pathsPanel, -1, ''), 0, wx.EXPAND | wx.LEFT, 5),
                            (self.textSfPlayerPath, 0, wx.EXPAND | wx.LEFT | wx.ALIGN_CENTER_VERTICAL, PADDING),
                            (buttonSfPlayerPath, 0, wx.RIGHT, 10),
                            (textSfEditorLabel, 0, wx.EXPAND | wx.LEFT | wx.TOP, PADDING),
                            (wx.StaticText(pathsPanel, -1, ''), 0, wx.EXPAND | wx.LEFT, 5),
                            (self.textSfEditorPath, 0, wx.EXPAND | wx.LEFT | wx.ALIGN_CENTER_VERTICAL, PADDING),
                            (buttonSfEditorPath, 0, wx.RIGHT, 10),
                            (textPrefPathLabel, 0, wx.EXPAND | wx.LEFT | wx.TOP, PADDING),
                            (wx.StaticText(pathsPanel, -1, ''), 0, wx.EXPAND | wx.LEFT, 5),
                            (self.textPrefPath, 0,  wx.LEFT | wx.ALIGN_CENTER_VERTICAL, PADDING),
                            (buttonPrefPath, 0, wx.RIGHT, 10),
                            ])
        gridSizer.AddGrowableCol(0, 1)
        
        self.textPrefPath.Navigate()
        panel.SetSizerAndFit(gridSizer)
        return pathsPanel

    def createCeciliaPanel(self, panel):
        ceciliaPanel = wx.Panel(panel)
        ceciliaPanel.SetBackgroundColour(BACKGROUND_COLOUR)
        gridSizer = wx.FlexGridSizer(3,3,10,3)

        textTotalTime = wx.StaticText(ceciliaPanel, 0, 'Total time default (sec) :')
        textTotalTime.SetFont(self.font)       
        self.choiceTotalTime = CustomMenu(ceciliaPanel, 
                                    choice= ["10.0", "30.0", "60.0", "120.0", "300.0", "600.0", "1200.0", "2400.0", "3600.0"], 
                                    init=str(CeciliaLib.getVar("defaultTotalTime")), outFunction=self.changeDefaultTotalTime)

        textUseTooltips = wx.StaticText(ceciliaPanel, 0, 'Use tooltips :')
        textUseTooltips.SetFont(self.font)       
        self.tooltipsToggle = Toggle(ceciliaPanel, CeciliaLib.getVar("useTooltips"), outFunction=self.enableTooltips)                              

        textgraphTexture = wx.StaticText(ceciliaPanel, 0, 'Use grapher texture :')
        textgraphTexture.SetFont(self.font)       
        self.textureToggle = Toggle(ceciliaPanel, CeciliaLib.getVar("graphTexture"), outFunction=self.enableGraphTexture)                              

        gridSizer.AddMany([ 
                            (textTotalTime, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, PADDING),
                            (wx.StaticText(ceciliaPanel, -1, '', size=(86,-1)), 1, wx.EXPAND),
                            (self.choiceTotalTime, 0, wx.ALIGN_CENTER_VERTICAL),
                            (textUseTooltips, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, PADDING),
                            (wx.StaticText(ceciliaPanel, -1, ''), 1, wx.EXPAND),
                            (self.tooltipsToggle, 0, wx.ALIGN_CENTER_VERTICAL),
                            (textgraphTexture, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, PADDING),
                            (wx.StaticText(ceciliaPanel, -1, ''), 1, wx.EXPAND),
                            (self.textureToggle, 0, wx.ALIGN_CENTER_VERTICAL),
                         ])

        gridSizer.AddGrowableCol(1, 1)
        ceciliaPanel.SetSizerAndFit(gridSizer)
        return ceciliaPanel

    def createAudioServerPanel(self, panel):
        csoundPanel = wx.Panel(panel)
        csoundPanel.SetBackgroundColour(BACKGROUND_COLOUR)
        gridSizer = wx.FlexGridSizer(3,3,10,3)

        textKsmps = wx.StaticText(csoundPanel, 0, 'ksmps :')
        textKsmps.SetFont(self.font)       
        self.choiceKsmps = CustomMenu(csoundPanel, choice= ["1", "2", "5", "10", "25", "50", "100"], 
                                      init="10", outFunction=self.changeKsmps)

        textHardbuff = wx.StaticText(csoundPanel, 0, 'Hardware buffer :')
        textHardbuff.SetFont(self.font)       
        self.choiceHardBuff = CustomMenu(csoundPanel, choice=BUFFER_SIZES, 
                                        init=str(CeciliaLib.getVar("bufferSize")), outFunction=self.changeHardBuff)

        textSoftbuff = wx.StaticText(csoundPanel, 0, 'Software buffer :')
        textSoftbuff.SetFont(self.font)       
        self.choiceSoftBuff = CustomMenu(csoundPanel, choice=BUFFER_SIZES, 
                                        init=str(CeciliaLib.getVar("bufferSize")), outFunction=self.changeSoftBuff)

        gridSizer.AddMany([ 
                            (textKsmps, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, PADDING),
                            (wx.StaticText(csoundPanel, -1, '', size=(125,-1)), 1, wx.EXPAND),
                            (self.choiceKsmps, 0, wx.ALIGN_CENTER_VERTICAL),
                            (textHardbuff, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, PADDING),
                            (wx.StaticText(csoundPanel, -1, ''), 1, wx.EXPAND),
                            (self.choiceHardBuff, 0, wx.ALIGN_CENTER_VERTICAL),
                            (textSoftbuff, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, PADDING),
                            (wx.StaticText(csoundPanel, -1, ''), 1, wx.EXPAND),
                            (self.choiceSoftBuff, 0, wx.ALIGN_CENTER_VERTICAL),
                         ])

        gridSizer.AddGrowableCol(1, 1)
        csoundPanel.SetSizerAndFit(gridSizer)
        return csoundPanel

    def createMidiPanel(self, panel):        
        midiParamPanel = wx.Panel(panel)
        midiParamPanel.SetBackgroundColour(BACKGROUND_COLOUR)

        box = wx.BoxSizer(wx.VERTICAL)

        gridSizer1 = wx.FlexGridSizer(5, 3, 5, 5)
        # Audio driver
        textInOutConfig = wx.StaticText(midiParamPanel, 0, 'Midi Driver :')
        textInOutConfig.SetFont(self.font)       
        self.midiDriverChoice = CustomMenu(midiParamPanel, choice=['PortMidi'], 
                                       init='PortMidi', outFunction=self.onMidiDriverPageChange)

        gridSizer1.AddMany([ 
                            (textInOutConfig, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, PADDING),
                            (self.midiDriverChoice, 1, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 155),
                            ])

        self.midiDriverBox = wx.BoxSizer(wx.VERTICAL)
        self.midiDriverCurrentPane = self.midiDriverChoice.getIndex()
        self.midiDriverPanels = []
        portmidiPane = self.createPortmidiPane(midiParamPanel)
        if self.midiDriverCurrentPane != 0:
            portmidiPane.Hide()
        self.midiDriverPanels.append(portmidiPane)
        self.midiDriverBox.Add(self.midiDriverPanels[self.midiDriverCurrentPane])

        gridSizer1.AddGrowableCol(1, 1)
        box.Add(gridSizer1)
        box.AddSpacer(20)
        box.Add(self.midiDriverBox)
        midiParamPanel.SetSizerAndFit(box)
        return midiParamPanel

    def createAudioPanel(self, panel):        
        audioParamPanel = wx.Panel(panel)
        audioParamPanel.SetBackgroundColour(BACKGROUND_COLOUR)
        
        box = wx.BoxSizer(wx.VERTICAL)

        gridSizer1 = wx.FlexGridSizer(5, 3, 5, 5)
        # Audio driver
        textInOutConfig = wx.StaticText(audioParamPanel, 0, 'Audio Driver :')
        textInOutConfig.SetFont(self.font)       
        self.driverChoice = CustomMenu(audioParamPanel, choice=AUDIO_DRIVERS, 
                                       init=CeciliaLib.getVar("audioHostAPI"), outFunction=self.onDriverPageChange)
        # self.updatePortaudioButton = CloseBox(audioParamPanel, outFunction=self.updateAudioInOut, label='Update')
        # if self.driverChoice.getLabel() == 'portaudio':
        #     self.updatePortaudioButton.Show()
        # else:    
        #     self.updatePortaudioButton.Hide()
        
        gridSizer1.AddMany([ 
                            (textInOutConfig, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, PADDING),
                            (self.driverChoice, 1, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 147),
                            #(self.updatePortaudioButton, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 0),
                            ])
        
        # Audio driver panels
        self.driverBox = wx.BoxSizer(wx.VERTICAL)
        self.driverCurrentPane = self.driverChoice.getLabel()
        self.driverPanels = {}
        coreaudioPane = self.createCoreaudioPane(audioParamPanel)
        portaudioPane = self.createPortaudioPane(audioParamPanel)
        jackPane = self.createJackPane(audioParamPanel)
        if self.driverCurrentPane != 'coreaudio':
            coreaudioPane.Hide()
        if self.driverCurrentPane != 'portaudio':    
            portaudioPane.Hide()
        if self.driverCurrentPane != 'jack':
            jackPane.Hide()
        self.driverPanels['coreaudio'] = coreaudioPane
        self.driverPanels['portaudio'] = portaudioPane
        self.driverPanels['jack'] = jackPane
        self.driverBox.Add(self.driverPanels[self.driverCurrentPane])
        
        gridSizer3 = wx.FlexGridSizer(5, 3, 5, 5)
        # File Format
        textFileFormat = wx.StaticText(audioParamPanel, 0, 'File Format :')
        textFileFormat.SetFont(self.font)       
        self.choiceFileFormat = CustomMenu(audioParamPanel, choice=AUDIO_FILE_FORMATS, 
                                      init=CeciliaLib.getVar("audioFileType"), outFunction=self.changeFileType)
        
        # Bit depth
        textBD = wx.StaticText(audioParamPanel, 0, 'Bit Depth :')
        textBD.SetFont(self.font)       
        self.choiceBD = CustomMenu(audioParamPanel, choice=sorted(BIT_DEPTHS.keys()), outFunction=self.changeSampSize)
        
        for item in BIT_DEPTHS.items():
            if item[1]==CeciliaLib.getVar("sampSize"):
                self.choiceBD.setStringSelection(item[0])
                        
        # Number of channels        
        textNCHNLS = wx.StaticText(audioParamPanel, 0, '# of channels :')
        textNCHNLS.SetFont(self.font)       
        self.choiceNCHNLS = CustomMenu(audioParamPanel, choice=[str(x) for x in range(1,37)], 
                            init=CeciliaLib.getVar("nchnls"), outFunction=self.changeNchnls)        
 
        # Sampling rate
        textSR = wx.StaticText(audioParamPanel, 0, 'Sample Rate :')
        textSR.SetFont(self.font)       
        self.comboSR = CustomMenu(audioParamPanel, choice=SAMPLE_RATES, 
                            init=str(CeciliaLib.getVar("sr")), outFunction=self.changeSr)        
                
        gridSizer3.AddMany([ 
                            (textFileFormat, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, PADDING),
                            (wx.StaticText(audioParamPanel, -1, '', size=(138,-1)), 1, wx.EXPAND),
                            (self.choiceFileFormat, 0, wx.ALIGN_CENTER_VERTICAL),
                            (textBD, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, PADDING),
                            (wx.StaticText(audioParamPanel, -1, ''), 1, wx.EXPAND),
                            (self.choiceBD, 0, wx.ALIGN_CENTER_VERTICAL),
                            (textNCHNLS, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, PADDING),
                            (wx.StaticText(audioParamPanel, -1, ''), 1, wx.EXPAND),
                            (self.choiceNCHNLS, 0, wx.ALIGN_CENTER_VERTICAL),
                            (textSR, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, PADDING),
                            (wx.StaticText(audioParamPanel, -1, ''), 1, wx.EXPAND),
                            (self.comboSR, 0, wx.ALIGN_CENTER_VERTICAL),
                         ])
        
        gridSizer1.AddGrowableCol(1, 1)
        gridSizer3.AddGrowableCol(1, 1)
        box.Add(gridSizer1)
        box.AddSpacer(20)
        box.Add(self.driverBox)
        box.AddSpacer([60,30,20,60][['coreaudio', 'portaudio', 'jack'].index(self.driverCurrentPane)])
        box.Add(gridSizer3)
        audioParamPanel.SetSizerAndFit(box)
        return audioParamPanel

    def createPortmidiPane(self, panel):
        portmidiPanel = wx.Panel(panel)
        portmidiPanel.SetBackgroundColour(BACKGROUND_COLOUR)

        gridSizer = wx.FlexGridSizer(5, 3, 5, 5)
        # Input
        textIn = wx.StaticText(portmidiPanel, 0, 'Input Device :')
        textIn.SetFont(self.font)       
        availableMidiIns = []
        for d in CeciliaLib.getVar("availableMidiInputs"):
            availableMidiIns.append(CeciliaLib.ensureNFD(d))
        if availableMidiIns != [] and 'All' not in availableMidiIns:
            availableMidiIns.append('All')
        if CeciliaLib.getVar("midiDeviceIn") != '':
            try:
                initInput = availableMidiIns[int(CeciliaLib.getVar("midiDeviceIn"))]
            except:
                initInput = 'dump'    
        else:
            initInput = 'dump'    
        self.midiChoiceInput = CustomMenu(portmidiPanel, choice=availableMidiIns, 
                                      init=initInput, size=(168,20), outFunction=self.changeMidiInput)

        gridSizer.AddMany([ 
                            (textIn, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, PADDING),
                             (wx.StaticText(portmidiPanel, -1, '', size=(74,-1)), 1, wx.EXPAND),
                            (self.midiChoiceInput, 0, wx.ALIGN_CENTER_VERTICAL),
                            ])
                            
        gridSizer.AddGrowableCol(1, 1)
        portmidiPanel.SetSizerAndFit(gridSizer)
        return portmidiPanel

    def createPortaudioPane(self, panel):
        portaudioPanel = wx.Panel(panel)
        portaudioPanel.SetBackgroundColour(BACKGROUND_COLOUR)

        gridSizer = wx.FlexGridSizer(5, 3, 5, 5)
        # Input
        textIn = wx.StaticText(portaudioPanel, 0, 'Input Device :')
        textIn.SetFont(self.font)       
        availableAudioIns = []
        for d in CeciliaLib.getVar("availableAudioInputs"):
            availableAudioIns.append(CeciliaLib.ensureNFD(d))
        if CeciliaLib.getVar("audioInput") != '':
            try:
                initInput = availableAudioIns[int(CeciliaLib.getVar("audioInput"))]
            except:
                initInput = 'dump'
        else:
            initInput = 'dump'    
        self.choiceInput = CustomMenu(portaudioPanel, choice=availableAudioIns, 
                                      init=initInput, size=(168,20), outFunction=self.changeAudioInput)
        if CeciliaLib.getVar("audioInput") == '' or CeciliaLib.getVar("enableAudioInput") == 0:
            initInputState = 0
        else:
            initInputState = 1
        self.inputToggle = Toggle(portaudioPanel, initInputState, outFunction=self.enableAudioInput)                              
        
        # Output
        textOut = wx.StaticText(portaudioPanel, 0, 'Output Device :')
        textOut.SetFont(self.font)       
        availableAudioOuts = []
        for d in CeciliaLib.getVar("availableAudioOutputs"):
            availableAudioOuts.append(CeciliaLib.ensureNFD(d))
        try:
            initOutput = availableAudioOuts[int(CeciliaLib.getVar("audioOutput"))]
        except:
            initOutput = availableAudioOuts[0]
        self.choiceOutput = CustomMenu(portaudioPanel, choice=availableAudioOuts, 
                                        init=initOutput, size=(168,20), outFunction=self.changeAudioOutput)
        
        gridSizer.AddMany([ 
                            (textIn, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, PADDING),
                            (self.inputToggle, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 45),
                            (self.choiceInput, 0, wx.ALIGN_CENTER_VERTICAL),
                            (textOut, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, PADDING),
                            (wx.StaticText(portaudioPanel, -1, '', size=(65,-1)), 1, wx.EXPAND),
                            (self.choiceOutput, 0, wx.ALIGN_CENTER_VERTICAL),
                            ])
        gridSizer.AddGrowableCol(1, 1)
        portaudioPanel.SetSizerAndFit(gridSizer)
        return portaudioPanel

    def createCoreaudioPane(self, panel):
        return self.createPortaudioPane(panel)

    def createJackPane(self, panel):
        jackPanel = wx.Panel(panel)
        jackPanel.SetBackgroundColour(BACKGROUND_COLOUR)

        gridSizer = wx.FlexGridSizer(3, 3, 5, 5)
        
        jackClientLabel = wx.StaticText(jackPanel, -1, 'Jack client :')
        jackClientLabel.SetFont(self.font)       
        self.jackClient = wx.TextCtrl(jackPanel, -1, CeciliaLib.getVar("jack")['client'], size=(235,-1), style=wx.TE_PROCESS_ENTER|wx.NO_BORDER)
        self.jackClient.SetFont(self.font)       
        self.jackClient.Bind(wx.EVT_TEXT_ENTER, self.changeJackClient)
        self.jackClient.SetForegroundColour((50,50,50))
        self.jackClient.SetBackgroundColour("#999999")

        jackInPortLabel = wx.StaticText(jackPanel, -1, 'In Port :')
        jackInPortLabel.SetFont(self.font)       
        self.jackInPort = wx.TextCtrl(jackPanel, -1, CeciliaLib.getVar("jack")['inPortName'], size=(235,-1), style=wx.TE_PROCESS_ENTER|wx.NO_BORDER)
        self.jackInPort.SetFont(self.font)       
        self.jackInPort.Bind(wx.EVT_TEXT_ENTER, self.changeJackInPort)
        self.jackInPort.SetForegroundColour((50,50,50))
        self.jackInPort.SetBackgroundColour("#999999")

        jackOutPortLabel = wx.StaticText(jackPanel, -1, 'Out Port :')
        jackOutPortLabel.SetFont(self.font)       
        self.jackOutPort = wx.TextCtrl(jackPanel, -1, CeciliaLib.getVar("jack")['outPortName'], size=(235,-1), style=wx.TE_PROCESS_ENTER|wx.NO_BORDER)
        self.jackOutPort.SetFont(self.font)       
        self.jackOutPort.Bind(wx.EVT_TEXT_ENTER, self.changeJackOutPort)
        self.jackOutPort.SetForegroundColour((50,50,50))
        self.jackOutPort.SetBackgroundColour("#999999")

        gridSizer.AddMany([ 
                            (jackClientLabel, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, PADDING),
                            (wx.StaticText(jackPanel, -1, '', size=(15,-1)), 1, wx.EXPAND),
                            (self.jackClient, 0, wx.ALIGN_CENTER_VERTICAL),
                            (jackInPortLabel, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, PADDING),
                            (wx.StaticText(jackPanel, -1, ''), 1, wx.EXPAND),
                            (self.jackInPort, 0, wx.ALIGN_CENTER_VERTICAL),
                            (jackOutPortLabel, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, PADDING),
                            (wx.StaticText(jackPanel, -1, ''), 1, wx.EXPAND),
                            (self.jackOutPort, 0, wx.ALIGN_CENTER_VERTICAL),
                         ])
        
        gridSizer.AddGrowableCol(1, 1)
        jackPanel.SetSizerAndFit(gridSizer)
        return jackPanel

    def onDriverPageChange(self, index, label):
        CeciliaLib.setVar("audioHostAPI", label)
        self.driverPanels[self.driverCurrentPane].Hide()    
        self.driverPanels[label].Show()        
        self.driverPanels[label].SetPosition(self.driverBox.GetPosition())
        self.driverBox.Replace(self.driverPanels[self.driverCurrentPane], self.driverPanels[label])
        self.driverCurrentPane = label
        self.Refresh()

    def onMidiDriverPageChange(self, index, label):
        pass
        
    def openAudioMidiSetup(self):
        os.system('open /Applications/Utilities/Audio\ MIDI\ Setup.app')

    def enableAudioInput(self, state):
        CeciliaLib.setVar('enableAudioInput', state)
        if state == 1:
            CeciliaLib.setVar("audioInput", str(self.choiceInput.getIndex()))
        else:
            CeciliaLib.setVar("audioInput", '')

    def changeAudioInput(self, index, label):
        CeciliaLib.setVar("audioInput", index)

    def changeAudioOutput(self, index, label):
        CeciliaLib.setVar("audioOutput", index)

    def changeMidiInput(self, index, label):
        CeciliaLib.setVar("midiDeviceIn", index)

    def changeSfPlayer(self):
        if CeciliaLib.getVar("systemPlatform")  == 'win32':
            wildcard =  "Executable files (*.exe)|*.exe|"     \
                        "All files (*.*)|*.*"
        elif CeciliaLib.getVar("systemPlatform")  == 'darwin':
            wildcard =  "Application files (*.app)|*.app|"     \
                        "All files (*.*)|*.*"
        else:
            wildcard = "All files (*.*)|*.*"

        path = ''
        dlg = wx.FileDialog(self, message="Choose a soundfile player...",
                                 defaultDir=os.path.expanduser('~'),
                                 wildcard=wildcard,
                                 style=wx.OPEN)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()   
        dlg.Destroy()

        if path:
            CeciliaLib.setVar("soundfilePlayer", path)
            self.textSfPlayerPath.SetLabel(path)

    def changeSfEditor(self):
        if CeciliaLib.getVar("systemPlatform")  == 'win32':
            wildcard =  "Executable files (*.exe)|*.exe|"     \
                        "All files (*.*)|*.*"
        elif CeciliaLib.getVar("systemPlatform")  == 'darwin':
            wildcard =  "Application files (*.app)|*.app|"     \
                        "All files (*.*)|*.*"
        else:
            wildcard = "All files (*.*)|*.*"

        path = ''
        dlg = wx.FileDialog(self, message="Choose a soundfile editor...",
                                 defaultDir=os.path.expanduser('~'),
                                 wildcard=wildcard,
                                 style=wx.OPEN)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()   
        dlg.Destroy() 

        if path:
            CeciliaLib.setVar("soundfileEditor", path)
            self.textSfEditorPath.SetLabel(path)

    def addPrefPath(self):
        currentPath = CeciliaLib.getVar("prefferedPath")

        path = ''
        dlg = wx.DirDialog(self, message="Choose a folder...",
                                 defaultPath=os.path.expanduser('~'))

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()   
        dlg.Destroy()

        if path and currentPath != '':
            path = currentPath + ';' + path
        elif not path:
            return

        CeciliaLib.setVar("prefferedPath", path)
        self.textPrefPath.SetValue(path)

    def handleEditPrefPath(self, event):
        path = self.textPrefPath.GetValue()
        CeciliaLib.setVar("prefferedPath", path)
        self.textPrefPath.Navigate()

    def changeFileType(self, index, label):
        CeciliaLib.setVar("audioFileType", label)

    def changeSr(self, index, label):
        sr = int(label.strip())
        CeciliaLib.setVar("sr", sr)

    def changeSampSize(self, index, label):
        CeciliaLib.setVar("sampSize", BIT_DEPTHS[label])

    def changeNchnls(self, index, choice):
        nchnls = int(choice)
        CeciliaLib.setVar("nchnls", nchnls)
        CeciliaLib.updateNchnlsDevices()

    def changeJackClient(self, event):
        CeciliaLib.setJackParams(client=event.GetString())

    def changeJackInPort(self, event):        
        CeciliaLib.setJackParams(inPortName=event.GetString())

    def changeJackOutPort(self, event):
        CeciliaLib.setJackParams(outPortName=event.GetString())

    def updateMidiIn(self):
        CeciliaLib.queryAudioMidiDrivers()

        inputs = CeciliaLib.getVar("availableMidiInputs")

        if inputs == []:
            self.midiChoiceInput.setChoice([''])
        else:
            inputs.append('All')
            self.midiChoiceInput.setChoice(inputs)
            self.midiChoiceInput.setByIndex(int(CeciliaLib.getVar("midiDeviceIn")))
        
    def updateAudioInOut(self):
        CeciliaLib.queryAudioMidiDrivers()

        inputs = CeciliaLib.getVar("availableAudioInputs")
        outputs = CeciliaLib.getVar("availableAudioOutputs")

        if inputs == []:
            self.choiceInput.setChoice([''])
        else:
            self.choiceInput.setChoice(inputs)
            if CeciliaLib.getVar("audioInput") == '':
                self.inputToggle.setValue(0)
            else:
                self.inputToggle.setValue(1)
                self.choiceInput.setByIndex(int(CeciliaLib.getVar("audioInput")))

        if outputs == []:
            self.choiceOutput.setChoice([''])
        else:
            self.choiceOutput.setChoice(outputs)
            self.choiceOutput.setByIndex(int(CeciliaLib.getVar("audioOutput")))

    def changeKsmps(self, index, label):
        pass

    def changeHardBuff(self, index, label):
        pass

    def changeSoftBuff(self, index, label):
        pass

    def changeDefaultTotalTime(self, index, label):
        CeciliaLib.setVar("defaultTotalTime", float(self.choiceTotalTime.getLabel().strip()))

    def enableTooltips(self, state):
        CeciliaLib.setVar("useTooltips", state)

    def enableGraphTexture(self, state):
        CeciliaLib.setVar("graphTexture", state)
        if CeciliaLib.getVar("grapher") != None:
            CeciliaLib.getVar("grapher").plotter.draw()
