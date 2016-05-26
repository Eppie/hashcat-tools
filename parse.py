#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import os.path

def isValidFile(parser, arg):
    try:
        return open(arg, 'r')
    except IOError:
        parser.error('The file \'{}\' does not exist!'.format(arg))


def applyOp(string, op, param1=None, param2=None):
    if op == ':': # Do nothing
        return string
    elif op == 'l': # Lowercase all letters
        return string.lower()
    elif op == 'u': # Uppercase all letteres
        return string.upper()
    elif op == 'c': # Capitalize the first letter and lower the rest
        return string[0].upper() + string[1:].lower()
    elif op == 'C': # Lowercase first found character, uppercase the rest
        return string[0].lower() + string[1:].upper()
    elif op == 't': # Toggle the case of all characters in word
        return ''.join(c.lower() if c.isupper() else c.upper() for c in string)
    elif op == 'T': # Toggle the case of characters at position N
        param1 = int(param1)
        c = string[param1]
        return string[:param1] + (c.lower() if c.isupper() else c.upper()) + string[param1 + 1:]
    elif op == 'r': # Reverse the entire word
        return string[::-1]
    elif op == 'd': # Duplicate the entire word
        return string + string
    elif op == 'p': # Append duplicated word N times
        param1 = int(param1)
        return string * (param1 + 1)
    elif op == 'f': # Duplicate word reversed
        return string + string[::-1]
    elif op == '{': # Rotates the word left
        return string[1:] + string[0]
    elif op == '}': # Rotates the word right
        return string[-1] + string[:-1]
    elif op == '$': # Append character X to end
        return string + param1
    elif op == '^': # Prepend character X to front
        return param1 + string
    elif op == '[': # Deletes first character
        return string[1:]
    elif op == ']': # Deletes last character
        return string[:-1]
    elif op == 'D': # Deletes character at position N
        param1 = int(param1)
        return string[:param1] + string[param1 + 1:]
    elif op == 'x': # Extracts M characters, starting at position N
        N = int(param1)
        M = int(param2)
        if len(string) <= N:
            return string
        return string[N: N + M]
    elif op == 'O': # Deletes M characters, starting at position N
        param1 = int(param1)
        param2 = int(param2)
        return string[:param1] + string[param1 + param2:]
    elif op == 'i': # Inserts character X at position N
        param1 = int(param1)
        return string[:param1] + param2 + string[param1:]
    elif op == 'o': # Overwrites character at position N with X
        param1 = int(param1)
        return string[:param1] + param2 + string[param1 + 1:]
    elif op == '\'': # Truncate word at position N
        param1 = int(param1)
        return string[:param1]
    elif op == 's': # Replace all instances of X with Y
        return ''.join(param2 if c == param1 else c for c in string)
    elif op == '@': # Purge all instances of X
        return ''.join('' if c == param1 else c for c in string)
    elif op == 'z': # Duplicates first character N times
        param1 = int(param1)
        return string[0] * param1 + string
    elif op == 'Z': # Duplicates last character N times
        param1 = int(param1)
        return string + string[-1] * param1
    elif op == 'q': # Duplicate every character
        return ''.join(c * 2 for c in string)
    elif op == 'k': # Swaps first two characters
        return string[1] + string[0] + string[2:]
    elif op == 'K': # Swaps last two characters
        return string[:-2] + string[-1] + string[-2]
    elif op == '*': # Swaps character at position X with character at position Y
        param1 = int(param1)
        param2 = int(param2)
        l = list(string)
        l[param1], l[param2] = l[param2], l[param1]
        return ''.join(l)
    elif op == 'L': # Bitwise shift left character at position N
        param1 = int(param1)
        print string[:param1] + chr(ord(string[param1]) << 1) + string[param1 + 1:]
    elif op == 'R': # Bitwise shift right character at position N
        param1 = int(param1)
        return string[:param1] + chr(ord(string[param1]) >> 1) + string[param1 + 1:]
    elif op == '+': # Increment character at position N by 1 ascii value
        param1 = int(param1)
        return string[:param1] + chr(ord(string[param1]) + 1) + string[param1 + 1:]
    elif op == '-': # Decrement character at position N by 1 ascii value
        param1 = int(param1)
        return string[:param1] + chr(ord(string[param1]) - 1) + string[param1 + 1:]
    elif op == '.': # Replaces character at position N with value at N plus 1
        param1 = int(param1)
        l = list(string)
        l[param1] = l[param1 + 1]
        return ''.join(l)
    elif op == ',': # Replaces character at position N with value at N minus 1
        param1 = int(param1)
        l = list(string)
        l[param1] = l[param1 - 1]
        return ''.join(l)
    elif op == 'y': # Duplicates first N characters
        param1 = int(param1)
        return string[:param1] + string
    elif op == 'Y': # Duplicates last N characters
        param1 = int(param1)
        return string + string[-param1:]
    elif op == 'E': # Lowercase the whole line, then uppercase the first letter and every letter after a space
        return ' '.join(c.capitalize() for c in string.lower().split(' '))
    else:
        raise ValueError('Rule contained unrecognized character: {}'.format(op))


def applyRule(string, rule, debug=False):
    oneParam = 'Tp$^D\'@zZLR+-.,yY'
    twoParam = 'xOios*'

    l = len(rule)
    i = 0;
    while i < l:
        op = rule[i]
        if op == ' ':
            if debug:
                print('Ignoring space at position {}'.format(i))
        elif op in oneParam:
            param1 = rule[i + 1]
            string = applyOp(string, op, param1)
            i += 1
            if debug:
                print('Applied op: \'{}\' with argument \'{}\'. Result: {}'.format(op, param1, string))
        elif op in twoParam:
            param1 = rule[i + 1]
            param2 = rule[i + 2]
            string = applyOp(string, op, param1, param2)
            i += 2
            if debug:
                print('Applied op: \'{}\' with arguments \'{}\', \'{}\'. Result: {}'.format(op, param1, param2, string))
        else:
            try:
                string = applyOp(string, op)
                if debug:
                    print('Applied op: \'{}\'. Result: {}'.format(op, string))
            except:
                pass
        i += 1
    return string

s = 'p@ssW0rd'
e = 'p@ssW0rd w0rld'

parser = argparse.ArgumentParser(description='Apply a number of rules to a number of strings')
parser.add_argument('-v', '--verbose', action='store_true', help='Show some debugging info')
parser.add_argument('-r', dest='rulefile', help='Read one or more rules from a file', type=lambda x: isValidFile(parser, x))
args = parser.parse_args()

rule = 'x83 x61 i5 '
print applyRule(s, rule, args.verbose)


assert(applyOp(s, ':') == 'p@ssW0rd')
assert(applyOp(s, 'l') == 'p@ssw0rd')
assert(applyOp(s, 'u') == 'P@SSW0RD')
assert(applyOp(s, 'c') == 'P@ssw0rd')
assert(applyOp(s, 'C') == 'p@SSW0RD')
assert(applyOp(s, 't') == 'P@SSw0RD')
assert(applyOp(s, 'T', 3) == 'p@sSW0rd')
assert(applyOp(s, 'r') == 'dr0Wss@p')
assert(applyOp(s, 'd') == 'p@ssW0rdp@ssW0rd')
assert(applyOp(s, 'p', 2) == 'p@ssW0rdp@ssW0rdp@ssW0rd')
assert(applyOp(s, 'f') == 'p@ssW0rddr0Wss@p')
assert(applyOp(s, '{') == '@ssW0rdp')
assert(applyOp(s, '}') == 'dp@ssW0r')
assert(applyOp(s, '$', '1') == 'p@ssW0rd1')
assert(applyOp(s, '^', '1') == '1p@ssW0rd')
assert(applyOp(s, '[') == '@ssW0rd')
assert(applyOp(s, ']') == 'p@ssW0r')
assert(applyOp(s, 'D', 3) == 'p@sW0rd')
assert(applyOp(s, 'x', 0, 4) == 'p@ss')
assert(applyOp(s, 'O', 1, 2) == 'psW0rd')
assert(applyOp(s, 'i', 4, '!') == 'p@ss!W0rd')
assert(applyOp(s, 'o', 3, '$') == 'p@s$W0rd')
assert(applyOp(s, '\'', 6) == 'p@ssW0')
assert(applyOp(s, 's', 's', '$') == 'p@$$W0rd')
assert(applyOp(s, '@', 's') == 'p@W0rd')
assert(applyOp(s, 'z', 2) == 'ppp@ssW0rd')
assert(applyOp(s, 'Z', 2) == 'p@ssW0rddd')
assert(applyOp(s, 'q') == 'pp@@ssssWW00rrdd')
assert(applyOp(s, 'k') == '@pssW0rd')
assert(applyOp(s, 'K') == 'p@ssW0dr')
assert(applyOp(s, '*', 3, 4) == 'p@sWs0rd')
# assert(applyOp(s, 'L', 2) == 'p@æsW0rd')
assert(applyOp(s, 'R', 2) == 'p@9sW0rd')
assert(applyOp(s, '+', 2) == 'p@tsW0rd')
assert(applyOp(s, '-', 1) == 'p?ssW0rd')
assert(applyOp(s, '.', 1) == 'psssW0rd')
assert(applyOp(s, ',', 1) == 'ppssW0rd')
assert(applyOp(s, 'y', 2) == 'p@p@ssW0rd')
assert(applyOp(s, 'Y', 2) == 'p@ssW0rdrd')
assert(applyOp(e, 'E') == 'P@ssw0rd W0rld')
