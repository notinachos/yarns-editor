# -*- coding: utf-8 -*-

license = '''
The MIT License (MIT)

Copyright (c) 2015 Panagiotis Peppas

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Notice:
Portions of this software may include text and/or graphics from Mutable Instruments, 
provided under the cc-by-sa 3.0 license. The author of this software is not 
endorsed by Mutable Instruments. Their company website, and the license, can be 
found at the following address: http://mutable-instruments.net/
'''

# imports
import sys
import platform
import ctypes
import random
import rtmidi_python as rtmidi
import wx
from wx.lib.embeddedimage import PyEmbeddedImage
from natsort import natsorted
import cc_values
import images

# the editor only supports this firmware version
firmware = str(1.02)

# information for the layout editor page
info_1M = 'In this mode, Yarns offers a single voice of CV/Gate conversion.'

info_2M = (
    'In this mode, Yarns provides two independent monophonic voices. The voices are\n'
    'independent in the sense that they can play different sequences, respond to\n'
    'different MIDI channels, etc.')

info_4M = 'In this mode, Yarns provides four independent monophonic voices.'

info_2P = (
    'In this mode, Yarns provides a single part made of two voices. The incoming notes\n'
    'are dispatched to these two voices.')

info_4P = (
    'In this mode, Yarns provides a single part made of four voices. The incoming notes\n'
    'are dispatched to these four voices.')

info_2poly = (
    'In this mode, Yarns provides a single part made of two voices. However, only the\n'
    'first voice is handled by Yarns\' CV/Gate outputs. The second voice is simply\n' 
    'forwarded as MIDI Note on/off messages the MIDI out. This allows "ping-pong" play\n'
    'between the modules connected to Yarns and another MIDI instrument. This can also\n'
    'be used to chain several instances of Yarns to get more CV outputs.')

info_4poly = (
    'In this mode, Yarns provides a single part made of 4voices. Only the first half\n'
    'of the voices are handled by Yarns\' CV/Gate outputs. Notes allocated to the other\n'
    'voices are forwarded to the MIDI output.')

info_8poly = (
    'In this mode, Yarns provides a single part made of 8 voices. Only the first half\n'
    'of the voices are handled by Yarns\' CV/Gate outputs. Notes allocated to the other\n'
    'voices are forwarded to the MIDI output.')

info_4trig = (
    'This layout is optimized for controlling percussion patches (for example from\n'
    'MIDI drum pads, or from a MIDI drum sequencer). It offers 4 parts, each of them\n'
    'listening to a single MIDI note. No control-voltage is emitted - just a trigger,\n'
    'freeing some outputs to emit additional gate and clock signals.')

info_3plus = (
    '3+ mode with 2 parts, designed specially for Edges. The first part has 3 voices\n'
    'of polyphony on channels 1-3, and the second part is monophonic, on channel 4.')

# i gave that script some variables. scripts love variables
default_tempo = '120'
default_swing = '0'
default_layout = '1M - Monophonic'
default_midiChannel = '1'
default_remoteChannel = '16'
default_lowerNote = '0 - C_0'
default_upperNote = '127 - G_10'
default_swing = '0'
default_legato = 'Off'
default_portamento = '0'
default_pitchBendRange = '2'
default_vibratoRange = '1'
default_fineTuning = '0'
default_oscillator = 'Off'
default_priority = 'Last'
default_voicing = 'Poly'
default_mode = 'Off'
default_vibrato = '50'
default_triggerDuration = '2'
default_transpose = '0'
default_arpRange = '0'
default_arpDirection = 'Up'
default_arpClockDiv = '/16'
default_arpGateLength = '3'
default_arpPattern = '1'
default_eucLength = '0'
default_eucFill = '0'
default_eucRotate = '0'
default_tuningSystem = 'Equal temperament'
default_tuningRoot = 'C'
default_velocityScale = 'Off'
default_triggerShape = 'Square'
default_auxCV = 'Aftertouch CC#2'
default_vibratoSpeed = '50'


class MidiManager():
    ''' handles midi events '''
    def __init__(self):
        self.midi_channel = None
        self.midi_input_device = None
        self.midi_output_device = None
        self.midi_input_port = None
        self.midi_output_port = None

    def InitMIDI(self):
        ''' initializes midi '''
        self.midi_input_device = rtmidi.MidiIn()
        self.midi_output_device = rtmidi.MidiOut()

    def ListMIDI(self, portDirection):
        ''' returns a list of available midi devices '''
        if (portDirection == 'input'):
            midiDevices = self.midi_input_device.ports
        elif (portDirection == 'output'):
            midiDevices = self.midi_output_device.ports
        else:
            raise ValueError('Incorrect value passed to MidiManager.ListMIDI()')
        return midiDevices

    def SetInput(self, deviceName):
        ''' sets the midi input port to use '''
        self.midi_input_port = deviceName

    def SetOutput(self, deviceName):
        ''' sets the midi output port to use '''
        self.midi_output_port = deviceName

    def SetChannel(self, channel):
        ''' sets the midi channel to use '''
        self.midi_channel = int(channel)

    def OpenMIDI(self):
        ''' looks up the ports by the index, and opens them '''
        if (self.midi_input_port): # midi input device is optional
            self.midi_input_device.open_port(
                self.midi_input_device.ports.index(self.midi_input_port))
        self.midi_output_device.open_port(
            self.midi_output_device.ports.index(self.midi_output_port))

    def CloseMIDI(self):
        ''' looks up the open ports by the index, and closes them '''
        if (self.midi_input_port): self.midi_input_device.close_port()
        if (self.midi_output_port): self.midi_output_device.close_port()

    def SendCC(self, controller, value):
        ''' sends data the the MIDI output '''
        # 1st byte changes depending on the midi channel
        if   (self.midi_channel == 1):  byte1 = 0xB0
        elif (self.midi_channel == 2):  byte1 = 0xB1
        elif (self.midi_channel == 3):  byte1 = 0xB2
        elif (self.midi_channel == 4):  byte1 = 0xB3
        elif (self.midi_channel == 5):  byte1 = 0xB4
        elif (self.midi_channel == 6):  byte1 = 0xB5
        elif (self.midi_channel == 7):  byte1 = 0xB6
        elif (self.midi_channel == 8):  byte1 = 0xB7
        elif (self.midi_channel == 9):  byte1 = 0xB8
        elif (self.midi_channel == 10): byte1 = 0xB9
        elif (self.midi_channel == 11): byte1 = 0xBA
        elif (self.midi_channel == 12): byte1 = 0xBB
        elif (self.midi_channel == 13): byte1 = 0xBC
        elif (self.midi_channel == 14): byte1 = 0xBD
        elif (self.midi_channel == 15): byte1 = 0xBE
        elif (self.midi_channel == 16): byte1 = 0xBF
        else:
            raise ValueError('Incorrect value passed to MidiManager.SendCC()')
        # send CC 
        self.midi_output_device.send_message([byte1, controller, value])


class LayoutSettings(wx.Panel):
    ''' the configuration page for layout options '''
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)

        # text
        txt_tempo = wx.StaticText(self, label='Tempo:')
        txt_swing = wx.StaticText(self, label='Swing:')
        txt_layout = wx.StaticText(self, label='Layout:')

        # populate menu contents
        tempo_menu = []
        for each in cc_values.tempo:
            tempo_menu.append(each)
        tempo_menu = natsorted(tempo_menu)

        swing_menu = []
        for each in cc_values.swing:
            swing_menu.append(each)
        swing_menu = natsorted(swing_menu)

        layout_menu = []
        for each in cc_values.layout:
            layout_menu.append(each)
        layout_menu = natsorted(layout_menu)

        # comboboxes
        self.cbox_tempo = wx.ComboBox(self, choices=tempo_menu, value=default_tempo, style=wx.CB_READONLY)
        self.cbox_swing = wx.ComboBox(self, choices=swing_menu, value=default_swing, style=wx.CB_READONLY)
        self.cbox_layouts = wx.ComboBox(self, choices=layout_menu, value=default_layout, style=wx.CB_READONLY)

        # combobox bindings
        self.cbox_tempo.Bind(wx.EVT_COMBOBOX, self.OnTempoSelect)
        self.cbox_swing.Bind(wx.EVT_COMBOBOX, self.OnSwingSelect)
        self.cbox_layouts.Bind(wx.EVT_COMBOBOX, self.OnLayoutSelect)

        # add it all to the sizer
        self.sizer.Add(txt_tempo)
        self.sizer.Add(self.cbox_tempo)
        self.sizer.Add(txt_swing)
        self.sizer.Add(self.cbox_swing)
        self.sizer.Add(txt_layout)
        self.sizer.Add(self.cbox_layouts)

        # default layout placeholders
        image = images.layout_1M.GetBitmap()
        self.layout_image = wx.StaticBitmap(self, -1, image, (0,0), (image.GetWidth(), image.GetHeight()))

        self.txt_info = wx.StaticText(self, label=info_1M)
        self.sizer.Add(wx.StaticText(self, label=''))
        self.sizer.Add(self.layout_image, 1, wx.ALIGN_CENTRE)
        self.sizer.Add(self.txt_info, 0, wx.ALIGN_CENTRE)

    def ChangeLayout(self, layout):
        ''' changes the layout image/text. also enables/disables tabs '''
        # pick correct layout image
        if   (layout == '1M - Monophonic'):                
            newImage = images.layout_1M.GetBitmap()
            self.parent.OnPartChange(1)
            self.txt_info.SetLabel(info_1M)

        elif (layout == '2M - Dual monophonic'):           
            newImage = images.layout_2M.GetBitmap()
            self.parent.OnPartChange(2)
            self.txt_info.SetLabel(info_2M)

        elif (layout == '4M - Quad monophonic'):           
            newImage = images.layout_4M.GetBitmap()
            self.parent.OnPartChange(4)
            self.txt_info.SetLabel(info_4M)

        elif (layout == '2P - Duophonic'):                 
            newImage = images.layout_2P.GetBitmap()
            self.parent.OnPartChange(1)
            self.txt_info.SetLabel(info_2P)

        elif (layout == '4P - Quadraphonic'):              
            newImage = images.layout_4P.GetBitmap()
            self.parent.OnPartChange(1)
            self.txt_info.SetLabel(info_4poly)

        elif (layout == '2> - Duophonic polychaining'):    
            newImage = images.layout_2P_chain.GetBitmap()
            self.parent.OnPartChange(1)
            self.txt_info.SetLabel(info_2poly)

        elif (layout == '4> - Quadraphonic polychaining'): 
            newImage = images.layout_4P_chain.GetBitmap()
            self.parent.OnPartChange(1)
            self.txt_info.SetLabel(info_4poly)

        elif (layout == '8> - Octophonic polychaining'):   
            newImage = images.layout_8P_chain.GetBitmap()
            self.parent.OnPartChange(1)
            self.txt_info.SetLabel(info_8poly)

        elif (layout == '4T - Quad trigger'):              
            newImage = images.layout_4T.GetBitmap()
            self.parent.OnPartChange(4)
            self.txt_info.SetLabel(info_4trig)

        elif (layout == '3+ - Three plus one'):            
            newImage = images.layout_3plus.GetBitmap()
            self.parent.OnPartChange(2)
            self.txt_info.SetLabel(info_3plus)

        else:
            raise ValueError('Incorrect value passed to LayoutSettings.ChangeLayout()')

        # set the new display image
        self.layout_image.SetBitmap(newImage)

        # refresh layout
        self.sizer.Layout()

    def OnTempoSelect(self, event):
        ''' called when the user selects a value from the combobox '''
        # get event type
        if (event == 'default'): choice = default_tempo 
        elif (event == 'random'): choice = random.choice(cc_values.tempo.keys())
        else: choice = event.GetString() 
        # correct combobox value 
        self.cbox_tempo.SetValue(choice)
        # set controller
        controller = cc_values.controllers['yarns_tempo']
        # set cc value
        value = cc_values.tempo[choice]
        # send cc message to midi output
        midiManager.SendCC(controller, value)

    def OnSwingSelect(self, event):
        ''' called when the user selects a value from the combobox '''
        # get event type
        if (event == 'default'): choice = default_swing
        elif (event == 'random'): choice = random.choice(cc_values.swing.keys())
        else: choice = event.GetString()
        # correct combobox value 
        self.cbox_swing.SetValue(choice)
        # set controller
        controller = cc_values.controllers['yarns_swing']
        # set cc value
        value = cc_values.swing[choice]
         # send cc message to midi output
        midiManager.SendCC(controller, value)

    def OnLayoutSelect(self, event):
        ''' called when the user selects a value from the combobox '''
        # get event type
        if (event == 'default'): choice = default_layout
        elif (event == 'random'): choice = random.choice(cc_values.layout.keys())
        else: choice = event.GetString()
        # correct combobox value 
        self.cbox_layouts.SetValue(choice)
        # set controller
        controller = cc_values.controllers['yarns_layout']
        # set cc value
        value = cc_values.layout[choice]
         # send cc message to midi output
        midiManager.SendCC(controller, value)

        # change layout image/text
        self.ChangeLayout(choice)

    def SendDefaults(self):
        ''' inits yarns with some default settings '''
        self.OnLayoutSelect('default')
        self.OnTempoSelect('default')
        self.OnSwingSelect('default')


class PartSettings(wx.Panel):
    ''' the configuration page for a single part '''
    def __init__(self, parent, partNumber):
        wx.Panel.__init__(self, parent)
        # the part number (1-4) that the page controls
        self.partNumber = partNumber
        # a list of checked boxes
        self.checkedBoxes = []
        # setup the GUI
        self.InitGUI()
        
    def InitGUI(self):
        ''' initializes the graphic elements '''
        # rows, columns, vertical gap, horizontal gap
        grid = wx.FlexGridSizer(28, 4, 8, 8)

        # add grid to panel
        self.SetSizer(grid)

        # checkboxes/text labels
        chk_midiChannel = wx.CheckBox(self, label='MIDI channel:')
        chk_lowerNote = wx.CheckBox(self, label='Lower note:')
        chk_upperNote = wx.CheckBox(self, label='Upper note:')
        chk_midiOutMode = wx.CheckBox(self, label='MIDI out mode:')
        chk_voicing = wx.CheckBox(self, label='Voicing:')
        chk_notePriority = wx.CheckBox(self, label='Note priority:')
        chk_portamento = wx.CheckBox(self, label='Portamento:')
        chk_legato = wx.CheckBox(self, label='Legato:')
        chk_pitchBendRange = wx.CheckBox(self, label='Pitch bend range:')
        chk_vibratoRange = wx.CheckBox(self, label='Vibrato range:')
        chk_vibratoSpeed = wx.CheckBox(self, label='Vibrato speed:')
        chk_transpose = wx.CheckBox(self, label='Transpose:')
        chk_fineTuning = wx.CheckBox(self, label='Fine tuning:')
        chk_tuningRoot = wx.CheckBox(self, label='Tuning root:')
        chk_tuningSystem = wx.CheckBox(self, label='Tuning system:')
        chk_triggerDuration = wx.CheckBox(self, label='Trigger duration:')
        chk_velocityScale = wx.CheckBox(self, label='Trigger velocity scale:')
        chk_triggerShape = wx.CheckBox(self, label='Trigger shape:')
        chk_auxCvOut = wx.CheckBox(self, label='Aux CV out:')
        chk_oscShape = wx.CheckBox(self, label='Oscillator shape:')
        chk_arpClockDiv = wx.CheckBox(self, label='Arp/Seq clock divider:')
        chk_arpGateLength = wx.CheckBox(self, label='Arp/Seq gate length:')
        chk_arpRange = wx.CheckBox(self, label='Arpeggiator range:')
        chk_arpDirection = wx.CheckBox(self, label='Arpeggiator direction:')
        chk_arpPattern = wx.CheckBox(self, label='Arpeggiator pattern:')
        chk_eucLength = wx.CheckBox(self, label='Euclidean length:')
        chk_eucFill = wx.CheckBox(self, label='Euclidean fill:')
        chk_eucRotate = wx.CheckBox(self, label='Euclidean rotate:')

        # checkbox bindings
        chk_midiChannel.Bind(wx.EVT_CHECKBOX, self.OnBoxChecked)
        chk_lowerNote.Bind(wx.EVT_CHECKBOX, self.OnBoxChecked)
        chk_upperNote.Bind(wx.EVT_CHECKBOX, self.OnBoxChecked)
        chk_midiOutMode.Bind(wx.EVT_CHECKBOX, self.OnBoxChecked)
        chk_voicing.Bind(wx.EVT_CHECKBOX, self.OnBoxChecked)
        chk_notePriority.Bind(wx.EVT_CHECKBOX, self.OnBoxChecked)
        chk_portamento.Bind(wx.EVT_CHECKBOX, self.OnBoxChecked)
        chk_legato.Bind(wx.EVT_CHECKBOX, self.OnBoxChecked)
        chk_pitchBendRange.Bind(wx.EVT_CHECKBOX, self.OnBoxChecked)
        chk_vibratoRange.Bind(wx.EVT_CHECKBOX, self.OnBoxChecked)
        chk_vibratoSpeed.Bind(wx.EVT_CHECKBOX, self.OnBoxChecked)
        chk_transpose.Bind(wx.EVT_CHECKBOX, self.OnBoxChecked)
        chk_fineTuning.Bind(wx.EVT_CHECKBOX, self.OnBoxChecked)
        chk_tuningRoot.Bind(wx.EVT_CHECKBOX, self.OnBoxChecked)
        chk_tuningSystem.Bind(wx.EVT_CHECKBOX, self.OnBoxChecked)
        chk_triggerDuration.Bind(wx.EVT_CHECKBOX, self.OnBoxChecked)
        chk_velocityScale.Bind(wx.EVT_CHECKBOX, self.OnBoxChecked)
        chk_triggerShape.Bind(wx.EVT_CHECKBOX, self.OnBoxChecked)
        chk_auxCvOut.Bind(wx.EVT_CHECKBOX, self.OnBoxChecked)
        chk_oscShape.Bind(wx.EVT_CHECKBOX, self.OnBoxChecked)
        chk_arpClockDiv.Bind(wx.EVT_CHECKBOX, self.OnBoxChecked)
        chk_arpGateLength.Bind(wx.EVT_CHECKBOX, self.OnBoxChecked)
        chk_arpRange.Bind(wx.EVT_CHECKBOX, self.OnBoxChecked)
        chk_arpDirection.Bind(wx.EVT_CHECKBOX, self.OnBoxChecked)
        chk_arpPattern.Bind(wx.EVT_CHECKBOX, self.OnBoxChecked)
        chk_eucLength.Bind(wx.EVT_CHECKBOX, self.OnBoxChecked)
        chk_eucFill.Bind(wx.EVT_CHECKBOX, self.OnBoxChecked)
        chk_eucRotate.Bind(wx.EVT_CHECKBOX, self.OnBoxChecked)

        # populate menu contents
        midiChannel_menu = []
        for each in cc_values.channel:
            midiChannel_menu.append(each)
        midiChannel_menu = natsorted(midiChannel_menu)

        midiNote_menu = []
        for each in cc_values.note:
            midiNote_menu.append(each)
        midiNote_menu = natsorted(midiNote_menu)

        midiOutput_menu = []
        for each in cc_values.midi_output:
            midiOutput_menu.append(each)
        midiOutput_menu = natsorted(midiOutput_menu)

        vibratoSpeed_menu = []
        for each in cc_values.vibrato_speed:
            vibratoSpeed_menu.append(each)
        vibratoSpeed_menu = natsorted(vibratoSpeed_menu)

        voicing_menu = []
        for each in cc_values.voicing:
            voicing_menu.append(each)
        voicing_menu = natsorted(voicing_menu)

        note_priority_menu = []
        for each in cc_values.note_priority:
            note_priority_menu.append(each)
        note_priority_menu = natsorted(note_priority_menu)

        boolean_menu = []
        for each in cc_values.boolean:
            boolean_menu.append(each)
        boolean_menu = natsorted(boolean_menu)

        tuningRoot_menu = []
        for each in cc_values.tuning_root:
            tuningRoot_menu.append(each)
        tuningRoot_menu = natsorted(tuningRoot_menu)

        tuningSystem_menu = []
        for each in cc_values.tuning_system:
            tuningSystem_menu.append(each)
        tuningSystem_menu = natsorted(tuningSystem_menu)

        triggerShape_menu = []
        for each in cc_values.trigger_shape:
            triggerShape_menu.append(each)
        triggerShape_menu = natsorted(triggerShape_menu)

        auxCV_menu = []
        for each in cc_values.aux_cv:
            auxCV_menu.append(each)
        auxCV_menu = natsorted(auxCV_menu)

        oscillator_menu = []
        for each in cc_values.oscillator:
            oscillator_menu.append(each)
        oscillator_menu = natsorted(oscillator_menu)

        arpClock_menu = []
        for each in cc_values.arp_clock_division:
            arpClock_menu.append(each)
        arpClock_menu = natsorted(arpClock_menu)

        arpDirection_menu = []
        for each in cc_values.arp_direction:
            arpDirection_menu.append(each)
        arpDirection_menu = natsorted(arpDirection_menu)

        pitchBend_menu = []
        for each in cc_values.pitch_bend:
            pitchBend_menu.append(each)
        pitchBend_menu = natsorted(pitchBend_menu)

        vibratoRange_menu = []
        for each in cc_values.vibrato_range:
            vibratoRange_menu.append(each)
        vibratoRange_menu = natsorted(vibratoRange_menu)

        transpose_menu = []
        for each in cc_values.transpose:
            transpose_menu.append(each)
        transpose_menu = natsorted(transpose_menu)

        fineTuning_menu = []
        for each in cc_values.fine_tuning:
            fineTuning_menu.append(each)
        fineTuning_menu = natsorted(fineTuning_menu)

        triggerDuration_menu = []
        for each in cc_values.trigger_duration:
            triggerDuration_menu.append(each)
        triggerDuration_menu = natsorted(triggerDuration_menu)

        arpRange_menu = []
        for each in cc_values.arp_range:
            arpRange_menu.append(each)
        arpRange_menu = natsorted(arpRange_menu)

        arpPattern_menu = []
        for each in cc_values.arp_pattern:
            arpPattern_menu.append(each)
        arpPattern_menu = natsorted(arpPattern_menu)

        arpGateLength_menu = []
        for each in cc_values.arp_gate_length:
            arpGateLength_menu.append(each)
        arpGateLength_menu = natsorted(arpGateLength_menu)

        euclidean_menu = []
        for each in cc_values.euclidean:
            euclidean_menu.append(each)
        euclidean_menu = natsorted(euclidean_menu)

        swing_menu = []
        for each in cc_values.swing:
            swing_menu.append(each)
        swing_menu = natsorted(swing_menu)

        # combo boxes
        self.cbox_triggerDuration = wx.ComboBox(
            self, choices=triggerDuration_menu, value=default_triggerDuration, style=wx.CB_READONLY)

        self.cbox_arpRange = wx.ComboBox(
            self, choices=arpRange_menu, value=default_arpRange, style=wx.CB_READONLY)

        self.cbox_arpPattern = wx.ComboBox(
            self, choices=arpPattern_menu, value=default_arpPattern, style=wx.CB_READONLY)

        self.cbox_arpGateLength = wx.ComboBox(
            self, choices=arpGateLength_menu, value=default_arpGateLength, style=wx.CB_READONLY)

        self.cbox_eucLength = wx.ComboBox(
            self, choices=euclidean_menu, value=default_eucLength, style=wx.CB_READONLY)

        self.cbox_eucFill = wx.ComboBox(
            self, choices=euclidean_menu, value=default_eucFill, style=wx.CB_READONLY)

        self.cbox_eucRotate = wx.ComboBox(
            self, choices=euclidean_menu, value=default_eucRotate, style=wx.CB_READONLY)

        self.cbox_fineTuning = wx.ComboBox(
            self, choices=fineTuning_menu, value=default_fineTuning, style=wx.CB_READONLY)

        self.cbox_transpose = wx.ComboBox(
            self, choices=transpose_menu, value=default_transpose, style=wx.CB_READONLY)

        self.cbox_vibratoRange = wx.ComboBox(
            self, choices=vibratoRange_menu, value=default_vibratoRange, style=wx.CB_READONLY)

        self.cbox_pitchBendRange = wx.ComboBox(
            self, choices=pitchBend_menu, value=default_pitchBendRange, style=wx.CB_READONLY)

        self.cbox_portamento = wx.ComboBox(
            self, choices=swing_menu, value=default_portamento, style=wx.CB_READONLY)

        self.cbox_midiChannel = wx.ComboBox(
            self, choices=midiChannel_menu, value=default_midiChannel, style=wx.CB_READONLY)

        self.cbox_vibratoSpeed = wx.ComboBox(
            self, choices=vibratoSpeed_menu, value=default_vibrato, style=wx.CB_READONLY)

        self.cbox_lowerNote = wx.ComboBox(
            self, choices=midiNote_menu, value=default_lowerNote, style=wx.CB_READONLY)

        self.cbox_upperNote = wx.ComboBox(
            self, choices=midiNote_menu, value=default_upperNote, style=wx.CB_READONLY)

        self.cbox_midiOutMode = wx.ComboBox(
            self, choices=midiOutput_menu, value=default_mode, style=wx.CB_READONLY)

        self.cbox_voicing = wx.ComboBox(
            self, choices=voicing_menu, value=default_voicing, style=wx.CB_READONLY)

        self.cbox_notePriority = wx.ComboBox(
            self, choices=note_priority_menu, value=default_priority, style=wx.CB_READONLY)

        self.cbox_legato = wx.ComboBox(
            self, choices=boolean_menu, value=default_legato, style=wx.CB_READONLY)        

        self.cbox_tuningRoot = wx.ComboBox(
            self, choices=tuningRoot_menu, value=default_tuningRoot, style=wx.CB_READONLY)

        self.cbox_tuningSystem = wx.ComboBox(
            self, choices=tuningSystem_menu, value=default_tuningSystem, style=wx.CB_READONLY)

        self.cbox_velocityScale = wx.ComboBox(
            self, choices=boolean_menu, value=default_velocityScale, style=wx.CB_READONLY)

        self.cbox_triggerShape = wx.ComboBox(
            self, choices=triggerShape_menu, value=default_triggerShape, style=wx.CB_READONLY)

        self.cbox_auxCvOut = wx.ComboBox(
            self, choices=auxCV_menu, value=default_auxCV, style=wx.CB_READONLY)

        self.cbox_oscShape = wx.ComboBox(
            self, choices=oscillator_menu, value=default_oscillator, style=wx.CB_READONLY)

        self.cbox_arpClockDiv = wx.ComboBox(
            self, choices=arpClock_menu, value=default_arpClockDiv, style=wx.CB_READONLY)

        self.cbox_arpDirection = wx.ComboBox(
            self, choices=arpDirection_menu, value=default_arpDirection, style=wx.CB_READONLY)
        
        # combo box bindings
        self.cbox_pitchBendRange.Bind(wx.EVT_COMBOBOX, self.OnPitchBendRangeSelect)
        self.cbox_vibratoRange.Bind(wx.EVT_COMBOBOX, self.OnVibratoRangeSelect)
        self.cbox_transpose.Bind(wx.EVT_COMBOBOX, self.OnTransposeSelect)
        self.cbox_fineTuning.Bind(wx.EVT_COMBOBOX, self.OnFineTuningSelect)
        self.cbox_triggerDuration.Bind(wx.EVT_COMBOBOX, self.OnTriggerDurationSelect)
        self.cbox_arpRange.Bind(wx.EVT_COMBOBOX, self.OnArpRangeSelect)
        self.cbox_arpPattern.Bind(wx.EVT_COMBOBOX, self.OnArpPatternSelect)
        self.cbox_arpGateLength.Bind(wx.EVT_COMBOBOX, self.OnArpGateLengthSelect)
        self.cbox_eucLength.Bind(wx.EVT_COMBOBOX, self.OnEucLengthSelect)
        self.cbox_eucFill.Bind(wx.EVT_COMBOBOX, self.OnEucFillSelect)
        self.cbox_eucRotate.Bind(wx.EVT_COMBOBOX, self.OnEucRotateSelect)
        self.cbox_portamento.Bind(wx.EVT_COMBOBOX, self.OnPortamentoSelect)
        self.cbox_midiChannel.Bind(wx.EVT_COMBOBOX, self.OnChannelSelect)
        self.cbox_lowerNote.Bind(wx.EVT_COMBOBOX, self.OnLowerNoteSelect)
        self.cbox_upperNote.Bind(wx.EVT_COMBOBOX, self.OnUpperNoteSelect)
        self.cbox_midiOutMode.Bind(wx.EVT_COMBOBOX, self.OnMidiOutModeSelect)
        self.cbox_voicing.Bind(wx.EVT_COMBOBOX, self.OnVoicingSelect)
        self.cbox_notePriority.Bind(wx.EVT_COMBOBOX, self.OnNotePrioritySelect)
        self.cbox_legato.Bind(wx.EVT_COMBOBOX, self.OnLegatoSelect)
        self.cbox_vibratoSpeed.Bind(wx.EVT_COMBOBOX, self.OnVibratoSpeedSelect)
        self.cbox_tuningRoot.Bind(wx.EVT_COMBOBOX, self.OnTuningRootSelect)
        self.cbox_tuningSystem.Bind(wx.EVT_COMBOBOX, self.OnTuningSystemSelect)
        self.cbox_velocityScale.Bind(wx.EVT_COMBOBOX, self.OnVelocityScaleSelect)
        self.cbox_triggerShape.Bind(wx.EVT_COMBOBOX, self.OnTriggerShapeSelect)
        self.cbox_auxCvOut.Bind(wx.EVT_COMBOBOX, self.OnAuxCvOutSelect)
        self.cbox_oscShape.Bind(wx.EVT_COMBOBOX, self.OnOscShapeSelect)
        self.cbox_arpClockDiv.Bind(wx.EVT_COMBOBOX, self.OnArpClockDivSelect)
        self.cbox_arpDirection.Bind(wx.EVT_COMBOBOX, self.OnArpDirectionSelect)
        
        # randomize buttons
        btn_randomSelection = wx.Button(self, label='Randomize selected')
        btn_randomSelection.Bind(wx.EVT_BUTTON, self.OnRandomSelection)

        btn_reset = wx.Button(self, label='Reset all defaults')
        btn_reset.Bind(wx.EVT_BUTTON, self.OnReset)

        # add all items to the 4 column grid created earlier
        grid.AddMany([
            (chk_midiChannel),    (self.cbox_midiChannel),    (chk_midiOutMode),     (self.cbox_midiOutMode),
            (chk_lowerNote),      (self.cbox_lowerNote),      (chk_voicing),         (self.cbox_voicing),
            (chk_upperNote),      (self.cbox_upperNote),      (chk_notePriority),    (self.cbox_notePriority),
            (chk_portamento),     (self.cbox_portamento),     (chk_legato),          (self.cbox_legato),
            (chk_pitchBendRange), (self.cbox_pitchBendRange), (chk_vibratoRange),    (self.cbox_vibratoRange),
            (chk_transpose),      (self.cbox_transpose),      (chk_vibratoSpeed),    (self.cbox_vibratoSpeed),
            (chk_fineTuning),     (self.cbox_fineTuning),     (chk_velocityScale),   (self.cbox_velocityScale),
            (chk_tuningSystem),   (self.cbox_tuningSystem),   (chk_triggerDuration), (self.cbox_triggerDuration),
            (chk_tuningRoot),     (self.cbox_tuningRoot),     (chk_triggerShape),    (self.cbox_triggerShape),
            (chk_arpGateLength),  (self.cbox_arpGateLength),  (chk_oscShape),        (self.cbox_oscShape),
            (chk_arpClockDiv),    (self.cbox_arpClockDiv),    (chk_auxCvOut),        (self.cbox_auxCvOut),
            (chk_arpRange),       (self.cbox_arpRange),       (chk_eucLength),       (self.cbox_eucLength),
            (chk_arpDirection),   (self.cbox_arpDirection),   (chk_eucFill),         (self.cbox_eucFill),
            (chk_arpPattern),     (self.cbox_arpPattern),     (chk_eucRotate),       (self.cbox_eucRotate),
            (0,0),                (0,0),                      (btn_randomSelection), (btn_reset)])

    def OnBoxChecked(self, event):
        ''' a checkbox was checked '''
        sender = event.GetEventObject()
        isChecked = sender.GetValue()

        if (isChecked == True):
            # add items to a list of currently checked boxes
            self.checkedBoxes.append(sender.GetLabel())
        elif (isChecked == False):
            # remove items from the list of currently checked boxes
            self.checkedBoxes.remove(sender.GetLabel())

    def OnRandomSelection(self, event):
        ''' randomizes all currently checked boxes '''
        for box in self.checkedBoxes:
            if   (box == 'MIDI channel:'): self.OnChannelSelect('random')
            elif (box == 'Lower note:'): self.OnLowerNoteSelect('random')
            elif (box == 'Upper note:'): self.OnUpperNoteSelect('random')
            elif (box == 'Portamento:'): self.OnPortamentoSelect('random')
            elif (box == 'Pitch bend range:'): self.OnPitchBendRangeSelect('random')
            elif (box == 'Transpose:'): self.OnTransposeSelect('random')
            elif (box == 'Fine tuning:'): self.OnFineTuningSelect('random')
            elif (box == 'Tuning system:'): self.OnTuningSystemSelect('random')
            elif (box == 'Tuning root:'): self.OnTuningRootSelect('random')
            elif (box == 'Arp/Seq gate length:'): self.OnArpGateLengthSelect('random')
            elif (box == 'Arp/Seq clock divider:'): self.OnArpClockDivSelect('random')
            elif (box == 'Arpeggiator range:'): self.OnArpRangeSelect('random')
            elif (box == 'Arpeggiator direction:'): self.OnArpDirectionSelect('random')
            elif (box == 'Arpeggiator pattern:'): self.OnArpPatternSelect('random')
            elif (box == 'MIDI out mode:'): self.OnMidiOutModeSelect('random')
            elif (box == 'Voicing:'): self.OnVoicingSelect('random')
            elif (box == 'Note priority:'): self.OnNotePrioritySelect('random')
            elif (box == 'Legato:'): self.OnLegatoSelect('random')
            elif (box == 'Vibrato range:'): self.OnVibratoRangeSelect('random')
            elif (box == 'Vibrato speed:'): self.OnVibratoSpeedSelect('random')
            elif (box == 'Trigger velocity scale:'): self.OnVelocityScaleSelect('random')
            elif (box == 'Trigger duration:'): self.OnTriggerDurationSelect('random')
            elif (box == 'Trigger shape:'): self.OnTriggerShapeSelect('random')
            elif (box == 'Oscillator shape:'): self.OnOscShapeSelect('random')
            elif (box == 'Aux CV out:'): self.OnAuxCvOutSelect('random')
            elif (box == 'Euclidean length:'): self.OnEucLengthSelect('random')
            elif (box == 'Euclidean fill:'): self.OnEucFillSelect('random')
            elif (box == 'Euclidean rotate:'): self.OnEucRotateSelect('random')
            else:
                raise ValueError('Incorrect value passed to PartSettings.OnRandomSelection()')

    def OnReset(self, event):
        ''' resets all values to defaults '''
        self.SendDefaults()

    def OnChannelSelect(self, event):
        ''' combobox '''
        # get event type
        if (event == 'default'): choice = default_midiChannel
        elif (event == 'random'): choice = random.choice(cc_values.channel.keys())
        else: choice = event.GetString()
        # correct combobox value 
        self.cbox_midiChannel.SetValue(choice)
        # set controller
        if   (self.partNumber == 1): controller = cc_values.controllers['part1_midiChannel']
        elif (self.partNumber == 2): controller = cc_values.controllers['part2_midiChannel']
        elif (self.partNumber == 3): controller = cc_values.controllers['part3_midiChannel']
        elif (self.partNumber == 4): controller = cc_values.controllers['part4_midiChannel']
        # set value
        value = cc_values.channel[choice]
        # send value to midi output
        midiManager.SendCC(controller, value)
    
    def OnLowerNoteSelect(self, event):
        ''' combobox '''
        # get event type
        if (event == 'default'): choice = default_lowerNote
        elif (event == 'random'): choice = random.choice(cc_values.note.keys())
        else: choice = event.GetString()
        # correct combobox value 
        self.cbox_lowerNote.SetValue(choice)
        # set controller
        if   (self.partNumber == 1): controller = cc_values.controllers['part1_lowerNote']
        elif (self.partNumber == 2): controller = cc_values.controllers['part2_lowerNote']
        elif (self.partNumber == 3): controller = cc_values.controllers['part3_lowerNote']
        elif (self.partNumber == 4): controller = cc_values.controllers['part4_lowerNote']
        # set value
        value = cc_values.note[choice]
        # send value to midi output
        midiManager.SendCC(controller, value)
    
    def OnUpperNoteSelect(self, event):
        ''' combobox '''
        # get event type
        if (event == 'default'): choice = default_upperNote
        elif (event == 'random'): choice = random.choice(cc_values.note.keys())
        else: choice = event.GetString()
        # correct combobox value 
        self.cbox_upperNote.SetValue(choice)
        # set controller
        if   (self.partNumber == 1): controller = cc_values.controllers['part1_upperNote']
        elif (self.partNumber == 2): controller = cc_values.controllers['part2_upperNote']
        elif (self.partNumber == 3): controller = cc_values.controllers['part3_upperNote']
        elif (self.partNumber == 4): controller = cc_values.controllers['part4_upperNote']
        # set value
        value = cc_values.note[choice]
        # send value to midi output
        midiManager.SendCC(controller, value)
    
    def OnMidiOutModeSelect(self, event):
        ''' combobox '''
        # get event type
        if (event == 'default'): choice = default_mode
        elif (event == 'random'): choice = random.choice(cc_values.midi_output.keys())
        else: choice = event.GetString()
        # correct combobox value 
        self.cbox_midiOutMode.SetValue(choice)
        # set controller
        if   (self.partNumber == 1): controller = cc_values.controllers['part1_midiOutMode']
        elif (self.partNumber == 2): controller = cc_values.controllers['part2_midiOutMode']
        elif (self.partNumber == 3): controller = cc_values.controllers['part3_midiOutMode']
        elif (self.partNumber == 4): controller = cc_values.controllers['part4_midiOutMode']
        # set value
        value = cc_values.midi_output[choice]
        # send value to midi output
        midiManager.SendCC(controller, value)
    
    def OnVoicingSelect(self, event):
        ''' combobox '''
        # get event type
        if (event == 'default'): choice = default_voicing
        elif (event == 'random'): choice = random.choice(cc_values.voicing.keys())
        else: choice = event.GetString()
        # correct combobox value 
        self.cbox_voicing.SetValue(choice)
        # set controller
        if   (self.partNumber == 1): controller = cc_values.controllers['part1_voicing']
        elif (self.partNumber == 2): controller = cc_values.controllers['part2_voicing']
        elif (self.partNumber == 3): controller = cc_values.controllers['part3_voicing']
        elif (self.partNumber == 4): controller = cc_values.controllers['part4_voicing']
        # set value
        value = cc_values.voicing[choice]
        # send value to midi output
        midiManager.SendCC(controller, value)
    
    def OnNotePrioritySelect(self, event):
        ''' combobox '''
        # get event type
        if (event == 'default'): choice = default_priority
        elif (event == 'random'): choice = random.choice(cc_values.note_priority.keys())
        else: choice = event.GetString()
        # correct combobox value 
        self.cbox_notePriority.SetValue(choice)
        # set controller
        if   (self.partNumber == 1): controller = cc_values.controllers['part1_notePriority']
        elif (self.partNumber == 2): controller = cc_values.controllers['part2_notePriority']
        elif (self.partNumber == 3): controller = cc_values.controllers['part3_notePriority']
        elif (self.partNumber == 4): controller = cc_values.controllers['part4_notePriority']
        # set value
        value = cc_values.note_priority[choice]
        # send value to midi output
        midiManager.SendCC(controller, value)
    
    def OnPortamentoSelect(self, event):
        ''' combobox '''
        # get event type
        if (event == 'default'): choice = default_portamento
        elif (event == 'random'): choice = random.choice(cc_values.portamento.keys())
        else: choice = event.GetString()
        # correct combobox value 
        self.cbox_portamento.SetValue(choice)
        # set controller
        if   (self.partNumber == 1): controller = cc_values.controllers['part1_portamento']
        elif (self.partNumber == 2): controller = cc_values.controllers['part2_portamento']
        elif (self.partNumber == 3): controller = cc_values.controllers['part3_portamento']
        elif (self.partNumber == 4): controller = cc_values.controllers['part4_portamento']
        # set value
        value = cc_values.portamento[choice] # portamento uses same cc values as swing
        # send value to midi output
        midiManager.SendCC(controller, value)
    
    def OnLegatoSelect(self, event):
        ''' combobox '''
        # get event type
        if (event == 'default'): choice = default_legato
        elif (event == 'random'): choice = random.choice(cc_values.boolean.keys())
        else: choice = event.GetString()
        # correct combobox value 
        self.cbox_legato.SetValue(choice)
        # set controller
        if   (self.partNumber == 1): controller = cc_values.controllers['part1_legato']
        elif (self.partNumber == 2): controller = cc_values.controllers['part2_legato']
        elif (self.partNumber == 3): controller = cc_values.controllers['part3_legato']
        elif (self.partNumber == 4): controller = cc_values.controllers['part4_legato']
        # set value
        value = cc_values.boolean[choice]
        # send value to midi output
        midiManager.SendCC(controller, value)
    
    def OnPitchBendRangeSelect(self, event):
        ''' combobox '''
        # get event type
        if (event == 'default'): choice = default_pitchBendRange
        elif (event == 'random'): choice = random.choice(cc_values.pitch_bend.keys())
        else: choice = event.GetString()
        # correct combobox value 
        self.cbox_pitchBendRange.SetValue(choice)
        # set controller
        if   (self.partNumber == 1): controller = cc_values.controllers['part1_pitchBendRange']
        elif (self.partNumber == 2): controller = cc_values.controllers['part2_pitchBendRange']
        elif (self.partNumber == 3): controller = cc_values.controllers['part3_pitchBendRange']
        elif (self.partNumber == 4): controller = cc_values.controllers['part4_pitchBendRange']
        # set value
        value = cc_values.pitch_bend[choice]
        # send value to midi output
        midiManager.SendCC(controller, value)
    
    def OnVibratoRangeSelect(self, event):
        ''' combobox '''
        # get event type
        if (event == 'default'): choice = default_vibratoRange
        elif (event == 'random'): choice = random.choice(cc_values.vibrato_range.keys())
        else: choice = event.GetString()
        # correct combobox value 
        self.cbox_vibratoRange.SetValue(choice)
        # set controller
        if   (self.partNumber == 1): controller = cc_values.controllers['part1_vibratoRange']
        elif (self.partNumber == 2): controller = cc_values.controllers['part2_vibratoRange']
        elif (self.partNumber == 3): controller = cc_values.controllers['part3_vibratoRange']
        elif (self.partNumber == 4): controller = cc_values.controllers['part4_vibratoRange']
        # set value
        value = cc_values.vibrato_range[choice]
        # send value to midi output
        midiManager.SendCC(controller, value)
    
    def OnVibratoSpeedSelect(self, event):
        ''' combobox '''
        # get event type
        if (event == 'default'): choice = default_vibratoSpeed
        elif (event == 'random'): choice = random.choice(cc_values.vibrato_speed.keys())
        else: choice = event.GetString()
        # correct combobox value 
        self.cbox_vibratoSpeed.SetValue(choice)
        # set controller
        if   (self.partNumber == 1): controller = cc_values.controllers['part1_vibratoSpeed']
        elif (self.partNumber == 2): controller = cc_values.controllers['part2_vibratoSpeed']
        elif (self.partNumber == 3): controller = cc_values.controllers['part3_vibratoSpeed']
        elif (self.partNumber == 4): controller = cc_values.controllers['part4_vibratoSpeed']
        # set value
        value = cc_values.vibrato_speed[choice]
        # send value to midi output
        midiManager.SendCC(controller, value)
    
    def OnTransposeSelect(self, event):
        ''' combobox '''
        # get event type
        if (event == 'default'): choice = default_transpose
        elif (event == 'random'): choice = random.choice(cc_values.transpose.keys())
        else: choice = event.GetString()
        # correct combobox value 
        self.cbox_transpose.SetValue(choice)
        # set controller
        if   (self.partNumber == 1): controller = cc_values.controllers['part1_transpose']
        elif (self.partNumber == 2): controller = cc_values.controllers['part2_transpose']
        elif (self.partNumber == 3): controller = cc_values.controllers['part3_transpose']
        elif (self.partNumber == 4): controller = cc_values.controllers['part4_transpose']
        # set value
        value = cc_values.transpose[choice]
        # send value to midi output
        midiManager.SendCC(controller, value)
    
    def OnFineTuningSelect(self, event):
        ''' combobox '''
        # get event type
        if (event == 'default'): choice = default_fineTuning
        elif (event == 'random'): choice = random.choice(cc_values.fine_tuning.keys())
        else: choice = event.GetString()
        # correct combobox value 
        self.cbox_fineTuning.SetValue(choice)
        # set controller
        if   (self.partNumber == 1): controller = cc_values.controllers['part1_fineTuning']
        elif (self.partNumber == 2): controller = cc_values.controllers['part2_fineTuning']
        elif (self.partNumber == 3): controller = cc_values.controllers['part3_fineTuning']
        elif (self.partNumber == 4): controller = cc_values.controllers['part4_fineTuning']
        # set value
        value = cc_values.fine_tuning[choice]
        # send value to midi output
        midiManager.SendCC(controller, value)
    
    def OnTuningRootSelect(self, event):
        ''' combobox '''
        # get event type
        if (event == 'default'): choice = default_tuningRoot
        elif (event == 'random'): choice = random.choice(cc_values.tuning_root.keys())
        else: choice = event.GetString()
        # correct combobox value 
        self.cbox_tuningRoot.SetValue(choice)
        # set controller
        if   (self.partNumber == 1): controller = cc_values.controllers['part1_tuningRoot']
        elif (self.partNumber == 2): controller = cc_values.controllers['part2_tuningRoot']
        elif (self.partNumber == 3): controller = cc_values.controllers['part3_tuningRoot']
        elif (self.partNumber == 4): controller = cc_values.controllers['part4_tuningRoot']
        # set value
        value = cc_values.tuning_root[choice]
        # send value to midi output
        midiManager.SendCC(controller, value)
    
    def OnTuningSystemSelect(self, event):
        ''' combobox '''
        # get event type
        if (event == 'default'): choice = default_tuningSystem
        elif (event == 'random'): choice = random.choice(cc_values.tuning_system.keys())
        else: choice = event.GetString()
        # correct combobox value 
        self.cbox_tuningSystem.SetValue(choice)
        # set controller
        if   (self.partNumber == 1): controller = cc_values.controllers['part1_tuningSystem']
        elif (self.partNumber == 2): controller = cc_values.controllers['part2_tuningSystem']
        elif (self.partNumber == 3): controller = cc_values.controllers['part3_tuningSystem']
        elif (self.partNumber == 4): controller = cc_values.controllers['part4_tuningSystem']
        # set value
        value = cc_values.tuning_system[choice]
        # send value to midi output
        midiManager.SendCC(controller, value)
    
    def OnTriggerDurationSelect(self, event):
        ''' combobox '''
        # get event type
        if (event == 'default'): choice = default_triggerDuration
        elif (event == 'random'): choice = random.choice(cc_values.trigger_duration.keys())
        else: choice = event.GetString()
        # correct combobox value 
        self.cbox_triggerDuration.SetValue(choice)
        # set controller
        if   (self.partNumber == 1): controller = cc_values.controllers['part1_triggerDuration']
        elif (self.partNumber == 2): controller = cc_values.controllers['part2_triggerDuration']
        elif (self.partNumber == 3): controller = cc_values.controllers['part3_triggerDuration']
        elif (self.partNumber == 4): controller = cc_values.controllers['part4_triggerDuration']
        # set value
        value = cc_values.trigger_duration[choice]
        # send value to midi output
        midiManager.SendCC(controller, value)
    
    def OnVelocityScaleSelect(self, event):
        ''' combobox '''
        # get event type
        if (event == 'default'): choice = default_velocityScale
        elif (event == 'random'): choice = random.choice(cc_values.boolean.keys())
        else: choice = event.GetString()
        # correct combobox value 
        self.cbox_velocityScale.SetValue(choice)
        # set controller
        if   (self.partNumber == 1): controller = cc_values.controllers['part1_velocityScale']
        elif (self.partNumber == 2): controller = cc_values.controllers['part2_velocityScale']
        elif (self.partNumber == 3): controller = cc_values.controllers['part3_velocityScale']
        elif (self.partNumber == 4): controller = cc_values.controllers['part4_velocityScale']
        # set value
        value = cc_values.boolean[choice]
        # send value to midi output
        midiManager.SendCC(controller, value)
    
    def OnTriggerShapeSelect(self, event):
        ''' combobox '''
        # get event type
        if (event == 'default'): choice = default_triggerShape
        elif (event == 'random'): choice = random.choice(cc_values.trigger_shape.keys())
        else: choice = event.GetString()
        # correct combobox value 
        self.cbox_triggerShape.SetValue(choice)
        # set controller
        if   (self.partNumber == 1): controller = cc_values.controllers['part1_triggerShape']
        elif (self.partNumber == 2): controller = cc_values.controllers['part2_triggerShape']
        elif (self.partNumber == 3): controller = cc_values.controllers['part3_triggerShape']
        elif (self.partNumber == 4): controller = cc_values.controllers['part4_triggerShape']
        # set value
        value = cc_values.trigger_shape[choice]
        # send value to midi output
        midiManager.SendCC(controller, value)
    
    def OnAuxCvOutSelect(self, event):
        ''' combobox '''
        # get event type
        if (event == 'default'): choice = default_auxCV
        elif (event == 'random'): choice = random.choice(cc_values.aux_cv.keys())
        else: choice = event.GetString()
        # correct combobox value 
        self.cbox_auxCvOut.SetValue(choice)
        # set controller
        if   (self.partNumber == 1): controller = cc_values.controllers['part1_auxCVout']
        elif (self.partNumber == 2): controller = cc_values.controllers['part2_auxCVout']
        elif (self.partNumber == 3): controller = cc_values.controllers['part3_auxCVout']
        elif (self.partNumber == 4): controller = cc_values.controllers['part4_auxCVout']
        # set value
        value = cc_values.aux_cv[choice]
        # send value to midi output
        midiManager.SendCC(controller, value)
    
    def OnOscShapeSelect(self, event):
        ''' combobox '''
        # get event type
        if (event == 'default'): choice = default_oscillator
        elif (event == 'random'): choice = random.choice(cc_values.oscillator.keys())
        else: choice = event.GetString()
        # correct combobox value 
        self.cbox_oscShape.SetValue(choice)
        # set controller
        if   (self.partNumber == 1): controller = cc_values.controllers['part1_oscillatorShape']
        elif (self.partNumber == 2): controller = cc_values.controllers['part2_oscillatorShape']
        elif (self.partNumber == 3): controller = cc_values.controllers['part3_oscillatorShape']
        elif (self.partNumber == 4): controller = cc_values.controllers['part4_oscillatorShape']
        # set value
        value = cc_values.oscillator[choice]
        # send value to midi output
        midiManager.SendCC(controller, value)
    
    def OnArpClockDivSelect(self, event):
        ''' combobox '''
        # get event type
        if (event == 'default'): choice = default_arpClockDiv
        elif (event == 'random'): choice = random.choice(cc_values.arp_clock_division.keys())
        else: choice = event.GetString()
        # correct combobox value 
        self.cbox_arpClockDiv.SetValue(choice)
        # set controller
        if   (self.partNumber == 1): controller = cc_values.controllers['part1_arpClockDiv']
        elif (self.partNumber == 2): controller = cc_values.controllers['part2_arpClockDiv']
        elif (self.partNumber == 3): controller = cc_values.controllers['part3_arpClockDiv']
        elif (self.partNumber == 4): controller = cc_values.controllers['part4_arpClockDiv']
        # set value
        value = cc_values.arp_clock_division[choice]
        # send value to midi output
        midiManager.SendCC(controller, value)
    
    def OnArpGateLengthSelect(self, event):
        ''' combobox '''
        # get event type
        if (event == 'default'): choice = default_arpGateLength
        elif (event == 'random'): choice = random.choice(cc_values.arp_gate_length.keys())
        else: choice = event.GetString()
        # correct combobox value 
        self.cbox_arpGateLength.SetValue(choice)
        # set controller
        if   (self.partNumber == 1): controller = cc_values.controllers['part1_arpGateLength']
        elif (self.partNumber == 2): controller = cc_values.controllers['part2_arpGateLength']
        elif (self.partNumber == 3): controller = cc_values.controllers['part3_arpGateLength']
        elif (self.partNumber == 4): controller = cc_values.controllers['part4_arpGateLength']
        # set value
        value = cc_values.arp_gate_length[choice]
        # send value to midi output
        midiManager.SendCC(controller, value)
    
    def OnArpRangeSelect(self, event):
        ''' combobox '''
        # get event type
        if (event == 'default'): choice = default_arpRange
        elif (event == 'random'): choice = random.choice(cc_values.arp_range.keys())
        else: choice = event.GetString()
        # correct combobox value 
        self.cbox_arpRange.SetValue(choice)
        # set controller
        if   (self.partNumber == 1): controller = cc_values.controllers['part1_arpRange']
        elif (self.partNumber == 2): controller = cc_values.controllers['part2_arpRange']
        elif (self.partNumber == 3): controller = cc_values.controllers['part3_arpRange']
        elif (self.partNumber == 4): controller = cc_values.controllers['part4_arpRange']
        # set value
        value = cc_values.arp_range[choice]
        # send value to midi output
        midiManager.SendCC(controller, value)
    
    def OnArpDirectionSelect(self, event):
        ''' combobox '''
        # get event type
        if (event == 'default'): choice = default_arpDirection
        elif (event == 'random'): choice = random.choice(cc_values.arp_direction.keys())
        else: choice = event.GetString()
        # correct combobox value 
        self.cbox_arpDirection.SetValue(choice)
        # set controller
        if   (self.partNumber == 1): controller = cc_values.controllers['part1_arpDirection']
        elif (self.partNumber == 2): controller = cc_values.controllers['part2_arpDirection']
        elif (self.partNumber == 3): controller = cc_values.controllers['part3_arpDirection']
        elif (self.partNumber == 4): controller = cc_values.controllers['part4_arpDirection']
        # set value
        value = cc_values.arp_direction[choice]
        # send value to midi output
        midiManager.SendCC(controller, value)
    
    def OnArpPatternSelect(self, event):
        ''' combobox '''
        # get event type
        if (event == 'default'): choice = default_arpPattern
        elif (event == 'random'): choice = random.choice(cc_values.arp_pattern.keys())
        else: choice = event.GetString()
        # correct combobox value 
        self.cbox_arpPattern.SetValue(choice)
        # set controller
        if   (self.partNumber == 1): controller = cc_values.controllers['part1_arpPattern']
        elif (self.partNumber == 2): controller = cc_values.controllers['part2_arpPattern']
        elif (self.partNumber == 3): controller = cc_values.controllers['part3_arpPattern']
        elif (self.partNumber == 4): controller = cc_values.controllers['part4_arpPattern']
        # set value
        value = cc_values.arp_pattern[choice]
        # send value to midi output
        midiManager.SendCC(controller, value)

    def OnEucLengthSelect(self, event):
        ''' combobox '''
        # get event type
        if (event == 'default'): choice = default_eucLength
        elif (event == 'random'): choice = random.choice(cc_values.euclidean.keys())
        else: choice = event.GetString()
        # correct combobox value 
        self.cbox_eucLength.SetValue(choice)
        # set controller
        if   (self.partNumber == 1): controller = cc_values.controllers['part1_euclideanLength']
        elif (self.partNumber == 2): controller = cc_values.controllers['part2_euclideanLength']
        elif (self.partNumber == 3): controller = cc_values.controllers['part3_euclideanLength']
        elif (self.partNumber == 4): controller = cc_values.controllers['part4_euclideanLength']
        # set value
        value = cc_values.euclidean[choice]
        # send value to midi output
        midiManager.SendCC(controller, value)

    def OnEucFillSelect(self, event):
        ''' combobox '''
        # get event type
        if (event == 'default'): choice = default_eucFill
        elif (event == 'random'): choice = random.choice(cc_values.euclidean.keys())
        else: choice = event.GetString()
        # correct combobox value 
        self.cbox_eucFill.SetValue(choice)
        # set controller
        if   (self.partNumber == 1): controller = cc_values.controllers['part1_euclideanFill']
        elif (self.partNumber == 2): controller = cc_values.controllers['part2_euclideanFill']
        elif (self.partNumber == 3): controller = cc_values.controllers['part3_euclideanFill']
        elif (self.partNumber == 4): controller = cc_values.controllers['part4_euclideanFill']
        # set value
        value = cc_values.euclidean[choice]
        # send value to midi output
        midiManager.SendCC(controller, value)

    def OnEucRotateSelect(self, event):
        ''' combobox '''
        # get event type
        if (event == 'default'): choice = default_eucRotate
        elif (event == 'random'): choice = random.choice(cc_values.euclidean.keys())
        else: choice = event.GetString()
        # correct combobox value 
        self.cbox_eucRotate.SetValue(choice)
        # set controller
        if   (self.partNumber == 1): controller = cc_values.controllers['part1_euclideanRotate']
        elif (self.partNumber == 2): controller = cc_values.controllers['part2_euclideanRotate']
        elif (self.partNumber == 3): controller = cc_values.controllers['part3_euclideanRotate']
        elif (self.partNumber == 4): controller = cc_values.controllers['part4_euclideanRotate']
        # set value
        value = cc_values.euclidean[choice]
        # send value to midi output
        midiManager.SendCC(controller, value)

    def SendDefaults(self):
        ''' inits yarns with some default settings '''
        self.OnVibratoRangeSelect('default')
        self.OnVibratoSpeedSelect('default')
        self.OnPitchBendRangeSelect('default')
        self.OnTransposeSelect('default')
        self.OnFineTuningSelect('default')
        self.OnTriggerDurationSelect('default')
        self.OnArpRangeSelect('default')
        self.OnArpPatternSelect('default')
        self.OnArpGateLengthSelect('default')
        self.OnEucLengthSelect('default')
        self.OnEucFillSelect('default')
        self.OnEucRotateSelect('default')
        self.OnPortamentoSelect('default')
        self.OnChannelSelect('default')
        self.OnLowerNoteSelect('default')
        self.OnUpperNoteSelect('default')
        self.OnMidiOutModeSelect('default')
        self.OnVoicingSelect('default')
        self.OnNotePrioritySelect('default')
        self.OnLegatoSelect('default')
        self.OnTuningRootSelect('default')
        self.OnTuningSystemSelect('default')
        self.OnVelocityScaleSelect('default')
        self.OnTriggerShapeSelect('default')
        self.OnAuxCvOutSelect('default')
        self.OnOscShapeSelect('default')
        self.OnArpClockDivSelect('default')
        self.OnArpDirectionSelect('default')


class EditorSettings(wx.Panel):
    ''' the editor's configuration page '''
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)

        # rows, columns, vertical gap, horizontal gap
        grid = wx.FlexGridSizer(28, 2, 8, 16)

        # column, proportion
        grid.AddGrowableCol(0,1)
        grid.AddGrowableCol(1,1)

        # midi input devices
        txt_midi_in = wx.StaticText(self, label='MIDI Input Device:')
        listbox_midi_in = wx.ListBox(self)
        listbox_midi_in.Bind(wx.EVT_LISTBOX, self.OnInputClick)
        listbox_midi_in.SetMinSize((0, 200))

        # midi output devices
        txt_midi_out = wx.StaticText(self, label='MIDI Output Device:')
        listbox_midi_out = wx.ListBox(self)
        listbox_midi_out.Bind(wx.EVT_LISTBOX, self.OnOutputClick)
        listbox_midi_in.SetMinSize((0, 200))

        # remote control channel
        txt_channel = wx.StaticText(self, label='MIDI RC Channel:')
        spin_channel = wx.SpinCtrl(self, value=default_remoteChannel)
        spin_channel.Bind(wx.EVT_SPINCTRL, self.OnRemoteChannelSelect)
        spin_channel.SetRange(1, 16)

        # notes
        txt_notes = wx.StaticText(self, label='Set MIDI channel to match Yarns RC channel.\n' + 
                                              'Restart program to refresh attached devices.\n' +
                                              'This program only supports firmware %s' %(firmware))
        # select button
        self.btn_confirm = wx.Button(self, label='Confirm Settings')
        self.btn_confirm.Bind(wx.EVT_BUTTON, self.OnConfirm)

        # add it all to the grid sizer
        grid.AddMany([
            (txt_midi_in),                   (txt_midi_out),
            (listbox_midi_in, 1, wx.EXPAND), (listbox_midi_out, 1, wx.EXPAND),
            (txt_channel),                   (wx.StaticText(self, label='')),
            (spin_channel),                  (wx.StaticText(self, label=''))])

        # add grid sizer to sizer
        self.sizer.Add(grid, 1, wx.EXPAND)
        self.sizer.Add(txt_notes, 0, wx.EXPAND)
        self.sizer.Add(self.btn_confirm, 0, wx.ALIGN_RIGHT)

        # init midi
        midiManager.InitMIDI()

        # populate MIDI information
        for midi_device in midiManager.ListMIDI('input'):
            listbox_midi_in.Append(midi_device)

        for midi_device in midiManager.ListMIDI('output'):
            listbox_midi_out.Append(midi_device)          

    def OnRemoteChannelSelect(self, event):
        ''' selects the midi channel '''
        choice = event.GetInt()
        midiManager.SetChannel(choice)

    def OnConfirm(self, event):
        ''' locks the midi output/channel coice for the session '''
        # midi output device is required
        if (midiManager.midi_output_port == None):
            errorMsg = wx.MessageDialog(None, 'You must select a MIDI output device!', 'Error', 
                wx.OK | wx.ICON_ERROR)
            errorMsg.ShowModal()
        else: self.parent.OnConfirm() # parent function handles this

    def OnInputClick(self, event):
        ''' called when the user clicks a midi input device in the listbox'''
        midiManager.SetInput(event.GetString())

    def OnOutputClick(self, event):
        ''' called when the user clicks a midi output device in the listbox '''
        midiManager.SetOutput(event.GetString())

class Editor(wx.Notebook):
    ''' all the panels put together in a "notebook" style (with tabs) '''
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, id=wx.ID_ANY, style=wx.BK_TOP)

        # Create the tabs and add them to the notebook
        self.page_editor = EditorSettings(self)
        self.AddPage(self.page_editor, 'Editor')

    def OnConfirm(self):
        ''' confirms midi device selection '''

        # close/re open midi ports
        midiManager.CloseMIDI()
        midiManager.OpenMIDI()

         # add layout panel
        self.OnPartChange(0)
        self.ChangeSelection(1)

    def KillPage(self, pageText):
        ''' removes a notebook page based on its page label '''
        for index in range(self.GetPageCount()):
            if (self.GetPageText(index) == pageText):
                self.DeletePage(index)
                self.SendSizeEvent()
                break

    def OnPartChange(self, number_of_parts):
        ''' enables/disables tabs as layouts are changed '''
        if (number_of_parts == 0):
            # add the layout panel if it doesn't exist
            if (self.GetPageCount() == 1):
                page_layout = LayoutSettings(self)
                self.AddPage(page_layout, 'Layout')
                page_layout.SendDefaults()

        elif (number_of_parts == 1):
            # remove parts 2, 3, and 4 if they exist
            self.KillPage('Part 2')
            self.KillPage('Part 3')
            self.KillPage('Part 4')
            # add page 1 if it doesn't exist
            if (self.GetPageCount() == 2):
                page_part1 = PartSettings(self, 1)
                self.AddPage(page_part1, 'Part 1')
                page_part1.SendDefaults()

        elif (number_of_parts == 2):
            # remove parts 3 and 4 if they exist
            self.KillPage('Part 3')
            self.KillPage('Part 4')
            # add page 2 if it doesn't exist
            if (self.GetPageCount() == 3):
                page_part2 = PartSettings(self, 2)
                self.AddPage(page_part2, 'Part 2')
                page_part2.SendDefaults()

        elif (number_of_parts == 4):
            if (self.GetPageCount() == 4):
                # add parts 3 and 4 if they don't exist
                page_part3 = PartSettings(self, 3)
                page_part4 = PartSettings(self, 4)
                self.AddPage(page_part3, 'Part 3')
                self.AddPage(page_part4, 'Part 4')
                page_part3.SendDefaults()
                page_part4.SendDefaults()
            elif (self.GetPageCount() == 3):
                # add parts 2, 3, and 4 if they don't exist
                page_part2 = PartSettings(self, 2)
                page_part3 = PartSettings(self, 3)
                page_part4 = PartSettings(self, 4)
                self.AddPage(page_part2, 'Part 2')
                self.AddPage(page_part3, 'Part 3')
                self.AddPage(page_part4, 'Part 4')
                page_part2.SendDefaults()
                page_part3.SendDefaults()
                page_part4.SendDefaults()
        else: 
            raise ValueError('Incorrect value passed to Editor.OnPartChange()')


class Window(wx.Frame):
    ''' the application window. '''
    def __init__(self):
        wx.Frame.__init__(self, 
                          parent=None,
                          title='Yarns Editor',
                          style=wx.DEFAULT_FRAME_STYLE)

        # platform specific tweaks
        os = platform.system().lower()
        if (os == 'windows'):
            appID = 'Yarns Editor'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appID)
            xSize = 600
            ySize = 560
        elif (os == 'darwin'):
            xSize = 690
            ySize = 570
        elif (os == 'linux'):
            xSize = 740
            ySize = 570
        else:
            xSize = 600
            ySize = 560

        # TODO: dynamically set correct sizes
        self.SetSize((xSize, ySize))
        self.SetMinSize((xSize, ySize))
        self.SetIcon(images.icon.GetIcon())
        self.Bind(wx.EVT_CLOSE, self.OnQuit)
        self.InitMenubar()
        self.InitGUI()

    def InitGUI(self):
        ''' creates the window elements '''
        panel = wx.Panel(self)
        notebook = Editor(panel)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.EXPAND)
        sizer.Layout() # causes black box glitch if omitted
        panel.SetSizer(sizer)
        self.Layout()
        self.Centre()
        self.Show()

    def InitMenubar(self):
        ''' creates the menubar contents '''
        # create menubar
        menubar = wx.MenuBar()

        # file menu
        fileMenu = wx.Menu()
        fileMenu_quit = fileMenu.Append(wx.ID_EXIT, '&Quit Yarns Editor')
        self.Bind(wx.EVT_MENU, self.OnQuit, id=wx.ID_EXIT)

        # help menu
        helpMenu = wx.Menu()
        helpMenu_about = helpMenu.Append(wx.ID_ABOUT, '&About Yarns Editor')
        self.Bind(wx.EVT_MENU, self.OnAbout, id=wx.ID_ABOUT)

        # add items to menubar
        menubar.Append(fileMenu, '&File')
        menubar.Append(helpMenu, '&Help')
        self.SetMenuBar(menubar)

    def OnQuit(self, event):
        ''' called when the user quits '''
        midiManager.CloseMIDI()
        self.Destroy()

    def OnAbout(self, event):
        ''' Called when the user chooses "About" from the help menu '''
        info = wx.AboutDialogInfo()
        info.SetIcon(images.icon.GetIcon())
        info.Name = 'Yarns Editor'
        info.Version = '0.9'
        info.Copyright = '(C) 2015 Panagiotis Peppas'
        info.License = license
        info.Description = 'A MIDI editor for Mutable Instruments Yarns.'
        info.WebSite = ('https://github.com/notinachos/yarns-editor', 'Source code on Github')
        wx.AboutBox(info)

if __name__ == '__main__':
    global midiManager

    # handles midi events
    midiManager = MidiManager()
    midiManager.SetChannel(default_remoteChannel)

    # the wx app
    app = wx.App()
    frame = Window()
    app.MainLoop()
    sys.exit(0)