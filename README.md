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
