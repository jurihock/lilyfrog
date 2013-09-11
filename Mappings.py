from evdev.ecodes import *

KeyChrToCodeMap = \
{
    # Note names
    'c':  [KEY_C],
    'd':  [KEY_D],
    'e':  [KEY_E],
    'f':  [KEY_F],
    'g':  [KEY_G],
    'a':  [KEY_A],
    'b':  [KEY_B],
    'i':  [KEY_I],
    's':  [KEY_S],

    # Octave marks
    ',':  [KEY_COMMA],
    '\'': [KEY_APOSTROPHE, KEY_SPACE], # consider the dead key

    # Note durations
    '\\': [KEY_BACKSLASH],
    'l':  [KEY_L],
    'o':  [KEY_O],
    'n':  [KEY_N],
    'v':  [KEY_V],
    '1':  [KEY_1],
    '2':  [KEY_2],
    '3':  [KEY_3],
    '4':  [KEY_4],
    '6':  [KEY_6],
    '8':  [KEY_8],
    '.':  [KEY_DOT],

    # Misc
    'r':  [KEY_R],
    '~':  [[KEY_GRAVE], KEY_SPACE], # consider the dead key
    '|':  [[KEY_BACKSLASH]],
    '\b': [KEY_BACKSPACE],
    '\n': [KEY_ENTER],
    ' ':  [KEY_SPACE]
}

NoteNumToStrMap = \
{
        'DefaultFlat':
        {
                0:  'c',
                1:  'des',
                2:  'd',
                3:  'es',
                4:  'e',
                5:  'f',
                6:  'ges',
                7:  'g',
                8:  'as',
                9:  'a',
                10: 'bes',
                11: 'b'
        },
        'DefaultSharp':
        {
                0:  'c',
                1:  'cis',
                2:  'd',
                3:  'dis',
                4:  'e',
                5:  'f',
                6:  'fis',
                7:  'g',
                8:  'gis',
                9:  'a',
                10: 'ais',
                11: 'b'
        },
        'TemporalFlat':
        {
                0:  'c',
                1:  'des',
                2:  'd',
                3:  'es',
                4:  'fes',
                5:  'f',
                6:  'ges',
                7:  'g',
                8:  'as',
                9:  'a',
                10: 'bes',
                11: 'ces'
        },
        'TemporalSharp':
        {
                0:  'bis',
                1:  'cis',
                2:  'd',
                3:  'dis',
                4:  'e',
                5:  'eis',
                6:  'fis',
                7:  'g',
                8:  'gis',
                9:  'a',
                10: 'ais',
                11: 'b'
        }
}