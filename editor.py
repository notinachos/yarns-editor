"""
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
Portions of this software may include text and/or graphics from Mutable
Instruments, provided under the cc-by-sa 3.0 license. The author of this
software is not endorsed by Mutable Instruments. Their company website, and
the license, can be found at the following address:
http://mutable-instruments.net/
"""

# imports
import ctypes
import platform
import random
import rtmidi_python as rtmidi
import sys

import wx
from natsort import natsorted

import cc_values
import images

# the editor only supports the following Yarns firmware version:
firmware = '1.1'

# information for the layout editor page
info_1M = 'In this mode, Yarns offers a single voice of CV/Gate conversion.'

info_2M = (
    'In this mode, Yarns provides two independent monophonic voices. The '
    'voices are independent in the sense that they can play different '
    'sequences, respond to different MIDI channels, etc.'
)

info_4M = 'In this mode, Yarns provides four independent monophonic voices.'

info_2P = (
    'In this mode, Yarns provides a single part made of two voices. '
    'The incoming notes are dispatched to these two voices.'
)

info_4P = (
    'In this mode, Yarns provides a single part made of four voices. '
    'The incoming notes are dispatched to these four voices.'
)

info_2poly = (
    'In this mode, Yarns provides a single part made of two voices. '
    'However, only the first voice is handled by Yarns\' CV/Gate outputs. '
    'The second voice is simply forwarded as MIDI Note on/off messages the '
    'MIDI out. This allows "ping-pong" play between the modules connected '
    'to Yarns and another MIDI instrument. This can also be used to chain '
    'several instances of Yarns to get more CV outputs.'
)

info_4poly = (
    'In this mode, Yarns provides a single part made of 4voices. Only the '
    'first half of the voices are handled by Yarns\' CV/Gate outputs. Notes '
    'allocated to the other voices are forwarded to the MIDI output.'
)

info_8poly = (
    'In this mode, Yarns provides a single part made of 8 voices. Only the '
    'first half of the voices are handled by Yarns\' CV/Gate outputs. Notes '
    'allocated to the other voices are forwarded to the MIDI output.'
)

info_4trig = (
    'This layout is optimized for controlling percussion patches (for '
    'example from MIDI drum pads, or from a MIDI drum sequencer). It offers '
    '4 parts, each of them listening to a single MIDI note. No control '
    'voltage is emitted - just a trigger, freeing some outputs to emit '
    'additional gate and clock signals.'
)

info_3plus = (
    '3+ mode with 2 parts, designed specially for Edges. The first part has '
    '3 voices of polyphony on channels 1-3, and the second part is '
    'monophonic, on channel 4.'
)


class MidiManager:
    """Handles MIDI events. """

    def __init__(self):
        self.midi_channel = None
        self.midi_input_device = None
        self.midi_output_device = None
        self.midi_input_port = None
        self.midi_output_port = None

    def init_midi(self):
        """Initializes MIDI. """
        self.midi_input_device = rtmidi.MidiIn()
        self.midi_output_device = rtmidi.MidiOut()

    def list_midi_devices(self, port_direction):
        """Returns a list of available midi devices.

        :param port_direction: specify 'input' or 'output' midi port to detect
        :return midi_devices: a list of detected midi input or output ports
        """
        if port_direction == 'input':
            midi_devices = self.midi_input_device.ports
        elif port_direction == 'output':
            midi_devices = self.midi_output_device.ports
        else:
            raise ValueError(
                'Incorrect value passed to MidiManager.list_midi_devices()'
            )
        return midi_devices

    def set_midi_input(self, device_name):
        """Sets the midi input port to use.

        :param device_name: name of the midi input
        """
        self.midi_input_port = device_name

    def set_midi_output(self, device_name):
        """Sets the midi output port to use.

        :param device_name: name of the midi output
        """
        self.midi_output_port = device_name

    def set_channel(self, channel):
        """Sets the midi channel to use.

        :param channel: midi channel 1-16
        """
        if 1 <= int(channel) <= 16:
            self.midi_channel = int(channel)
        else:
            raise ValueError(
                'Incorrect value passed to MidiManager.set_channel()'
            )

    def open_midi(self):
        """Looks up the ports by the index, and opens them. """
        if self.midi_input_port:  # midi input device is optional
            self.midi_input_device.open_port(
                self.midi_input_device.ports.index(self.midi_input_port))
        self.midi_output_device.open_port(
            self.midi_output_device.ports.index(self.midi_output_port))

    def close_midi(self):
        """Looks up the open ports by the index, and closes them. """
        if self.midi_input_port:
            self.midi_input_device.close_port()
        if self.midi_output_port:
            self.midi_output_device.close_port()

    def send_cc(self, controller, value):
        """Sends data to the MIDI output.

        :param controller: the CC number
        :param value: the CC value
        """
        # 1st byte changes depending on the midi channel
        if self.midi_channel == 1:
            byte1 = 0xB0
        elif self.midi_channel == 2:
            byte1 = 0xB1
        elif self.midi_channel == 3:
            byte1 = 0xB2
        elif self.midi_channel == 4:
            byte1 = 0xB3
        elif self.midi_channel == 5:
            byte1 = 0xB4
        elif self.midi_channel == 6:
            byte1 = 0xB5
        elif self.midi_channel == 7:
            byte1 = 0xB6
        elif self.midi_channel == 8:
            byte1 = 0xB7
        elif self.midi_channel == 9:
            byte1 = 0xB8
        elif self.midi_channel == 10:
            byte1 = 0xB9
        elif self.midi_channel == 11:
            byte1 = 0xBA
        elif self.midi_channel == 12:
            byte1 = 0xBB
        elif self.midi_channel == 13:
            byte1 = 0xBC
        elif self.midi_channel == 14:
            byte1 = 0xBD
        elif self.midi_channel == 15:
            byte1 = 0xBE
        elif self.midi_channel == 16:
            byte1 = 0xBF
        else:
            raise ValueError(
                'Incorrect value passed to MidiManager.send_cc()'
            )
        # send CC 
        self.midi_output_device.send_message([byte1, controller, value])


class LayoutSettings(wx.Panel):
    """The configuration page for layout options. """

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
            if 'default' not in each:
                tempo_menu.append(each)
        tempo_menu = natsorted(tempo_menu)

        swing_menu = []
        for each in cc_values.swing:
            if 'default' not in each:
                swing_menu.append(each)
        swing_menu = natsorted(swing_menu)

        layout_menu = []
        for each in cc_values.layout:
            if 'default' not in each:
                layout_menu.append(each)
        layout_menu = natsorted(layout_menu)

        # comboboxes
        self.combobox_tempo = wx.ComboBox(
            self,
            choices=tempo_menu,
            value=cc_values.tempo['default'],
            style=wx.CB_READONLY
        )
        self.combobox_swing = wx.ComboBox(
            self,
            choices=swing_menu,
            value=cc_values.swing['default'],
            style=wx.CB_READONLY
        )
        self.combobox_layouts = wx.ComboBox(
            self,
            choices=layout_menu,
            value=cc_values.layout['default'],
            style=wx.CB_READONLY
        )

        # combobox bindings
        self.combobox_tempo.Bind(wx.EVT_COMBOBOX, self.on_tempo_select)
        self.combobox_swing.Bind(wx.EVT_COMBOBOX, self.on_swing_select)
        self.combobox_layouts.Bind(wx.EVT_COMBOBOX, self.on_layout_select)

        # add it all to the sizer
        self.sizer.Add(txt_tempo)
        self.sizer.Add(self.combobox_tempo)
        self.sizer.Add(txt_swing)
        self.sizer.Add(self.combobox_swing)
        self.sizer.Add(txt_layout)
        self.sizer.Add(self.combobox_layouts)

        # default layout placeholders
        image = images.layout_1M.GetBitmap()
        self.layout_image = wx.StaticBitmap(
            self,
            -1,
            image,
            (0, 0),
            (image.GetWidth(), image.GetHeight())
        )

        self.txt_info = wx.StaticText(self, label=info_1M)
        self.sizer.Add(wx.StaticText(self, label=''))
        self.sizer.Add(self.layout_image, 1, wx.ALIGN_CENTRE)
        self.sizer.Add(self.txt_info, 0, wx.ALIGN_CENTRE)

    def change_layout(self, layout):
        """Changes the layout image/text. also enables/disables tabs.

        :param layout: the layout to switch to
        """
        # pick correct layout image
        if layout == '1M - Monophonic':
            new_image = images.layout_1M.GetBitmap()
            self.parent.on_part_change(1)
            self.txt_info.SetLabel(info_1M)

        elif layout == '2M - Dual monophonic':
            new_image = images.layout_2M.GetBitmap()
            self.parent.on_part_change(2)
            self.txt_info.SetLabel(info_2M)

        elif layout == '4M - Quad monophonic':
            new_image = images.layout_4M.GetBitmap()
            self.parent.on_part_change(4)
            self.txt_info.SetLabel(info_4M)

        elif layout == '2P - Duophonic':
            new_image = images.layout_2P.GetBitmap()
            self.parent.on_part_change(1)
            self.txt_info.SetLabel(info_2P)

        elif layout == '4P - Quadraphonic':
            new_image = images.layout_4P.GetBitmap()
            self.parent.on_part_change(1)
            self.txt_info.SetLabel(info_4poly)

        elif layout == '2> - Duophonic polychaining':
            new_image = images.layout_2P_chain.GetBitmap()
            self.parent.on_part_change(1)
            self.txt_info.SetLabel(info_2poly)

        elif layout == '4> - Quadraphonic polychaining':
            new_image = images.layout_4P_chain.GetBitmap()
            self.parent.on_part_change(1)
            self.txt_info.SetLabel(info_4poly)

        elif layout == '8> - Octophonic polychaining':
            new_image = images.layout_8P_chain.GetBitmap()
            self.parent.on_part_change(1)
            self.txt_info.SetLabel(info_8poly)

        elif layout == '4T - Quad trigger':
            new_image = images.layout_4T.GetBitmap()
            self.parent.on_part_change(4)
            self.txt_info.SetLabel(info_4trig)

        elif layout == '3+ - Three plus one':
            new_image = images.layout_3plus.GetBitmap()
            self.parent.on_part_change(2)
            self.txt_info.SetLabel(info_3plus)

        else:
            raise ValueError(
                'Incorrect value passed to LayoutSettings.change_layout()'
            )

        # set the new display image
        self.layout_image.SetBitmap(new_image)

        # refresh layout
        self.sizer.Layout()

    def on_tempo_select(self, event):
        """Called when the user selects a value from the combobox.

        :param event: the wxPython event
        """
        # get event type
        if event == 'default':
            choice = cc_values.tempo['default']
        elif event == 'random':
            choice = random.choice(cc_values.tempo.keys())
        else:
            choice = event.GetString()
        # correct combobox value 
        self.combobox_tempo.SetValue(choice)
        # set controller
        controller = cc_values.controllers['yarns_tempo']
        # set cc value
        value = cc_values.tempo[choice]
        # send cc message to midi output
        midiManager.send_cc(controller, value)

    def on_swing_select(self, event):
        """Called when the user selects a value from the combobox.

        :param event: the wxPython event
        """
        # get event type
        if event == 'default':
            choice = cc_values.swing['default']
        elif event == 'random':
            choice = random.choice(cc_values.swing.keys())
        else:
            choice = event.GetString()
        # correct combobox value 
        self.combobox_swing.SetValue(choice)
        # set controller
        controller = cc_values.controllers['yarns_swing']
        # set cc value
        value = cc_values.swing[choice]
        # send cc message to midi output
        midiManager.send_cc(controller, value)

    def on_layout_select(self, event):
        """Called when the user selects a value from the combobox.

        :param event: the wxPython event
        """
        # get event type
        if event == 'default':
            choice = cc_values.layout['default']
        elif event == 'random':
            choice = random.choice(cc_values.layout.keys())
        else:
            choice = event.GetString()
        # correct combobox value 
        self.combobox_layouts.SetValue(choice)
        # set controller
        controller = cc_values.controllers['yarns_layout']
        # set cc value
        value = cc_values.layout[choice]
        # send cc message to midi output
        midiManager.send_cc(controller, value)

        # change layout image/text
        self.change_layout(choice)

    def send_defaults(self):
        """Initialises yarns with some default settings. """
        self.on_layout_select('default')
        self.on_tempo_select('default')
        self.on_swing_select('default')


class PartSettings(wx.Panel):
    """The configuration page for a single part. """

    def __init__(self, parent, part_number):
        wx.Panel.__init__(self, parent)
        # the part number (1-4) that the page controls
        self.part_number = part_number
        # a list of checked boxes
        self.checkedBoxes = []
        # rows, columns, vertical gap, horizontal gap
        grid = wx.FlexGridSizer(28, 4, 8, 8)

        # add grid to panel
        self.SetSizer(grid)

        # checkboxes/text labels
        chk_midi_channel = wx.CheckBox(self, label='MIDI channel:')
        chk_lower_note = wx.CheckBox(self, label='Lower note:')
        chk_upper_note = wx.CheckBox(self, label='Upper note:')
        chk_midi_output_mode = wx.CheckBox(self, label='MIDI out mode:')
        chk_voicing = wx.CheckBox(self, label='Voicing:')
        chk_note_priority = wx.CheckBox(self, label='Note priority:')
        chk_portamento = wx.CheckBox(self, label='Portamento:')
        chk_legato = wx.CheckBox(self, label='Legato:')
        chk_pitch_bend_range = wx.CheckBox(self, label='Pitch bend range:')
        chk_vibrato_range = wx.CheckBox(self, label='Vibrato range:')
        chk_vibrato_speed = wx.CheckBox(self, label='Vibrato speed:')
        chk_transpose = wx.CheckBox(self, label='Transpose:')
        chk_fine_tuning = wx.CheckBox(self, label='Fine tuning:')
        chk_tuning_root = wx.CheckBox(self, label='Tuning root:')
        chk_tuning_system = wx.CheckBox(self, label='Tuning system:')
        chk_trigger_duration = wx.CheckBox(self, label='Trigger duration:')
        chk_velocity_scale = wx.CheckBox(self, label='Trigger velocity scale:')
        chk_trigger_shape = wx.CheckBox(self, label='Trigger shape:')
        chk_aux_cv_out = wx.CheckBox(self, label='Aux CV out:')
        chk_osc_shape = wx.CheckBox(self, label='Oscillator shape:')
        chk_arp_clock_div = wx.CheckBox(self, label='Arp/Seq clock divider:')
        chk_arp_gate_length = wx.CheckBox(self, label='Arp/Seq gate length:')
        chk_arp_range = wx.CheckBox(self, label='Arpeggiator range:')
        chk_arp_direction = wx.CheckBox(self, label='Arpeggiator direction:')
        chk_arp_pattern = wx.CheckBox(self, label='Arpeggiator pattern:')
        chk_euclidean_length = wx.CheckBox(self, label='Euclidean length:')
        chk_euclidean_fill = wx.CheckBox(self, label='Euclidean fill:')
        chk_euclidean_rotate = wx.CheckBox(self, label='Euclidean rotate:')

        # checkbox bindings
        chk_midi_channel.Bind(wx.EVT_CHECKBOX, self.on_box_checked)
        chk_lower_note.Bind(wx.EVT_CHECKBOX, self.on_box_checked)
        chk_upper_note.Bind(wx.EVT_CHECKBOX, self.on_box_checked)
        chk_midi_output_mode.Bind(wx.EVT_CHECKBOX, self.on_box_checked)
        chk_voicing.Bind(wx.EVT_CHECKBOX, self.on_box_checked)
        chk_note_priority.Bind(wx.EVT_CHECKBOX, self.on_box_checked)
        chk_portamento.Bind(wx.EVT_CHECKBOX, self.on_box_checked)
        chk_legato.Bind(wx.EVT_CHECKBOX, self.on_box_checked)
        chk_pitch_bend_range.Bind(wx.EVT_CHECKBOX, self.on_box_checked)
        chk_vibrato_range.Bind(wx.EVT_CHECKBOX, self.on_box_checked)
        chk_vibrato_speed.Bind(wx.EVT_CHECKBOX, self.on_box_checked)
        chk_transpose.Bind(wx.EVT_CHECKBOX, self.on_box_checked)
        chk_fine_tuning.Bind(wx.EVT_CHECKBOX, self.on_box_checked)
        chk_tuning_root.Bind(wx.EVT_CHECKBOX, self.on_box_checked)
        chk_tuning_system.Bind(wx.EVT_CHECKBOX, self.on_box_checked)
        chk_trigger_duration.Bind(wx.EVT_CHECKBOX, self.on_box_checked)
        chk_velocity_scale.Bind(wx.EVT_CHECKBOX, self.on_box_checked)
        chk_trigger_shape.Bind(wx.EVT_CHECKBOX, self.on_box_checked)
        chk_aux_cv_out.Bind(wx.EVT_CHECKBOX, self.on_box_checked)
        chk_osc_shape.Bind(wx.EVT_CHECKBOX, self.on_box_checked)
        chk_arp_clock_div.Bind(wx.EVT_CHECKBOX, self.on_box_checked)
        chk_arp_gate_length.Bind(wx.EVT_CHECKBOX, self.on_box_checked)
        chk_arp_range.Bind(wx.EVT_CHECKBOX, self.on_box_checked)
        chk_arp_direction.Bind(wx.EVT_CHECKBOX, self.on_box_checked)
        chk_arp_pattern.Bind(wx.EVT_CHECKBOX, self.on_box_checked)
        chk_euclidean_length.Bind(wx.EVT_CHECKBOX, self.on_box_checked)
        chk_euclidean_fill.Bind(wx.EVT_CHECKBOX, self.on_box_checked)
        chk_euclidean_rotate.Bind(wx.EVT_CHECKBOX, self.on_box_checked)

        # populate menu contents
        midi_channel_menu = []
        for each in cc_values.channel:
            if 'default' not in each:
                midi_channel_menu.append(each)
        midi_channel_menu = natsorted(midi_channel_menu)

        midi_note_menu = []
        for each in cc_values.note:
            if 'default' not in each:
                midi_note_menu.append(each)
        midi_note_menu = natsorted(midi_note_menu)

        midi_output_menu = []
        for each in cc_values.midi_output:
            if 'default' not in each:
                midi_output_menu.append(each)
        midi_output_menu = natsorted(midi_output_menu)

        vibrato_speed_menu = []
        for each in cc_values.vibrato_speed:
            if 'default' not in each:
                vibrato_speed_menu.append(each)
        vibrato_speed_menu = natsorted(vibrato_speed_menu)

        voicing_menu = []
        for each in cc_values.voicing:
            if 'default' not in each:
                voicing_menu.append(each)
        voicing_menu = natsorted(voicing_menu)

        note_priority_menu = []
        for each in cc_values.note_priority:
            if 'default' not in each:
                note_priority_menu.append(each)
        note_priority_menu = natsorted(note_priority_menu)

        portamento_menu = []
        for each in cc_values.portamento:
            if 'default' not in each:
                portamento_menu.append(each)
        portamento_menu = natsorted(portamento_menu)

        boolean_menu = []
        for each in cc_values.boolean:
            if 'default' not in each:
                boolean_menu.append(each)
        boolean_menu = natsorted(boolean_menu)

        tuning_root_menu = []
        for each in cc_values.tuning_root:
            if 'default' not in each:
                tuning_root_menu.append(each)
        tuning_root_menu = natsorted(tuning_root_menu)

        tuning_system_menu = []
        for each in cc_values.tuning_system:
            if 'default' not in each:
                tuning_system_menu.append(each)
        tuning_system_menu = natsorted(tuning_system_menu)

        trigger_shape_menu = []
        for each in cc_values.trigger_shape:
            if 'default' not in each:
                trigger_shape_menu.append(each)
        trigger_shape_menu = natsorted(trigger_shape_menu)

        aux_cv_menu = []
        for each in cc_values.aux_cv:
            if 'default' not in each:
                aux_cv_menu.append(each)
        aux_cv_menu = natsorted(aux_cv_menu)

        oscillator_menu = []
        for each in cc_values.oscillator:
            if 'default' not in each:
                oscillator_menu.append(each)
        oscillator_menu = natsorted(oscillator_menu)

        arp_clock_menu = []
        for each in cc_values.arp_clock_division:
            if 'default' not in each:
                arp_clock_menu.append(each)
        arp_clock_menu = natsorted(arp_clock_menu)

        arp_direction_menu = []
        for each in cc_values.arp_direction:
            if 'default' not in each:
                arp_direction_menu.append(each)
        arp_direction_menu = natsorted(arp_direction_menu)

        pitch_bend_menu = []
        for each in cc_values.pitch_bend:
            if 'default' not in each:
                pitch_bend_menu.append(each)
        pitch_bend_menu = natsorted(pitch_bend_menu)

        vibrato_range_menu = []
        for each in cc_values.vibrato_range:
            if 'default' not in each:
                vibrato_range_menu.append(each)
        vibrato_range_menu = natsorted(vibrato_range_menu)

        transpose_menu = []
        for each in cc_values.transpose:
            if 'default' not in each:
                transpose_menu.append(each)
        transpose_menu = natsorted(transpose_menu)

        fine_tuning_menu = []
        for each in cc_values.fine_tuning:
            if 'default' not in each:
                fine_tuning_menu.append(each)
        fine_tuning_menu = natsorted(fine_tuning_menu)

        trigger_duration_menu = []
        for each in cc_values.trigger_duration:
            if 'default' not in each:
                trigger_duration_menu.append(each)
        trigger_duration_menu = natsorted(trigger_duration_menu)

        arp_range_menu = []
        for each in cc_values.arp_range:
            if 'default' not in each:
                arp_range_menu.append(each)
        arp_range_menu = natsorted(arp_range_menu)

        arp_pattern_menu = []
        for each in cc_values.arp_pattern:
            if 'default' not in each:
                arp_pattern_menu.append(each)
        arp_pattern_menu = natsorted(arp_pattern_menu)

        arp_gate_length_menu = []
        for each in cc_values.arp_gate_length:
            if 'default' not in each:
                arp_gate_length_menu.append(each)
        arp_gate_length_menu = natsorted(arp_gate_length_menu)

        euclidean_menu = []
        for each in cc_values.euclidean:
            if 'default' not in each:
                euclidean_menu.append(each)
        euclidean_menu = natsorted(euclidean_menu)

        # combo boxes
        self.combobox_trigger_duration = wx.ComboBox(
            self,
            choices=trigger_duration_menu,
            value=cc_values.trigger_duration['default'],
            style=wx.CB_READONLY
        )

        self.combobox_arp_range = wx.ComboBox(
            self,
            choices=arp_range_menu,
            value=cc_values.arp_range['default'],
            style=wx.CB_READONLY
        )

        self.combobox_arp_pattern = wx.ComboBox(
            self,
            choices=arp_pattern_menu,
            value=cc_values.arp_pattern['default'],
            style=wx.CB_READONLY
        )

        self.combobox_arp_gate_length = wx.ComboBox(
            self,
            choices=arp_gate_length_menu,
            value=cc_values.arp_gate_length['default'],
            style=wx.CB_READONLY
        )

        self.combobox_euclidean_length = wx.ComboBox(
            self,
            choices=euclidean_menu,
            value=cc_values.euclidean['default'],
            style=wx.CB_READONLY
        )

        self.combobox_euclidean_fill = wx.ComboBox(
            self,
            choices=euclidean_menu,
            value=cc_values.euclidean['default'],
            style=wx.CB_READONLY
        )

        self.combobox_euclidean_rotate = wx.ComboBox(
            self,
            choices=euclidean_menu,
            value=cc_values.euclidean['default'],
            style=wx.CB_READONLY)

        self.combobox_fine_tuning = wx.ComboBox(
            self,
            choices=fine_tuning_menu,
            value=cc_values.fine_tuning['default'],
            style=wx.CB_READONLY
        )

        self.combobox_transpose = wx.ComboBox(
            self,
            choices=transpose_menu,
            value=cc_values.transpose['default'],
            style=wx.CB_READONLY
        )

        self.combobox_vibrato_range = wx.ComboBox(
            self,
            choices=vibrato_range_menu,
            value=cc_values.vibrato_range['default'],
            style=wx.CB_READONLY
        )

        self.combobox_pitch_bend_range = wx.ComboBox(
            self,
            choices=pitch_bend_menu,
            value=cc_values.pitch_bend['default'],
            style=wx.CB_READONLY
        )

        self.combobox_portamento = wx.ComboBox(
            self,
            choices=portamento_menu,
            value=cc_values.portamento['default'],
            style=wx.CB_READONLY
        )

        self.combobox_midi_channel = wx.ComboBox(
            self,
            choices=midi_channel_menu,
            value=cc_values.channel['default'],
            style=wx.CB_READONLY
        )

        self.combobox_vibrato_speed = wx.ComboBox(
            self,
            choices=vibrato_speed_menu,
            value=cc_values.vibrato_speed['default'],
            style=wx.CB_READONLY
        )

        self.combobox_lower_note = wx.ComboBox(
            self,
            choices=midi_note_menu,
            value=cc_values.note['default low'],
            style=wx.CB_READONLY
        )

        self.combobox_upper_note = wx.ComboBox(
            self,
            choices=midi_note_menu,
            value=cc_values.note['default high'],
            style=wx.CB_READONLY
        )

        self.combobox_midi_output_mode = wx.ComboBox(
            self,
            choices=midi_output_menu,
            value=cc_values.midi_output['default'],
            style=wx.CB_READONLY
        )

        self.combobox_voicing = wx.ComboBox(
            self,
            choices=voicing_menu,
            value=cc_values.voicing['default'],
            style=wx.CB_READONLY
        )

        self.combobox_note_priority = wx.ComboBox(
            self,
            choices=note_priority_menu,
            value=cc_values.note_priority['default'],
            style=wx.CB_READONLY
        )

        self.combobox_legato = wx.ComboBox(
            self,
            choices=boolean_menu,
            value=cc_values.boolean['default'],
            style=wx.CB_READONLY
        )

        self.combobox_tuning_root = wx.ComboBox(
            self,
            choices=tuning_root_menu,
            value=cc_values.tuning_root['default'],
            style=wx.CB_READONLY
        )

        self.combobox_tuning_system = wx.ComboBox(
            self,
            choices=tuning_system_menu,
            value=cc_values.tuning_system['default'],
            style=wx.CB_READONLY
        )

        self.combobox_velocity_scale = wx.ComboBox(
            self,
            choices=boolean_menu,
            value=cc_values.boolean['default'],
            style=wx.CB_READONLY
        )

        self.combobox_trigger_shape = wx.ComboBox(
            self,
            choices=trigger_shape_menu,
            value=cc_values.trigger_shape['default'],
            style=wx.CB_READONLY
        )

        self.combobox_aux_cv_out = wx.ComboBox(
            self,
            choices=aux_cv_menu,
            value=cc_values.aux_cv['default'],
            style=wx.CB_READONLY
        )

        self.combobox_osc_shape = wx.ComboBox(
            self,
            choices=oscillator_menu,
            value=cc_values.oscillator['default'],
            style=wx.CB_READONLY
        )

        self.combobox_arp_clock_div = wx.ComboBox(
            self,
            choices=arp_clock_menu,
            value=cc_values.arp_clock_division['default'],
            style=wx.CB_READONLY
        )

        self.combobox_arp_direction = wx.ComboBox(
            self,
            choices=arp_direction_menu,
            value=cc_values.arp_direction['default'],
            style=wx.CB_READONLY
        )

        # combo box bindings
        self.combobox_pitch_bend_range.Bind(
            wx.EVT_COMBOBOX,
            self.on_pitch_bend_range_select
        )

        self.combobox_vibrato_range.Bind(
            wx.EVT_COMBOBOX,
            self.on_vibrato_range_select
        )

        self.combobox_transpose.Bind(
            wx.EVT_COMBOBOX,
            self.on_transpose_select
        )

        self.combobox_fine_tuning.Bind(
            wx.EVT_COMBOBOX,
            self.on_fine_tuning_select
        )

        self.combobox_trigger_duration.Bind(
            wx.EVT_COMBOBOX,
            self.on_trigger_duration_select
        )

        self.combobox_arp_range.Bind(
            wx.EVT_COMBOBOX,
            self.on_arp_range_select
        )

        self.combobox_arp_pattern.Bind(
            wx.EVT_COMBOBOX,
            self.on_arp_pattern_select
        )

        self.combobox_arp_gate_length.Bind(
            wx.EVT_COMBOBOX,
            self.on_arp_gate_length_select
        )

        self.combobox_euclidean_length.Bind(
            wx.EVT_COMBOBOX,
            self.on_euclidean_length_select
        )

        self.combobox_euclidean_fill.Bind(
            wx.EVT_COMBOBOX,
            self.on_euclidean_fill_select
        )

        self.combobox_euclidean_rotate.Bind(
            wx.EVT_COMBOBOX,
            self.on_euclidean_rotate_select
        )

        self.combobox_portamento.Bind(
            wx.EVT_COMBOBOX,
            self.on_portamento_select
        )

        self.combobox_midi_channel.Bind(
            wx.EVT_COMBOBOX,
            self.on_channel_select
        )

        self.combobox_lower_note.Bind(
            wx.EVT_COMBOBOX,
            self.on_lower_note_select
        )

        self.combobox_upper_note.Bind(
            wx.EVT_COMBOBOX,
            self.on_upper_note_select
        )

        self.combobox_midi_output_mode.Bind(
            wx.EVT_COMBOBOX,
            self.on_midi_output_mode_select
        )

        self.combobox_voicing.Bind(
            wx.EVT_COMBOBOX,
            self.on_voicing_select
        )

        self.combobox_note_priority.Bind(
            wx.EVT_COMBOBOX,
            self.on_note_priority_select
        )

        self.combobox_legato.Bind(
            wx.EVT_COMBOBOX,
            self.on_legato_select
        )

        self.combobox_vibrato_speed.Bind(
            wx.EVT_COMBOBOX,
            self.on_vibrato_speed_select
        )

        self.combobox_tuning_root.Bind(
            wx.EVT_COMBOBOX,
            self.on_tuning_root_select
        )

        self.combobox_tuning_system.Bind(
            wx.EVT_COMBOBOX,
            self.on_tuning_system_select
        )

        self.combobox_velocity_scale.Bind(
            wx.EVT_COMBOBOX,
            self.on_velocity_scale_select
        )

        self.combobox_trigger_shape.Bind(
            wx.EVT_COMBOBOX,
            self.on_trigger_shape_select
        )

        self.combobox_aux_cv_out.Bind(
            wx.EVT_COMBOBOX,
            self.on_aux_cv_output_select
        )

        self.combobox_osc_shape.Bind(
            wx.EVT_COMBOBOX,
            self.on_osc_shape_select
        )

        self.combobox_arp_clock_div.Bind(
            wx.EVT_COMBOBOX,
            self.on_arp_clock_divide_select
        )

        self.combobox_arp_direction.Bind(
            wx.EVT_COMBOBOX,
            self.on_arp_direction_select
        )

        # randomize buttons
        btn_random_selection = wx.Button(self, label='Randomize selected')
        btn_random_selection.Bind(wx.EVT_BUTTON, self.on_random_selection)

        btn_reset = wx.Button(self, label='Reset all defaults')
        btn_reset.Bind(wx.EVT_BUTTON, self.on_reset)

        # add all items to the 4 column grid created earlier
        grid.AddMany([
            chk_midi_channel, self.combobox_midi_channel,
            chk_midi_output_mode, self.combobox_midi_output_mode,
            chk_lower_note, self.combobox_lower_note,
            chk_voicing, self.combobox_voicing,
            chk_upper_note, self.combobox_upper_note,
            chk_note_priority, self.combobox_note_priority,
            chk_portamento, self.combobox_portamento,
            chk_legato, self.combobox_legato,
            chk_pitch_bend_range, self.combobox_pitch_bend_range,
            chk_vibrato_range, self.combobox_vibrato_range,
            chk_transpose, self.combobox_transpose,
            chk_vibrato_speed, self.combobox_vibrato_speed,
            chk_fine_tuning, self.combobox_fine_tuning,
            chk_velocity_scale, self.combobox_velocity_scale,
            chk_tuning_system, self.combobox_tuning_system,
            chk_trigger_duration, self.combobox_trigger_duration,
            chk_tuning_root, self.combobox_tuning_root,
            chk_trigger_shape, self.combobox_trigger_shape,
            chk_arp_gate_length, self.combobox_arp_gate_length,
            chk_osc_shape, self.combobox_osc_shape,
            chk_arp_clock_div, self.combobox_arp_clock_div,
            chk_aux_cv_out, self.combobox_aux_cv_out,
            chk_arp_range, self.combobox_arp_range,
            chk_euclidean_length, self.combobox_euclidean_length,
            chk_arp_direction, self.combobox_arp_direction,
            chk_euclidean_fill, self.combobox_euclidean_fill,
            chk_arp_pattern, self.combobox_arp_pattern,
            chk_euclidean_rotate, self.combobox_euclidean_rotate,
            (0, 0), (0, 0),
            btn_random_selection, btn_reset])

    def on_box_checked(self, event):
        """Called when the checkbox is checked.

        :param event: the wxPython event
        """
        sender = event.GetEventObject()
        is_checked = sender.GetValue()

        if is_checked:
            # add items to a list of currently checked boxes
            self.checkedBoxes.append(sender.GetLabel())
        elif not is_checked:
            # remove items from the list of currently checked boxes
            self.checkedBoxes.remove(sender.GetLabel())

    def on_random_selection(self, event):
        """Randomizes all currently checked boxes.

        :param event: the wxPython event
        """
        for box in self.checkedBoxes:
            if box == 'MIDI channel:':
                self.on_channel_select('random')
            elif box == 'Lower note:':
                self.on_lower_note_select('random')
            elif box == 'Upper note:':
                self.on_upper_note_select('random')
            elif box == 'Portamento:':
                self.on_portamento_select('random')
            elif box == 'Pitch bend range:':
                self.on_pitch_bend_range_select('random')
            elif box == 'Transpose:':
                self.on_transpose_select('random')
            elif box == 'Fine tuning:':
                self.on_fine_tuning_select('random')
            elif box == 'Tuning system:':
                self.on_tuning_system_select('random')
            elif box == 'Tuning root:':
                self.on_tuning_root_select('random')
            elif box == 'Arp/Seq gate length:':
                self.on_arp_gate_length_select('random')
            elif box == 'Arp/Seq clock divider:':
                self.on_arp_clock_divide_select('random')
            elif box == 'Arpeggiator range:':
                self.on_arp_range_select('random')
            elif box == 'Arpeggiator direction:':
                self.on_arp_direction_select('random')
            elif box == 'Arpeggiator pattern:':
                self.on_arp_pattern_select('random')
            elif box == 'MIDI out mode:':
                self.on_midi_output_mode_select('random')
            elif box == 'Voicing:':
                self.on_voicing_select('random')
            elif box == 'Note priority:':
                self.on_note_priority_select('random')
            elif box == 'Legato:':
                self.on_legato_select('random')
            elif box == 'Vibrato range:':
                self.on_vibrato_range_select('random')
            elif box == 'Vibrato speed:':
                self.on_vibrato_speed_select('random')
            elif box == 'Trigger velocity scale:':
                self.on_velocity_scale_select('random')
            elif box == 'Trigger duration:':
                self.on_trigger_duration_select('random')
            elif box == 'Trigger shape:':
                self.on_trigger_shape_select('random')
            elif box == 'Oscillator shape:':
                self.on_osc_shape_select('random')
            elif box == 'Aux CV out:':
                self.on_aux_cv_output_select('random')
            elif box == 'Euclidean length:':
                self.on_euclidean_length_select('random')
            elif box == 'Euclidean fill:':
                self.on_euclidean_fill_select('random')
            elif box == 'Euclidean rotate:':
                self.on_euclidean_rotate_select('random')
            else:
                raise ValueError(
                    'Incorrect value passed to on_random_selection()'
                )

    def on_reset(self, event):
        """Resets all values to defaults.

        :param event: the wxPython event
        """
        self.send_defaults()

    def on_channel_select(self, event):
        """Called when the combobox is checked.

        :param event: the wxPython event
        """
        # get event type
        if event == 'default':
            choice = cc_values.channel['default']
        elif event == 'random':
            choice = random.choice(cc_values.channel.keys())
        else:
            choice = event.GetString()
        # correct combobox value
        self.combobox_midi_channel.SetValue(choice)
        # set controller
        if self.part_number == 1:
            controller = cc_values.controllers['part1_midiChannel']
        elif self.part_number == 2:
            controller = cc_values.controllers['part2_midiChannel']
        elif self.part_number == 3:
            controller = cc_values.controllers['part3_midiChannel']
        elif self.part_number == 4:
            controller = cc_values.controllers['part4_midiChannel']
        else:
            raise ValueError(
                'part_number must be an integer, 1-4'
            )
        # set value
        value = cc_values.channel[choice]
        # send value to midi output
        midiManager.send_cc(controller, value)

    def on_lower_note_select(self, event):
        """Called when the combobox is checked.

        :param event: the wxPython event
        """
        # get event type
        if event == 'default':
            choice = cc_values.note['default low']
        elif event == 'random':
            choice = random.choice(cc_values.note.keys())
        else:
            choice = event.GetString()
        # correct combobox value
        self.combobox_lower_note.SetValue(choice)
        # set controller
        if self.part_number == 1:
            controller = cc_values.controllers['part1_lowerNote']
        elif self.part_number == 2:
            controller = cc_values.controllers['part2_lowerNote']
        elif self.part_number == 3:
            controller = cc_values.controllers['part3_lowerNote']
        elif self.part_number == 4:
            controller = cc_values.controllers['part4_lowerNote']
        else:
            raise ValueError(
                'part_number must be an integer, 1-4'
            )
        # set value
        value = cc_values.note[choice]
        # send value to midi output
        midiManager.send_cc(controller, value)

    def on_upper_note_select(self, event):
        """Called when the combobox is checked.

        :param event: the wxPython event
        """
        # get event type
        if event == 'default':
            choice = cc_values.note['default high']
        elif event == 'random':
            choice = random.choice(cc_values.note.keys())
        else:
            choice = event.GetString()
        # correct combobox value
        self.combobox_upper_note.SetValue(choice)
        # set controller
        if self.part_number == 1:
            controller = cc_values.controllers['part1_upperNote']
        elif self.part_number == 2:
            controller = cc_values.controllers['part2_upperNote']
        elif self.part_number == 3:
            controller = cc_values.controllers['part3_upperNote']
        elif self.part_number == 4:
            controller = cc_values.controllers['part4_upperNote']
        else:
            raise ValueError(
                'part_number must be an integer, 1-4'
            )
        # set value
        value = cc_values.note[choice]
        # send value to midi output
        midiManager.send_cc(controller, value)

    def on_midi_output_mode_select(self, event):
        """Called when the combobox is checked.

        :param event: the wxPython event
        """
        # get event type
        if event == 'default':
            choice = cc_values.midi_output['default']
        elif event == 'random':
            choice = random.choice(cc_values.midi_output.keys())
        else:
            choice = event.GetString()
        # correct combobox value
        self.combobox_midi_output_mode.SetValue(choice)
        # set controller
        if self.part_number == 1:
            controller = cc_values.controllers['part1_midiOutMode']
        elif self.part_number == 2:
            controller = cc_values.controllers['part2_midiOutMode']
        elif self.part_number == 3:
            controller = cc_values.controllers['part3_midiOutMode']
        elif self.part_number == 4:
            controller = cc_values.controllers['part4_midiOutMode']
        else:
            raise ValueError(
                'part_number must be an integer, 1-4'
            )
        # set value
        value = cc_values.midi_output[choice]
        # send value to midi output
        midiManager.send_cc(controller, value)

    def on_voicing_select(self, event):
        """Called when the combobox is checked.

        :param event: the wxPython event
        """
        # get event type
        if event == 'default':
            choice = cc_values.voicing['default']
        elif event == 'random':
            choice = random.choice(cc_values.voicing.keys())
        else:
            choice = event.GetString()
        # correct combobox value
        self.combobox_voicing.SetValue(choice)
        # set controller
        if self.part_number == 1:
            controller = cc_values.controllers['part1_voicing']
        elif self.part_number == 2:
            controller = cc_values.controllers['part2_voicing']
        elif self.part_number == 3:
            controller = cc_values.controllers['part3_voicing']
        elif self.part_number == 4:
            controller = cc_values.controllers['part4_voicing']
        else:
            raise ValueError(
                'part_number must be an integer, 1-4'
            )
        # set value
        value = cc_values.voicing[choice]
        # send value to midi output
        midiManager.send_cc(controller, value)

    def on_note_priority_select(self, event):
        """Called when the combobox is checked.

        :param event: the wxPython event
        """
        # get event type
        if event == 'default':
            choice = cc_values.note_priority['default']
        elif event == 'random':
            choice = random.choice(cc_values.note_priority.keys())
        else:
            choice = event.GetString()
        # correct combobox value
        self.combobox_note_priority.SetValue(choice)
        # set controller
        if self.part_number == 1:
            controller = cc_values.controllers['part1_notePriority']
        elif self.part_number == 2:
            controller = cc_values.controllers['part2_notePriority']
        elif self.part_number == 3:
            controller = cc_values.controllers['part3_notePriority']
        elif self.part_number == 4:
            controller = cc_values.controllers['part4_notePriority']
        else:
            raise ValueError(
                'part_number must be an integer, 1-4'
            )
        # set value
        value = cc_values.note_priority[choice]
        # send value to midi output
        midiManager.send_cc(controller, value)

    def on_portamento_select(self, event):
        """Called when the combobox is checked.

        :param event: the wxPython event
        """
        # get event type
        if event == 'default':
            choice = cc_values.portamento['default']
        elif event == 'random':
            choice = random.choice(cc_values.portamento.keys())
        else:
            choice = event.GetString()
        # correct combobox value
        self.combobox_portamento.SetValue(choice)
        # set controller
        if self.part_number == 1:
            controller = cc_values.controllers['part1_portamento']
        elif self.part_number == 2:
            controller = cc_values.controllers['part2_portamento']
        elif self.part_number == 3:
            controller = cc_values.controllers['part3_portamento']
        elif self.part_number == 4:
            controller = cc_values.controllers['part4_portamento']
        else:
            raise ValueError(
                'part_number must be an integer, 1-4'
            )
        # set value
        value = cc_values.portamento[choice]
        # send value to midi output
        midiManager.send_cc(controller, value)

    def on_legato_select(self, event):
        """Called when the combobox is checked.

        :param event: the wxPython event
        """
        # get event type
        if event == 'default':
            choice = cc_values.boolean['default']
        elif event == 'random':
            choice = random.choice(cc_values.boolean.keys())
        else:
            choice = event.GetString()
        # correct combobox value
        self.combobox_legato.SetValue(choice)
        # set controller
        if self.part_number == 1:
            controller = cc_values.controllers['part1_legato']
        elif self.part_number == 2:
            controller = cc_values.controllers['part2_legato']
        elif self.part_number == 3:
            controller = cc_values.controllers['part3_legato']
        elif self.part_number == 4:
            controller = cc_values.controllers['part4_legato']
        else:
            raise ValueError(
                'part_number must be an integer, 1-4'
            )
        # set value
        value = cc_values.boolean[choice]
        # send value to midi output
        midiManager.send_cc(controller, value)

    def on_pitch_bend_range_select(self, event):
        """Called when the combobox is checked.

        :param event: the wxPython event
        """
        # get event type
        if event == 'default':
            choice = cc_values.pitch_bend['default']
        elif event == 'random':
            choice = random.choice(cc_values.pitch_bend.keys())
        else:
            choice = event.GetString()
        # correct combobox value
        self.combobox_pitch_bend_range.SetValue(choice)
        # set controller
        if self.part_number == 1:
            controller = cc_values.controllers['part1_pitchBendRange']
        elif self.part_number == 2:
            controller = cc_values.controllers['part2_pitchBendRange']
        elif self.part_number == 3:
            controller = cc_values.controllers['part3_pitchBendRange']
        elif self.part_number == 4:
            controller = cc_values.controllers['part4_pitchBendRange']
        else:
            raise ValueError(
                'part_number must be an integer, 1-4'
            )
        # set value
        value = cc_values.pitch_bend[choice]
        # send value to midi output
        midiManager.send_cc(controller, value)

    def on_vibrato_range_select(self, event):
        """Called when the combobox is checked.

        :param event: the wxPython event
        """
        # get event type
        if event == 'default':
            choice = cc_values.vibrato_range['default']
        elif event == 'random':
            choice = random.choice(cc_values.vibrato_range.keys())
        else:
            choice = event.GetString()
        # correct combobox value
        self.combobox_vibrato_range.SetValue(choice)
        # set controller
        if self.part_number == 1:
            controller = cc_values.controllers['part1_vibratoRange']
        elif self.part_number == 2:
            controller = cc_values.controllers['part2_vibratoRange']
        elif self.part_number == 3:
            controller = cc_values.controllers['part3_vibratoRange']
        elif self.part_number == 4:
            controller = cc_values.controllers['part4_vibratoRange']
        else:
            raise ValueError(
                'part_number must be an integer, 1-4'
            )
        # set value
        value = cc_values.vibrato_range[choice]
        # send value to midi output
        midiManager.send_cc(controller, value)

    def on_vibrato_speed_select(self, event):
        """Called when the combobox is checked.

        :param event: the wxPython event
        """
        # get event type
        if event == 'default':
            choice = cc_values.vibrato_speed['default']
        elif event == 'random':
            choice = random.choice(cc_values.vibrato_speed.keys())
        else:
            choice = event.GetString()
        # correct combobox value
        self.combobox_vibrato_speed.SetValue(choice)
        # set controller
        if self.part_number == 1:
            controller = cc_values.controllers['part1_vibratoSpeed']
        elif self.part_number == 2:
            controller = cc_values.controllers['part2_vibratoSpeed']
        elif self.part_number == 3:
            controller = cc_values.controllers['part3_vibratoSpeed']
        elif self.part_number == 4:
            controller = cc_values.controllers['part4_vibratoSpeed']
        else:
            raise ValueError(
                'part_number must be an integer, 1-4'
            )
        # set value
        value = cc_values.vibrato_speed[choice]
        # send value to midi output
        midiManager.send_cc(controller, value)

    def on_transpose_select(self, event):
        """Called when the combobox is checked.

        :param event: the wxPython event
        """
        # get event type
        if event == 'default':
            choice = cc_values.transpose['default']
        elif event == 'random':
            choice = random.choice(cc_values.transpose.keys())
        else:
            choice = event.GetString()
        # correct combobox value
        self.combobox_transpose.SetValue(choice)
        # set controller
        if self.part_number == 1:
            controller = cc_values.controllers['part1_transpose']
        elif self.part_number == 2:
            controller = cc_values.controllers['part2_transpose']
        elif self.part_number == 3:
            controller = cc_values.controllers['part3_transpose']
        elif self.part_number == 4:
            controller = cc_values.controllers['part4_transpose']
        else:
            raise ValueError(
                'part_number must be an integer, 1-4'
            )
        # set value
        value = cc_values.transpose[choice]
        # send value to midi output
        midiManager.send_cc(controller, value)

    def on_fine_tuning_select(self, event):
        """Called when the combobox is checked.

        :param event: the wxPython event
        """
        # get event type
        if event == 'default':
            choice = cc_values.fine_tuning['default']
        elif event == 'random':
            choice = random.choice(cc_values.fine_tuning.keys())
        else:
            choice = event.GetString()
        # correct combobox value
        self.combobox_fine_tuning.SetValue(choice)
        # set controller
        if self.part_number == 1:
            controller = cc_values.controllers['part1_fineTuning']
        elif self.part_number == 2:
            controller = cc_values.controllers['part2_fineTuning']
        elif self.part_number == 3:
            controller = cc_values.controllers['part3_fineTuning']
        elif self.part_number == 4:
            controller = cc_values.controllers['part4_fineTuning']
        else:
            raise ValueError(
                'part_number must be an integer, 1-4'
            )
        # set value
        value = cc_values.fine_tuning[choice]
        # send value to midi output
        midiManager.send_cc(controller, value)

    def on_tuning_root_select(self, event):
        """Called when the combobox is checked.

        :param event: the wxPython event
        """
        # get event type
        if event == 'default':
            choice = cc_values.tuning_root['default']
        elif event == 'random':
            choice = random.choice(cc_values.tuning_root.keys())
        else:
            choice = event.GetString()
        # correct combobox value
        self.combobox_tuning_root.SetValue(choice)
        # set controller
        if self.part_number == 1:
            controller = cc_values.controllers['part1_tuningRoot']
        elif self.part_number == 2:
            controller = cc_values.controllers['part2_tuningRoot']
        elif self.part_number == 3:
            controller = cc_values.controllers['part3_tuningRoot']
        elif self.part_number == 4:
            controller = cc_values.controllers['part4_tuningRoot']
        else:
            raise ValueError(
                'part_number must be an integer, 1-4'
            )
        # set value
        value = cc_values.tuning_root[choice]
        # send value to midi output
        midiManager.send_cc(controller, value)

    def on_tuning_system_select(self, event):
        """Called when the combobox is checked.

        :param event: the wxPython event
        """
        # get event type
        if event == 'default':
            choice = cc_values.tuning_system['default']
        elif event == 'random':
            choice = random.choice(cc_values.tuning_system.keys())
        else:
            choice = event.GetString()
        # correct combobox value
        self.combobox_tuning_system.SetValue(choice)
        # set controller
        if self.part_number == 1:
            controller = cc_values.controllers['part1_tuningSystem']
        elif self.part_number == 2:
            controller = cc_values.controllers['part2_tuningSystem']
        elif self.part_number == 3:
            controller = cc_values.controllers['part3_tuningSystem']
        elif self.part_number == 4:
            controller = cc_values.controllers['part4_tuningSystem']
        else:
            raise ValueError(
                'part_number must be an integer, 1-4'
            )
        # set value
        value = cc_values.tuning_system[choice]
        # send value to midi output
        midiManager.send_cc(controller, value)

    def on_trigger_duration_select(self, event):
        """Called when the combobox is checked.

        :param event: the wxPython event
        """
        # get event type
        if event == 'default':
            choice = cc_values.trigger_duration['default']
        elif event == 'random':
            choice = random.choice(cc_values.trigger_duration.keys())
        else:
            choice = event.GetString()
        # correct combobox value
        self.combobox_trigger_duration.SetValue(choice)
        # set controller
        if self.part_number == 1:
            controller = cc_values.controllers['part1_triggerDuration']
        elif self.part_number == 2:
            controller = cc_values.controllers['part2_triggerDuration']
        elif self.part_number == 3:
            controller = cc_values.controllers['part3_triggerDuration']
        elif self.part_number == 4:
            controller = cc_values.controllers['part4_triggerDuration']
        else:
            raise ValueError(
                'part_number must be an integer, 1-4'
            )
        # set value
        value = cc_values.trigger_duration[choice]
        # send value to midi output
        midiManager.send_cc(controller, value)

    def on_velocity_scale_select(self, event):
        """Called when the combobox is checked.

        :param event: the wxPython event
        """
        # get event type
        if event == 'default':
            choice = cc_values.boolean['default']
        elif event == 'random':
            choice = random.choice(cc_values.boolean.keys())
        else:
            choice = event.GetString()
        # correct combobox value
        self.combobox_velocity_scale.SetValue(choice)
        # set controller
        if self.part_number == 1:
            controller = cc_values.controllers['part1_velocityScale']
        elif self.part_number == 2:
            controller = cc_values.controllers['part2_velocityScale']
        elif self.part_number == 3:
            controller = cc_values.controllers['part3_velocityScale']
        elif self.part_number == 4:
            controller = cc_values.controllers['part4_velocityScale']
        else:
            raise ValueError(
                'part_number must be an integer, 1-4'
            )
        # set value
        value = cc_values.boolean[choice]
        # send value to midi output
        midiManager.send_cc(controller, value)

    def on_trigger_shape_select(self, event):
        """Called when the combobox is checked.

        :param event: the wxPython event
        """
        # get event type
        if event == 'default':
            choice = cc_values.trigger_shape['default']
        elif event == 'random':
            choice = random.choice(cc_values.trigger_shape.keys())
        else:
            choice = event.GetString()
        # correct combobox value
        self.combobox_trigger_shape.SetValue(choice)
        # set controller
        if self.part_number == 1:
            controller = cc_values.controllers['part1_triggerShape']
        elif self.part_number == 2:
            controller = cc_values.controllers['part2_triggerShape']
        elif self.part_number == 3:
            controller = cc_values.controllers['part3_triggerShape']
        elif self.part_number == 4:
            controller = cc_values.controllers['part4_triggerShape']
        else:
            raise ValueError(
                'part_number must be an integer, 1-4'
            )
        # set value
        value = cc_values.trigger_shape[choice]
        # send value to midi output
        midiManager.send_cc(controller, value)

    def on_aux_cv_output_select(self, event):
        """Called when the combobox is checked.

        :param event: the wxPython event
        """
        # get event type
        if event == 'default':
            choice = cc_values.aux_cv['default']
        elif event == 'random':
            choice = random.choice(cc_values.aux_cv.keys())
        else:
            choice = event.GetString()
        # correct combobox value
        self.combobox_aux_cv_out.SetValue(choice)
        # set controller
        if self.part_number == 1:
            controller = cc_values.controllers['part1_auxCVout']
        elif self.part_number == 2:
            controller = cc_values.controllers['part2_auxCVout']
        elif self.part_number == 3:
            controller = cc_values.controllers['part3_auxCVout']
        elif self.part_number == 4:
            controller = cc_values.controllers['part4_auxCVout']
        else:
            raise ValueError(
                'part_number must be an integer, 1-4'
            )
        # set value
        value = cc_values.aux_cv[choice]
        # send value to midi output
        midiManager.send_cc(controller, value)

    def on_osc_shape_select(self, event):
        """Called when the combobox is checked.

        :param event: the wxPython event
        """
        # get event type
        if event == 'default':
            choice = cc_values.oscillator['default']
        elif event == 'random':
            choice = random.choice(cc_values.oscillator.keys())
        else:
            choice = event.GetString()
        # correct combobox value
        self.combobox_osc_shape.SetValue(choice)
        # set controller
        if self.part_number == 1:
            controller = cc_values.controllers['part1_oscillatorShape']
        elif self.part_number == 2:
            controller = cc_values.controllers['part2_oscillatorShape']
        elif self.part_number == 3:
            controller = cc_values.controllers['part3_oscillatorShape']
        elif self.part_number == 4:
            controller = cc_values.controllers['part4_oscillatorShape']
        else:
            raise ValueError(
                'part_number must be an integer, 1-4'
            )
        # set value
        value = cc_values.oscillator[choice]
        # send value to midi output
        midiManager.send_cc(controller, value)

    def on_arp_clock_divide_select(self, event):
        """Called when the combobox is checked.

        :param event: the wxPython event
        """
        # get event type
        if event == 'default':
            choice = cc_values.arp_clock_division['default']
        elif event == 'random':
            choice = random.choice(cc_values.arp_clock_division.keys())
        else:
            choice = event.GetString()
        # correct combobox value
        self.combobox_arp_clock_div.SetValue(choice)
        # set controller
        if self.part_number == 1:
            controller = cc_values.controllers['part1_arpClockDiv']
        elif self.part_number == 2:
            controller = cc_values.controllers['part2_arpClockDiv']
        elif self.part_number == 3:
            controller = cc_values.controllers['part3_arpClockDiv']
        elif self.part_number == 4:
            controller = cc_values.controllers['part4_arpClockDiv']
        else:
            raise ValueError(
                'part_number must be an integer, 1-4'
            )
        # set value
        value = cc_values.arp_clock_division[choice]
        # send value to midi output
        midiManager.send_cc(controller, value)

    def on_arp_gate_length_select(self, event):
        """Called when the combobox is checked.

        :param event: the wxPython event
        """
        # get event type
        if event == 'default':
            choice = cc_values.arp_gate_length['default']
        elif event == 'random':
            choice = random.choice(cc_values.arp_gate_length.keys())
        else:
            choice = event.GetString()
        # correct combobox value
        self.combobox_arp_gate_length.SetValue(choice)
        # set controller
        if self.part_number == 1:
            controller = cc_values.controllers['part1_arpGateLength']
        elif self.part_number == 2:
            controller = cc_values.controllers['part2_arpGateLength']
        elif self.part_number == 3:
            controller = cc_values.controllers['part3_arpGateLength']
        elif self.part_number == 4:
            controller = cc_values.controllers['part4_arpGateLength']
        else:
            raise ValueError(
                'part_number must be an integer, 1-4'
            )
        # set value
        value = cc_values.arp_gate_length[choice]
        # send value to midi output
        midiManager.send_cc(controller, value)

    def on_arp_range_select(self, event):
        """Called when the combobox is checked.

        :param event: the wxPython event
        """
        # get event type
        if event == 'default':
            choice = cc_values.arp_range['default']
        elif event == 'random':
            choice = random.choice(cc_values.arp_range.keys())
        else:
            choice = event.GetString()
        # correct combobox value
        self.combobox_arp_range.SetValue(choice)
        # set controller
        if self.part_number == 1:
            controller = cc_values.controllers['part1_arpRange']
        elif self.part_number == 2:
            controller = cc_values.controllers['part2_arpRange']
        elif self.part_number == 3:
            controller = cc_values.controllers['part3_arpRange']
        elif self.part_number == 4:
            controller = cc_values.controllers['part4_arpRange']
        else:
            raise ValueError(
                'part_number must be an integer, 1-4'
            )
        # set value
        value = cc_values.arp_range[choice]
        # send value to midi output
        midiManager.send_cc(controller, value)

    def on_arp_direction_select(self, event):
        """Called when the combobox is checked.

        :param event: the wxPython event
        """
        # get event type
        if event == 'default':
            choice = cc_values.arp_direction['default']
        elif event == 'random':
            choice = random.choice(cc_values.arp_direction.keys())
        else:
            choice = event.GetString()
        # correct combobox value
        self.combobox_arp_direction.SetValue(choice)
        # set controller
        if self.part_number == 1:
            controller = cc_values.controllers['part1_arpDirection']
        elif self.part_number == 2:
            controller = cc_values.controllers['part2_arpDirection']
        elif self.part_number == 3:
            controller = cc_values.controllers['part3_arpDirection']
        elif self.part_number == 4:
            controller = cc_values.controllers['part4_arpDirection']
        else:
            raise ValueError(
                'part_number must be an integer, 1-4'
            )
        # set value
        value = cc_values.arp_direction[choice]
        # send value to midi output
        midiManager.send_cc(controller, value)

    def on_arp_pattern_select(self, event):
        """Called when the combobox is checked.

        :param event: the wxPython event
        """
        # get event type
        if event == 'default':
            choice = cc_values.arp_pattern['default']
        elif event == 'random':
            choice = random.choice(cc_values.arp_pattern.keys())
        else:
            choice = event.GetString()
        # correct combobox value
        self.combobox_arp_pattern.SetValue(choice)
        # set controller
        if self.part_number == 1:
            controller = cc_values.controllers['part1_arpPattern']
        elif self.part_number == 2:
            controller = cc_values.controllers['part2_arpPattern']
        elif self.part_number == 3:
            controller = cc_values.controllers['part3_arpPattern']
        elif self.part_number == 4:
            controller = cc_values.controllers['part4_arpPattern']
        else:
            raise ValueError(
                'part_number must be an integer, 1-4'
            )
        # set value
        value = cc_values.arp_pattern[choice]
        # send value to midi output
        midiManager.send_cc(controller, value)

    def on_euclidean_length_select(self, event):
        """Called when the combobox is checked.

        :param event: the wxPython event
        """
        # get event type
        if event == 'default':
            choice = cc_values.euclidean['default']
        elif event == 'random':
            choice = random.choice(cc_values.euclidean.keys())
        else:
            choice = event.GetString()
        # correct combobox value
        self.combobox_euclidean_length.SetValue(choice)
        # set controller
        if self.part_number == 1:
            controller = cc_values.controllers['part1_euclideanLength']
        elif self.part_number == 2:
            controller = cc_values.controllers['part2_euclideanLength']
        elif self.part_number == 3:
            controller = cc_values.controllers['part3_euclideanLength']
        elif self.part_number == 4:
            controller = cc_values.controllers['part4_euclideanLength']
        else:
            raise ValueError(
                'part_number must be an integer, 1-4'
            )
        # set value
        value = cc_values.euclidean[choice]
        # send value to midi output
        midiManager.send_cc(controller, value)

    def on_euclidean_fill_select(self, event):
        """Called when the combobox is checked.

        :param event: the wxPython event
        """
        # get event type
        if event == 'default':
            choice = cc_values.euclidean['default']
        elif event == 'random':
            choice = random.choice(cc_values.euclidean.keys())
        else:
            choice = event.GetString()
        # correct combobox value
        self.combobox_euclidean_fill.SetValue(choice)
        # set controller
        if self.part_number == 1:
            controller = cc_values.controllers['part1_euclideanFill']
        elif self.part_number == 2:
            controller = cc_values.controllers['part2_euclideanFill']
        elif self.part_number == 3:
            controller = cc_values.controllers['part3_euclideanFill']
        elif self.part_number == 4:
            controller = cc_values.controllers['part4_euclideanFill']
        else:
            raise ValueError(
                'part_number must be an integer, 1-4'
            )
        # set value
        value = cc_values.euclidean[choice]
        # send value to midi output
        midiManager.send_cc(controller, value)

    def on_euclidean_rotate_select(self, event):
        """Called when the combobox is checked.

        :param event: the wxPython event
        """
        # get event type
        if event == 'default':
            choice = cc_values.euclidean['default']
        elif event == 'random':
            choice = random.choice(cc_values.euclidean.keys())
        else:
            choice = event.GetString()
        # correct combobox value
        self.combobox_euclidean_rotate.SetValue(choice)
        # set controller
        if self.part_number == 1:
            controller = cc_values.controllers['part1_euclideanRotate']
        elif self.part_number == 2:
            controller = cc_values.controllers['part2_euclideanRotate']
        elif self.part_number == 3:
            controller = cc_values.controllers['part3_euclideanRotate']
        elif self.part_number == 4:
            controller = cc_values.controllers['part4_euclideanRotate']
        else:
            raise ValueError(
                'part_number must be an integer, 1-4'
            )
        # set value
        value = cc_values.euclidean[choice]
        # send value to midi output
        midiManager.send_cc(controller, value)

    def send_defaults(self):
        """Initialises yarns with some default settings. """
        self.on_vibrato_range_select('default')
        self.on_vibrato_speed_select('default')
        self.on_pitch_bend_range_select('default')
        self.on_transpose_select('default')
        self.on_fine_tuning_select('default')
        self.on_trigger_duration_select('default')
        self.on_arp_range_select('default')
        self.on_arp_pattern_select('default')
        self.on_arp_gate_length_select('default')
        self.on_euclidean_length_select('default')
        self.on_euclidean_fill_select('default')
        self.on_euclidean_rotate_select('default')
        self.on_portamento_select('default')
        self.on_channel_select('default')
        self.on_lower_note_select('default')
        self.on_upper_note_select('default')
        self.on_midi_output_mode_select('default')
        self.on_voicing_select('default')
        self.on_note_priority_select('default')
        self.on_legato_select('default')
        self.on_tuning_root_select('default')
        self.on_tuning_system_select('default')
        self.on_velocity_scale_select('default')
        self.on_trigger_shape_select('default')
        self.on_aux_cv_output_select('default')
        self.on_osc_shape_select('default')
        self.on_arp_clock_divide_select('default')
        self.on_arp_direction_select('default')


class EditorSettings(wx.Panel):
    """The editor's configuration page. """

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)

        # rows, columns, vertical gap, horizontal gap
        grid = wx.FlexGridSizer(28, 2, 8, 16)

        # column, proportion
        grid.AddGrowableCol(0, 1)
        grid.AddGrowableCol(1, 1)

        # midi input devices
        txt_midi_in = wx.StaticText(self, label='MIDI Input Device:')
        listbox_midi_in = wx.ListBox(self)
        listbox_midi_in.Bind(wx.EVT_LISTBOX, self.on_input_click)
        listbox_midi_in.SetMinSize((0, 200))

        # midi output devices
        txt_midi_out = wx.StaticText(self, label='MIDI Output Device:')
        listbox_midi_out = wx.ListBox(self)
        listbox_midi_out.Bind(wx.EVT_LISTBOX, self.on_output_click)
        listbox_midi_in.SetMinSize((0, 200))

        # remote control channel
        txt_channel = wx.StaticText(self, label='MIDI RC Channel:')
        spin_channel = wx.SpinCtrl(
            self, value=cc_values.channel['default remote']
        )
        spin_channel.Bind(wx.EVT_SPINCTRL, self.on_remote_channel_select)
        spin_channel.SetRange(1, 16)

        # notes
        txt_notes = wx.StaticText(
            self,
            label='Set MIDI channel to match Yarns RC channel.\n' +
            'Restart program to refresh attached devices.\n' +
            'This program only supports firmware %s' % firmware
        )

        # select button
        self.btn_confirm = wx.Button(self, label='Confirm Settings')
        self.btn_confirm.Bind(wx.EVT_BUTTON, self.on_confirm)

        # add it all to the grid sizer
        grid.AddMany([
            txt_midi_in, txt_midi_out,
            (listbox_midi_in, 1, wx.EXPAND), (listbox_midi_out, 1, wx.EXPAND),
            txt_channel, (wx.StaticText(self, label='')),
            spin_channel, (wx.StaticText(self, label=''))])

        # add grid sizer to sizer
        self.sizer.Add(grid, 1, wx.EXPAND)
        self.sizer.Add(txt_notes, 0, wx.EXPAND)
        self.sizer.Add(self.btn_confirm, 0, wx.ALIGN_RIGHT)

        # init midi
        midiManager.init_midi()

        # populate MIDI information
        for midi_device in midiManager.list_midi_devices('input'):
            listbox_midi_in.Append(midi_device)

        for midi_device in midiManager.list_midi_devices('output'):
            listbox_midi_out.Append(midi_device)

    def on_remote_channel_select(self, event):
        """Selects the RC midi channel.

        :param event: the wxPython event
        """
        choice = event.GetInt()
        midiManager.set_channel(choice)

    def on_confirm(self, event):
        """Locks the midi output/channel choice for the session.

        :param event: the wxPython event
        """
        # midi output device is required
        if midiManager.midi_output_port is None:
            error_message = wx.MessageDialog(
                None,
                'You must select a MIDI output device!',
                'Error',
                wx.OK | wx.ICON_ERROR
            )
            error_message.ShowModal()
        else:
            self.parent.on_confirm()  # parent function handles this

    def on_input_click(self, event):
        """Called when the user clicks a midi input device.

        :param event: the wxPython event
        """
        midiManager.set_midi_input(event.GetString())

    def on_output_click(self, event):
        """Called when the user clicks a midi output device.

        :param event: the wxPython event
        """
        midiManager.set_midi_output(event.GetString())


class Editor(wx.Notebook):
    """All the panels put together in a "notebook" style (with tabs.) """

    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, id=wx.ID_ANY, style=wx.BK_TOP)

        # Create the tabs and add them to the notebook
        self.page_editor = EditorSettings(self)
        self.AddPage(self.page_editor, 'Editor')

    def on_confirm(self):
        """Confirms midi device selection. """

        # close/re open midi ports
        midiManager.close_midi()
        midiManager.open_midi()

        # add layout panel and switch to it
        self.on_part_change(0)
        self.ChangeSelection(1)

    def kill_page(self, page_text):
        """Removes a notebook page based on its page label.

        :param page_text: the page label to kill
        """
        for index in range(self.GetPageCount()):
            if self.GetPageText(index) == page_text:
                self.DeletePage(index)
                self.SendSizeEvent()
                break

    def on_part_change(self, number_of_parts):
        """Enables/disables tabs as layouts are changed.

        :param number_of_parts: number of pages that should remain
        """
        if number_of_parts == 0:
            # add the layout panel if it doesn't exist
            if self.GetPageCount() == 1:
                page_layout = LayoutSettings(self)
                self.AddPage(page_layout, 'Layout')
                page_layout.send_defaults()

        elif number_of_parts == 1:
            # remove parts 2, 3, and 4 if they exist
            self.kill_page('Part 2')
            self.kill_page('Part 3')
            self.kill_page('Part 4')
            # add page 1 if it doesn't exist
            if self.GetPageCount() == 2:
                page_part1 = PartSettings(self, 1)
                self.AddPage(page_part1, 'Part 1')
                page_part1.send_defaults()

        elif number_of_parts == 2:
            # remove parts 3 and 4 if they exist
            self.kill_page('Part 3')
            self.kill_page('Part 4')
            # add page 2 if it doesn't exist
            if self.GetPageCount() == 3:
                page_part2 = PartSettings(self, 2)
                self.AddPage(page_part2, 'Part 2')
                page_part2.send_defaults()

        elif number_of_parts == 4:
            if self.GetPageCount() == 4:
                # add parts 3 and 4 if they don't exist
                page_part3 = PartSettings(self, 3)
                page_part4 = PartSettings(self, 4)
                self.AddPage(page_part3, 'Part 3')
                self.AddPage(page_part4, 'Part 4')
                page_part3.send_defaults()
                page_part4.send_defaults()
            elif self.GetPageCount() == 3:
                # add parts 2, 3, and 4 if they don't exist
                page_part2 = PartSettings(self, 2)
                page_part3 = PartSettings(self, 3)
                page_part4 = PartSettings(self, 4)
                self.AddPage(page_part2, 'Part 2')
                self.AddPage(page_part3, 'Part 3')
                self.AddPage(page_part4, 'Part 4')
                page_part2.send_defaults()
                page_part3.send_defaults()
                page_part4.send_defaults()
        else:
            raise ValueError(
                'Incorrect value passed to Editor.on_part_change()'
            )


class Window(wx.Frame):
    """The application window. """

    def __init__(self):
        wx.Frame.__init__(self,
                          parent=None,
                          title='Yarns Editor',
                          style=wx.DEFAULT_FRAME_STYLE)

        # platform specific tweaks
        os = platform.system().lower()
        if os == 'windows':
            application_id = 'Yarns Editor'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                application_id
            )
            window_x_size = 600
            window_y_size = 560
        elif os == 'darwin':
            window_x_size = 690
            window_y_size = 570
        elif os == 'linux':
            window_x_size = 740
            window_y_size = 570
        else:
            window_x_size = 600
            window_y_size = 560

        # TODO(notinachos): dynamically set correct sizes
        self.SetSize((window_x_size, window_y_size))
        self.SetMinSize((window_x_size, window_y_size))
        self.SetIcon(images.icon.GetIcon())
        self.Bind(wx.EVT_CLOSE, self.on_quit)
        self.init_menu_bar()
        self.init_gui()

    def init_gui(self):
        """Creates the window elements. """
        panel = wx.Panel(self)
        notebook = Editor(panel)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.EXPAND)
        sizer.Layout()  # causes black box glitch if omitted
        panel.SetSizer(sizer)
        self.Layout()
        self.Centre()
        self.Show()

    def init_menu_bar(self):
        """Creates the menu_bar contents. """
        # create menu_bar
        menu_bar = wx.MenuBar()

        # file menu
        file_menu = wx.Menu()
        file_menu_quit = file_menu.Append(wx.ID_EXIT, '&Quit Yarns Editor')
        self.Bind(wx.EVT_MENU, self.on_quit, id=wx.ID_EXIT)

        # help menu
        help_menu = wx.Menu()
        help_menu_about = help_menu.Append(wx.ID_ABOUT, '&About Yarns Editor')
        self.Bind(wx.EVT_MENU, self.on_about, id=wx.ID_ABOUT)

        # add items to menu_bar
        menu_bar.Append(file_menu, '&File')
        menu_bar.Append(help_menu, '&Help')
        self.SetMenuBar(menu_bar)

    def on_quit(self, event):
        """Called when the user quits.

        :param event: the wxPython event
        """
        midiManager.close_midi()
        self.Destroy()

    def on_about(self, event):
        """Called when the user chooses "About" from the help menu.

        :param event: the wxPython event
        """
        info = wx.AboutDialogInfo()
        info.SetIcon(images.icon.GetIcon())
        info.Name = 'Yarns Editor'
        info.Version = '0.9.1'
        info.Copyright = '(C) 2015 Panagiotis Peppas'
        info.License = 'The MIT License. See source code for full license.'
        info.Description = 'A MIDI editor for Mutable Instruments Yarns.'
        info.WebSite = (
            'https://github.com/notinachos/yarns-editor',
            'Source code on Github'
        )
        wx.AboutBox(info)


if __name__ == '__main__':
    global midiManager

    # handles midi events
    midiManager = MidiManager()
    midiManager.set_channel(cc_values.channel['default remote'])

    # the wx app
    app = wx.App()
    frame = Window()
    app.MainLoop()
    sys.exit(0)
