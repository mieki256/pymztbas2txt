#!python
# -*- coding: utf-8 -*-
# -*- mode: python; Encoding: utf-8; coding: utf-8 -*-
# Last updated: <2019/05/21 09:02:49 +0900>
"""
Convert SP-5030/S-BASIC/Hu-BASIC program to text.

* Windows10 1809 x64 + Python 2.7.16 32bit
* Author : mieki256
* License : CC0 / Public Domain

Ver. 1.1 fix : Fix error when redirect.
Ver. 1.0 first commit.
"""

import struct
import argparse
import sys

ID_SP5030 = 0
ID_SBASIC = 1
ID_HUBASIC = 2

jp_flag = False
target_id = ID_SP5030

# SP-5030 command list
sp5030_command_list = {
    0x80: "REM",
    0x81: "DATA",
    0x82: "LIST",
    0x83: "RUN",
    0x84: "NEW",
    0x85: "PRINT",
    0x86: "LET",
    0x87: "FOR",
    0x88: "IF",
    0x89: "GOTO",
    0x8A: "READ",
    0x8B: "GOSUB",
    0x8C: "RETURN",
    0x8D: "NEXT",
    0x8E: "STOP",
    0x8F: "END",
    0x90: "ON",
    0x91: "LOAD",
    0x92: "SAVE",
    0x93: "VERIFY",
    0x94: "POKE",
    0x95: "DIM",
    0x96: "DEF FN",
    0x97: "INPUT",
    0x98: "RESTORE",
    0x99: "CLR",
    0x9A: "MUSIC",
    0x9B: "TEMPO",
    0x9C: "USR(",
    0x9D: "WOPEN",
    0x9E: "ROPEN",
    0x9F: "CLOSE",
    0xA0: "BYE",
    0xA1: "LIMIT",
    0xA2: "CONT",
    0xA3: "SET",
    0xA4: "RESET",
    0xA5: "GET",
    0xA6: "INP#",
    0xA7: "OUT#",
    0xA8: "*(0F2H)",
    # 0xA9: None,
    # 0xAA: None,
    # 0xAB: None,
    # 0xAC: None,
    0xAD: "THEN",
    0xAE: "TO",
    0xAF: "STEP",
    0xB0: "><",
    0xB1: "<>",
    0xB2: "=<",
    0xB3: "<=",
    0xB4: "=>",
    0xB5: ">=",
    0xB6: "=",
    0xB7: ">",
    0xB8: "<",
    0xB9: "AND",  # syntax error
    0xBA: "OR",   # syntax error
    0xBB: "NOT",  # syntax error
    0xBC: "+",
    0xBD: "-",
    0xBE: "*",
    0xBF: "/",
    0xC0: "LEFT$(",
    0xC1: "RIGHT$(",
    0xC2: "MID$(",
    0xC3: "LEN(",
    0xC4: "CHR$(",
    0xC5: "STR$",
    0xC6: "ASC(",
    0xC7: "VAL(",
    0xC8: "PEEK(",
    0xC9: "TAB(",
    0xCA: "SPC(",
    0xCB: "SIZE",
    # 0xCC: None,
    # 0xCD: None,
    # 0xCE: None,
    0xCF: "^",
    0xD0: "RND(",
    0xD1: "SIN(",
    0xD2: "COS(",
    0xD3: "TAN(",
    0xD4: "ATN(",
    0xD5: "EXP(",
    0xD6: "INT(",
    0xD7: "LOG(",
    0xD8: "LN(",
    0xD9: "ABS(",
    0xDA: "SGN(",
    0xDB: "SQR(",
    # 0xDC: None,
    # ...
    # 0xF1: None,
    0xF2: "CURSOR",
    # 0xF3: None,
    # ...
    # 0xFF: None,
}

# S-BASIC command list (0x80-0xFD)
sbasic_command_list_a = {
    0x80: "GOTO",
    0x81: "GOSUB",
    # 0x82: None,
    0x83: "RUN",
    0x84: "RETURN",
    0x85: "RESTORE",
    0x86: "RESUME",
    0x87: "LIST",
    # 0x88: None,
    0x89: "DELETE",
    0x8A: "RENUM",
    0x8B: "AUTO",
    # 0x8C: None,
    0x8D: "FOR",
    0x8E: "NEXT",
    0x8F: "PRINT",
    # 0x90: None,
    0x91: "INPUT",
    # 0x92: None,
    0x93: "IF",
    0x94: "DATA",
    0x95: "READ",
    0x96: "DIM",
    0x97: "REM",
    0x98: "END",
    0x99: "STOP",
    0x9A: "CONT",
    0x9B: "CLS",
    # 0x9C: None,
    0x9D: "ON",
    0x9E: "LET",
    0x9F: "NEW",
    0xA0: "POKE",
    0xA1: "OFF",
    0xA2: "MODE",
    0xA3: "SKIP",
    0xA4: "PLOT",
    0xA5: "LINE",
    0xA6: "RLINE",
    0xA7: "MOVE",
    0xA8: "RMOVE",
    0xA9: "TRON",
    0xAA: "TROFF",
    0xAB: "INP#",
    # 0xAC: None,
    0xAD: "GET",
    0xAE: "PCOLOR",
    0xAF: "PHOME",
    0xB0: "HSET",
    0xB1: "GPRINT",
    0xB2: "KEY",
    0xB3: "AXIS",
    0xB4: "LOAD",
    0xB5: "SAVE",
    0xB6: "MERGE",
    # 0xB7: None,
    0xB8: "CONSOLE",
    # 0xB9: None,
    0xBA: "OUT#",
    0xBB: "CIRCLE",
    0xBC: "TEST",
    0xBD: "PAGE",
    # 0xBE: None,
    # 0xBF: None,
    0xC0: "ERASE",
    0xC1: "ERROR",
    # 0xC2: None,
    0xC3: "USR",
    0xC4: "BYE",
    # 0xC5: None,
    # 0xC6: None,
    0xC7: "DEF",
    # 0xC8: None,
    # 0xC9: None,
    # 0xCA: None,
    # 0xCB: None,
    # 0xCC: None,
    # 0xCD: None,
    0xCE: "WOPEN",
    0xCF: "CLOSE",
    0xD0: "ROPEN",
    # 0xD1: None,
    # 0xD2: None,
    # 0xD3: None,
    # 0xD4: None,
    # 0xD5: None,
    # 0xD6: None,
    # 0xD7: None,
    # 0xD8: None,
    0xD9: "KILL",
    # 0xDA: None,
    # 0xDB: None,
    # 0xDC: None,
    # 0xDD: None,
    # 0xDE: None,
    # 0xDF: None,
    0xE0: "TO",
    0xE1: "STEP",
    0xE2: "THEN",
    0xE3: "USING",
    0xE4: "{FF}",
    # 0xE5: None,
    0xE6: "TAB",
    0xE7: "SPC",
    # 0xE8: None,
    # 0xE9: None,
    # 0xEA: None,
    0xEB: "OR",
    0xEC: "AND",
    # 0xED: None,
    0xEE: "><",
    0xEF: "<>",
    0xF0: "=<",
    0xF1: "<=",
    0xF2: "=>",
    0xF3: ">=",
    0xF4: "=",
    0xF5: ">",
    0xF6: "<",
    0xF7: "+",
    0xF8: "-",
    # 0xF9: None,
    # 0xFA: None,
    0xFB: "/",
    0xFC: "*",
    0xFD: "^",
}

# S-BASIC command list (0xFE81 - 0xFFFF)
sbasic_command_list_b = {
    # 0xFE80: None,
    0xFE81: "SET",
    0xFE82: "RESET",
    0xFE83: "COLOR",
    # 0xFE84: None,
    # ...
    # 0xFEA1: None,
    0xFEA2: "MUSIC",
    0xFEA3: "TEMPO",
    0xFEA4: "CURSOR",
    0xFEA5: "VERIFY",
    0xFEA6: "CLR",
    0xFEA7: "LIMIT",
    # 0xFEA8: None,
    # ...
    # 0xFEAD: None,
    0xFEAE: "BOOT",
    # 0xFEAF: None,
    0xFF80: "INT",
    0xFF81: "ABS",
    0xFF82: "SIN",
    0xFF83: "COS",
    0xFF84: "TAN",
    0xFF85: "LN",
    0xFF86: "EXP",
    0xFF87: "SQR",
    0xFF88: "RND",
    0xFF89: "PEEK",
    0xFF8A: "ATN",
    0xFF8B: "SGN",
    0xFF8C: "LOG",
    # 0xFF8D: None,
    0xFF8E: "PAI",
    0xFF8F: "RAD",
    # 0xFF90: None,
    # ...
    # 0xFF94: None,
    0xFF95: "EOF",
    # 0xFF96: None,
    # ...
    # 0xFF9D: None,
    0xFF9E: "JOY",
    # 0xFF9F: None,
    0xFFA0: "CHR$",
    0xFFA1: "STR$",
    0xFFA2: "HEX$",
    # 0xFFA3: None,
    # ...
    # 0xFFAA: None,
    0xFFAB: "ASC",
    0xFFAC: "LEN",
    0xFFAD: "VAL",
    # 0xFFAE: None,
    # ...
    # 0xFFB2: None,
    0xFFB3: "ERN",
    0xFFB4: "ERL",
    0xFFB5: "SIZE",
    # 0xFFB6: None,
    # 0xFFB7: None,
    # 0xFFB8: None,
    # 0xFFB9: None,
    0xFFBA: "LEFT$",
    0xFFBB: "RIGHT$",
    0xFFBC: "MID$",
    # 0xFFBD: None,
    # 0xFFBE: None,
    # 0xFFBF: None,
    # 0xFFC0: None,
    # 0xFFC1: None,
    # 0xFFC2: None,
    0xFFC3: "STRING$",
    0xFFC4: "TI$",
    # 0xFFC5: None,
    # 0xFFC6: None,
    0xFFC7: "FN",
    # 0xFFC8: None,
    # ...
    # 0xFFCF: None,
}

# Hu-BASIC command list (0x80 - 0xFD)
hubasic_command_list_a = {
    0x80: "GOTO",
    0x81: "GOSUB",
    0x82: "GO",
    0x83: "RUN",
    0x84: "RETURN",
    0x85: "RESTORE",
    0x86: "RESUME",
    0x87: "LIST",
    0x88: "LLIST",
    0x89: "DELETE",
    0x8A: "RENUM",
    0x8B: "AUTO",
    0x8C: "EDIT",
    0x8D: "FOR",
    0x8E: "NEXT",
    0x8F: "PRINT",
    0x90: "LPRINT",
    0x91: "INPUT",
    0x92: "LINPUT",
    0x93: "IF",
    0x94: "DATA",
    0x95: "READ",
    0x96: "DIM",
    0x97: "REM",
    0x98: "END",
    0x99: "STOP",
    0x9A: "CONT",
    0x9B: "CLS",
    0x9C: "CLEAR",
    0x9D: "ON",
    0x9E: "LET",
    0x9F: "NEW",
    0xA0: "POKE",
    0xA1: "OFF",
    0xA2: "WHILE",
    0xA3: "WEND",
    0xA4: "REPEAT",
    0xA5: "UNTIL",
    # 0xA6: None,
    # 0xA7: None,
    0xA8: "TRACE",
    0xA9: "TRON",
    0xAA: "TROFF",
    0xAB: "SPEED",
    # 0xAC: None,
    # 0xAD: None,
    0xAE: "DEFINT",
    0xAF: "DEFSNG",
    0xB0: "DEFDBL",
    0xB1: "DEFSTR",
    0xB2: "DEF",
    # 0xB3: None,
    0xB4: "LOAD",
    0xB5: "SAVE",
    0xB6: "MERGE",
    0xB7: "CHAIN",
    0xB8: "CONSOLE",
    # 0xB9: None,
    0xBA: "OUT",
    0xBB: "SEARCH",
    0xBC: "WAIT",
    0xBD: "PAUSE",
    0xBE: "WRITE",
    0xBF: "SWAP",
    0xC0: "ERASE",
    0xC1: "ERROR",
    0xC2: "ELSE",
    0xC3: "CALL",
    0xC4: "MON",
    0xC5: "LOCATE",
    0xC6: "MODE",
    0xC7: "KEY",
    0xC8: "PUSH",
    0xC9: "POP",
    0xCA: "LABEL",
    0xCB: "RANDOMIZE",
    0xCC: "OPTION",
    0xCD: "LINE",
    0xCE: "OPEN",
    0xCF: "CLOSE",
    # 0xD0: None,
    0xD1: "FIELD",
    0xD2: "GET",
    0xD3: "PUT",
    0xD4: "SET",
    0xD5: "FILES",
    0xD6: "LFILES",
    0xD7: "DEVICE",
    0xD8: "NAME",
    0xD9: "KILL",
    0xDA: "LSET",
    0xDB: "RSET",
    0xDC: "INIT",
    0xDD: "VDIM",
    0xDE: "MAXFILES",
    0xE0: "TO",
    0xE1: "STEP",
    0xE2: "THEN",
    0xE3: "USING",
    0xE4: "SUB",
    0xE5: "BASE",
    0xE6: "TAB",
    0xE7: "SPC",
    0xE8: "EQV",
    0xE9: "IMP",
    0xEA: "XOR",
    0xEB: "OR",
    0xEC: "AND",
    0xED: "NOT",
    0xEE: "><",
    0xEF: "<>",
    0xF0: "=<",
    0xF1: "<=",
    0xF2: "=>",
    0xF3: ">=",
    0xF4: "=",
    0xF5: ">",
    0xF6: "<",
    0xF7: "+",
    0xF8: "-",
    0xF9: "MOD",
    0xFA: "\\",
    0xFB: "/",
    0xFC: "*",
    0xFD: "^",
}

# Hu-BASIC command list (0xFE81 - 0xFFFF)
hubasic_command_list_b = {
    0xFE81: "PSET",
    0xFE82: "PRESET",
    0xFE83: "COLOR",
    # 0xFE84: None,
    # ...
    # 0xFE8A: None,
    0xFE8B: "PLAY",
    # 0xFE8C: None,
    0xFE8D: "BEEP",
    # 0xFE8E: None,
    # ...
    # 0xFE93: None,
    0xFE94: "CGEN",
    0xFE95: "PCOLOR",
    0xFE96: "SKIP",
    0xFE97: "RLINE",
    0xFE98: "MOVE",
    0xFE99: "RMOVE",
    0xFE9A: "PHOME",
    0xFE9B: "HSET",
    0xFE9C: "GPRINT",
    0xFE9D: "AXIS",
    0xFE9E: "CIRCLE",
    0xFE9F: "TSET",
    0xFEA0: "PLOT",
    0xFEA1: "PAGE",
    0xFEA2: "MUSIC",
    0xFEA3: "TEMPO",
    0xFEA4: "CURSOR",
    0xFEA5: "VERIFY",
    0xFEA6: "CLR",
    0xFEA7: "LIMIT",
    0xFEA8: "KLIST",
    # 0xFEA9: None,
    # 0xFEAA: None,
    0xFEAB: "CLICK",
    0xFEAC: "BOOT",
    0xFEAD: "DEVI$",
    0xFEAE: "DEVO$",
    # 0xFEAF: None,
    0xFF80: "INT",
    0xFF81: "ABS",
    0xFF82: "SIN",
    0xFF83: "COS",
    0xFF84: "TAN",
    0xFF85: "LOG",
    0xFF86: "EXP",
    0xFF87: "SQR",
    0xFF88: "RND",
    0xFF89: "PEEK",
    0xFF8A: "ATN",
    0xFF8B: "SGN",
    0xFF8C: "FRAC",
    0xFF8D: "FIX",
    0xFF8E: "PAI",
    0xFF8F: "RAD",
    0xFF90: "INP",
    0xFF91: "CDBL",
    0xFF92: "CSNG",
    0xFF93: "CINT",
    0xFF94: "DSKF",
    0xFF95: "EOF",
    0xFF96: "FPOS",
    0xFF97: "LOC",
    0xFF98: "LOF",
    0xFF99: "POS",
    0xFF9A: "FAC",
    0xFF9B: "SUM",
    0xFF9C: "FRE",
    0xFF9D: "LPOS",
    0xFF9E: "JOY",
    # 0xFE9F: None,
    0xFFA0: "CHR$",
    0xFfA1: "STR$",
    0xFFA2: "HEX$",
    0xFfA3: "OCT$",
    0xFFA4: "BIN$",
    0xFFA5: "MKI$",
    0xFFA6: "MKS$",
    0xFFA7: "MKD$",
    0xFFA8: "SPACE$",
    # 0xFEA9: None,
    # 0xFEAA: None,
    0xFFAB: "ASC",
    0xFFAC: "LEN",
    0xFFAD: "VAL",
    0xFFAE: "CVS",
    0xFFAF: "CVD",
    0xFFB0: "CVI",
    # 0xFEB1: None,
    # 0xFEB2: None,
    0xFFB3: "ERR",
    0xFFB4: "ERL",
    0xFFB5: "CSRLIN",
    0xFFB6: "STRPTR",
    0xFFB7: "DTL",
    # 0xFEB8: None,
    # 0xFEB9: None,
    0xFFBA: "LEFT$",
    0xFFBB: "RIGHT$",
    0xFFBC: "MID$",
    0xFFBD: "INKEY$",
    0xFFBE: "INSTR",
    0xFFBF: "HEXCHR$",
    0xFFC0: "MEM$",
    0xFFC1: "SCRN$",
    0xFFC2: "VARPTR",
    0xFFC3: "STRING$",
    0xFFC4: "TIME$",
    # 0xFEC5: None,
    # 0xFEC6: None,
    0xFFC7: "FN",
    0xFFC8: "USR",
    # 0xFEC9: None,
    # 0xFECA: None,
    0xFFCB: "ATTR$",
    # 0xFECC: None,
    0xFFCD: "CHARACTER$",
    # 0xFECE: None,
}

# SP-5030 or S-BASIC control code
ctrl_dic_sbasic = {
    0x05: "{lower}",
    0x06: "{upper}",
    0x0D: "{CR}",
    0x11: u"{↓}",  # down arrow BG reverse
    0x12: u"{↑}",  # up arrow BG reverse
    0x13: u"{→}",  # right arrow BG reverse
    0x14: u"{←}",  # left arrow BG reverse
    0x15: "{HOME}",
    0x16: "{CLR}",
    0x18: "{INST}",
}

# Hu-BASIC control code
ctrl_dic_hubasic = {
    0x0B: "{HOME}",
    0x0C: "{CLR}",
    0x0D: "{CR}",
    0x10: "{lower}",
    0x11: "{upper}",
    0x12: "{INST}",
    0x1C: u"{→}",  # right arrow BG reverse
    0x1D: u"{←}",  # left arrow BG reverse
    0x1E: u"{↑}",  # up arrow BG reverse
    0x1F: u"{↓}",  # down arrow BG reverse
}

# japanese character. kanji.
kanji_dic = u'日月火水木金土生年時分秒円￥￡'

# japanese character. kana.
kana_dic = u'。「」、．ヲァィゥェォャュョッ'
kana_dic += u'ーアイウエオカキクケコサシスセソ'
kana_dic += u'タチツテトナニヌネノハヒフヘホマ'
kana_dic += u'ミムメモヤユヨラリルレロワン゛゜'

# japanese character. graphic.
graph_dic = {
    0x5E: u'↑',  # up arrow
    0x5F: u'←',  # left arrow
    0x60: '{ufo}',
    0x63: '{human}',
    0x67: '{smileblack}',
    0x68: '{smilewhite}',
    0x69: '{snake}',
    0x80: u'↓',  # down arrow
    0xC0: u'→',  # right arrow
    # 0xC2: u'▄',
    0xC4: u'_',
    # 0xC5: u'▏',
    # 0xC6: u'▒',  # fill block half tone
    0xC8: u'■',  # fill block
    # 0xC9: u'◤',
    0xCB: u'├',
    # 0xCC: u'◘',
    0xCD: u'└',
    0xCE: u'┐',
    # 0xCF: u'▂',
    0xD0: u'┌',
    0xD1: u'┴',
    0xD2: u'┬',
    0xD3: u'┤',
    # 0xD4: u'▎',
    # 0xD5: u'▌',
    # 0xD8: u'▀',
    # 0xD9: u'▃',
    0xDD: u'┘',
    # 0xDE: u'▞',
    # 0xDF: u'▚',
    0xE0: u'─',
    0xE1: '{spade}',
    # 0xE9: u'◣',
    0xED: u'＼',
    0xEE: u'／',
    0xF1: u'●',
    0xF3: '{heart}',
    # 0xF5: u'◢',
    0xF6: u'×',
    0xF7: u'○',
    0xF8: '{club}',
    0xFA: u'◆',  # diamond
    0xFB: u'┼',
    0xFD: u'│',
    # 0xFE: u'◥',
    0xFF: u'π',
}


def get_byte(buf, p):
    """Get 1byte value."""
    return ord(buf[p])


def get_last_byte(buf):
    """Get last 1byte value."""
    return ord(buf[-1:])


def get_word(buf, p):
    """Get 2byte value (little endian)."""
    v = ord(buf[p + 1]) << 8 | ord(buf[p])
    return v


def get_word_big_endian(buf, p):
    """Get 2byte value (big endian)."""
    v = ord(buf[p]) << 8 | ord(buf[p + 1])
    return v


def get_float(bindata):
    """Get float value (5 byte)."""
    v = struct.unpack('BBBBB', bindata)
    e = v[0]
    r = v[1] << 24 | v[2] << 16 | v[3] << 8 | v[4]
    s = -1 if (r & 0x80000000) != 0 else 1
    if e == 0:
        return 0.0
    e -= 128
    d = (r | 0x80000000) * pow(2, e - 32)
    return s * d


def get_double(bindata):
    """Get double value (8 byte)."""
    v = struct.unpack('BBBBBBBB', bindata)
    e = v[0]
    rh = v[1] << 24 | v[2] << 16 | v[3] << 8 | v[4]
    rl = v[5] << 24 | v[6] << 16 | v[7] << 8
    s = -1 if (rh & 0x80000000) != 0 else 1
    if e == 0:
        return 0.0
    e -= 128
    d = (rh | 0x80000000) * pow(2.0, e - 32)
    d += rl * pow(2.0, e - 32 - 24)
    return s * d


def get_binary_string(v):
    """Get binary string (2 byte)."""
    s = ""
    j = 0x8000
    while (j > 1 and (v & j) == 0):
        j >>= 1
    while j != 0:
        s += '1' if (v & j) != 0 else '0'
        j >>= 1
    return s


def conv_chr(c):
    """Get charactor ASCII or not ASCII."""
    if 0x20 <= c and c <= 0x5d:  # in ASCII
        return chr(c)

    if jp_flag:  # output japanese character
        if target_id == ID_HUBASIC:
            if c in ctrl_dic_hubasic:  # in control code
                return ctrl_dic_hubasic[c]
        else:
            if c in ctrl_dic_sbasic:  # in control code
                return ctrl_dic_sbasic[c]

        if 0x70 <= c and c <= 0x7e:  # in kanji
            return kanji_dic[c - 0x70]

        if 0x81 <= c and c <= 0xbf:  # in kana
            return kana_dic[c - 0x81]

        if c in graph_dic:  # in graphic
            return graph_dic[c]

    return "{%02X}" % c


def found_word_endcode(buf, endcode):
    """Check source end code."""
    if get_word(buf, len(buf) - 2) != endcode:
        return False
    return True


def get_line_sp5030(line, lp, line_end_code):
    """Get SP-5030 1 line string."""
    s = ""
    str_mode = False
    rem_mode = False
    while True:
        c = get_byte(line, lp)
        lp += 1
        if c == line_end_code:
            break

        if str_mode or rem_mode:
            s += conv_chr(c)
            if str_mode and c == ord('"'):
                str_mode = False
            if rem_mode and c == ord(':'):  # multi statement separator
                rem_mode = False
        elif c in sp5030_command_list:
            cmdstr = sp5030_command_list[c]
            s += cmdstr
            if cmdstr == "REM" or cmdstr == "DATA":
                rem_mode = True
        else:
            s += conv_chr(c)
            if c == ord('"'):
                str_mode = True
    return s


def get_line_sbasic(line, lp, line_end_code):
    """Get S-BASIC 1 line string."""
    s = ""
    str_mode = False
    rem_mode = False
    while True:
        c = get_byte(line, lp)
        lp += 1
        if c == line_end_code:
            break

        w = 0
        if c == 0xfe or c == 0xff:
            w = get_word_big_endian(line, lp - 1)

        if str_mode or rem_mode:
            s += conv_chr(c)
            if str_mode and c == ord('"'):
                str_mode = False
            if rem_mode and c == ord(':'):
                # multi statement separator
                rem_mode = False
        elif c in sbasic_command_list_a:
            # 0x80 - 0xfd
            cmdstr = sbasic_command_list_a[c]
            s += cmdstr
            if cmdstr == "REM" or cmdstr == "DATA":
                rem_mode = True
        elif w != 0 and w in sbasic_command_list_b:
            # 0xfexx - 0xffxx
            cmdstr = sbasic_command_list_b[w]
            s += cmdstr
            lp += 1
        elif c == 0x0b:  # line number
            s += "%d" % get_word(line, lp)
            lp += 2
        elif c == 0x11:  # hex number ($xxxx)
            s += "%X" % get_word(line, lp)
            lp += 2
        elif c == 0x15:  # float number
            s += "%g" % get_float(line[lp:lp + 5])
            lp += 5
        else:
            s += conv_chr(c)
            if c == ord('"'):
                str_mode = True
    return s


def get_line_hubasic(line, lp, line_end_code):
    """Get Hu-BASIC 1 line string."""
    s = ""
    str_mode = False
    rem_mode = False
    while True:
        c = get_byte(line, lp)
        lp += 1
        if c == line_end_code:
            break

        c0 = get_byte(line, lp)
        w = 0
        if c == 0xfe or c == 0xff:
            w = get_word_big_endian(line, lp - 1)

        if str_mode or rem_mode:
            s += conv_chr(c)
            if str_mode and c == ord('"'):
                str_mode = False
            if rem_mode and c == ord(':'):
                # multi statement separator
                rem_mode = False
        elif c in hubasic_command_list_a:
            # 0x80 - 0xfd
            cmdstr = hubasic_command_list_a[c]
            s += cmdstr
            if cmdstr == "REM" or cmdstr == "DATA":
                rem_mode = True
        elif w != 0 and w in hubasic_command_list_b:
            # 0xfexx - 0xffxx
            cmdstr = hubasic_command_list_b[w]
            s += cmdstr
            lp += 1
        elif 1 <= c and c <= 10:  # integer number (0-9)
            s += "%s" % chr(0x30 + c - 1)
        elif c == 0x0b:  # line number (GOTO xxxx, GOSUB xxxx)
            s += "%d" % get_word(line, lp)
            lp += 2
        elif c == 0x0d:  # octal number (&Oxxxx)
            s += "&O%o" % get_word(line, lp)
            lp += 2
        elif c == 0x0e:  # binary number (&Bxxxx)
            i = get_word(line, lp)
            s += "&B%s" % get_binary_string(i)
            lp += 2
        elif c == 0x0f:  # hex number (&Hxxxx)
            s += "&H%X" % get_word(line, lp)
            lp += 2
        elif c == 0x12:  # integer number
            i = get_word(line, lp)
            if i > 0x7fff:
                i -= 0x10000
            s += "%d" % i
            lp += 2
        elif c == 0x15:  # float number
            s += "%g" % get_float(line[lp:lp + 5])
            lp += 5
        elif c == 0x18:  # double number
            s += "%g" % get_double(line[lp:lp + 8])
            lp += 8
        elif c == ord(':'):
            if c0 == 0x27:  # REM character
                s += conv_chr(c0)
                lp += 1
                rem_mode = True
            elif c0 == 0xc2:  # ELSE code
                pass
            else:
                s += conv_chr(c)
        else:
            s += conv_chr(c)
            if c == ord('"'):
                str_mode = True
    return s


def dump_source(buf, id):
    """Dump BASIC source."""

    if id == ID_SP5030:
        line_end_code = 0x0d
        src_end_code = 0x0000
        kind = "SP-5030"
    elif id == ID_SBASIC:
        line_end_code = 0x00
        src_end_code = 0x0000
        kind = "S-BASIC"
    elif id == ID_HUBASIC:
        line_end_code = 0x00
        src_end_code = 0x0000
        kind = "Hu-BASIC"
    else:
        return 1

    if not found_word_endcode(buf, src_end_code):
        print("Not found %s end code (0x%04X)" % (kind, src_end_code))
        return 1

    p = 0
    while True:
        line_length = get_word(buf, p)
        if line_length == src_end_code:
            # Found Source end code
            break

        # get 1 line data
        line = buf[p:p + line_length]
        if get_last_byte(line) != line_end_code:
            print("Not found %s line end code (0x%02X)" % (kind, line_end_code))
            return 1

        line_number = get_word(line, 2)
        if id == ID_SP5030:
            lstr = get_line_sp5030(line, 4, line_end_code)
        elif id == ID_SBASIC:
            lstr = get_line_sbasic(line, 4, line_end_code)
        elif id == ID_HUBASIC:
            lstr = get_line_hubasic(line, 4, line_end_code)

        if jp_flag:
            # print("%d %s" % (line_number, lstr.encode('utf-8')))
            print("%d %s" % (line_number, lstr.encode('cp932')))
        else:
            print("%d %s" % (line_number, lstr))

        p += line_length

    return 0


def main():
    """main."""
    global jp_flag
    global target_id

    target_list = {
        "sp5030": ID_SP5030,
        "sbasic": ID_SBASIC,
        "hubasic": ID_HUBASIC
    }

    # get command line oprion
    p = argparse.ArgumentParser()
    p.description = "Convert BASIC program in MZT file to text."
    p.add_argument("--version", action='version', version="%(prog)s 1.1")
    p.add_argument("infile", metavar='INFILE', help=".mzt file")
    p.add_argument("--target", choices=target_list.keys(),
                   help="target BASIC. SP-5030, S-BASIC, Hu-BASIC")
    p.add_argument("--jp", default=False, action='store_true',
                   help="output japanese character")
    args = p.parse_args()
    infile = args.infile
    target = args.target
    jp_flag = args.jp

    if target is None:
        target = "sp5030"

    if target in target_list:
        target_id = target_list[target]
    else:
        print("Unknown target : %s" % target)
        sys.exit(1)

    # read binary file
    f = open(infile, "rb")
    buf = f.read()
    f.close()

    # MZT header
    head_tape = buf[:24]
    # head_fd = buf[24:0x40]
    # patch = buf[0x40:0x80]
    body = buf[0x80:]
    datasize = len(body)

    attr, fn, fsize, sadrs, eadrs = struct.unpack("<B17sHHH", head_tape)

    if fsize != datasize:
        print("Data size does not match.")
        print("data size in header : 0x%04x" % fsize)
        print("real data size      : 0x%04x" % datasize)
        sys.exit(1)

    if attr == 0x01:
        print("MZT attribute is 0x%02X = binary file. Not target." % attr)
        sys.exit(1)

    ret = 0
    if target_id == ID_SP5030 and attr == 0x02:
        ret = dump_source(body, ID_SP5030)
    elif target_id == ID_SBASIC and attr == 0x05:
        ret = dump_source(body, ID_SBASIC)
    elif target_id == ID_HUBASIC and attr == 0x02:
        ret = dump_source(body, ID_HUBASIC)
    else:
        print("MZT attribute is 0x%02X. Not target." % attr)
        print("0x02 : SP-5030 or Hu-BASIC")
        print("0x05 : S-BASIC")
        ret = 1

    sys.exit(ret)


if __name__ == '__main__':
    main()
