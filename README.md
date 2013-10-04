LilyFrog
========

LilyFrog allows you faster note entering in the [LilyPond](http://lilypond.org) text editor of your choice, e.g. Frescobaldi. What you need is a MIDI master keyboard and an usual USB numeric keypad. The keypad is required to easy control temporal parameters like note duration, note accidental and so on. By pressing a key on the MIDI keyboard, the resulting LilyPond snippet will be generated and virtually typed on the PC. Summarized, the LilyFrog types notes that you are playing, which is an intuitive and fast method to enter LilyPond music scores.

Requirements and limitations
----------------------------

LilyFrog is written in Python and requires following libraries to be installed:

 * [pyqt4](http://www.riverbankcomputing.co.uk/software/pyqt/intro)
 * [rtmidi](http://github.com/superquadratic/rtmidi-python)
 * [evdev](http://github.com/gvalkov/python-evdev)

Because of specific keypad handling, it runs only on Linux (at the moment) and only with superuser privileges. Currently the [Delock 12371](http://www.google.com/?q=site:delock.de+12371) USB keypad was successfully tested. However, a random MIDI master keyboard can be connected via QjackCtl. 

Setup instructions
------------------

 1. Install PyQt4 from your Linux distribution repository. Download two remaining libraries and run `sudo python setup.py install` respectively.
 2. Find out the keypad vendor and product number by executing `lsusb`. You may run this command twice, before and after connecting the keypad to quickly find the right entry. Insert both numbers into the `Keypad.py` file.
 3. Start QjackCtl and plug in the MIDI keyboard. Connect the MIDI keyboard output to *MIDI through* input or optionally to *RtMidi client* input after the next step.
 4. Execute the `lilyfrog` command. You'll be prompted to enter the superuser password.
 5. Optionally adjust keyboard key combinations and note names in the `Mappings.py` file depending on your needs.

Keypad shortcuts
----------------

To activate LilyFrog press the `NumLock` button. If the keypad has a LED indicator, it should get on.

There are two kinds of keypad shortcuts: passive and active. Passive shortcuts produces no output itself, they only changes the temporal note or rest state until a MIDI key or the rest shortcut is pressed. With passive shortcuts you can control the duration, accidental and relative octave of the note/rest. After entering a note/rest the temporal state will be automatically reset. Press a passive shortcut twice to undo the state change. Active keypad shortcuts don't reset any temporal state, but they produces an output.

Note/rest duration:

 * `1`: 64th
 * `2`: 32nd
 * `3`: 16th
 * `4`: Eighth
 * `5`: Quarter
 * `6`: Half
 * `7`: Whole
 * `8`: Breve
 * `9`: Longa
 * `.`: Dot

Note accidental:

 * '/': Flat
 * '*': Sharp

A temporal accidental is not restricted to the black keys only. It is also possible to produce notes like `eis` by pressing '*' on the keypad and 'f' on the MIDI keyboard respectively.

Relative octave mark:

 * '-': Down
 * '+': Up

Common active keys:

 * '0': Inserts a rest `r` instead of note
 * 'Enter': Inserts a bar check `|` and a line break

Special active keys (depending on keypad manufacturer):

 * 'Backspace': Deletes the last typed character
 * 'Space': Inserts a tie `~`
