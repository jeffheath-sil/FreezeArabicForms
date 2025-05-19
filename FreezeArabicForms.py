#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# FreezeArabicForms
#
progVersion = "2.2"
description = "Freeze Arabic script letters in their contextual forms. (V{})".format(progVersion)
#
epilog = \
"""In most cases Arabic script letters are automatically displayed in their
proper contextual forms depending on their position in the word (initial,
medial, final, or isolated). This program identifies the proper contextual
form of each Arabic script letter in an input text file and "freezes" it
into its proper contextual form, using Zero Width Joiners (ZWJs), and by
placing Word Joiners (WJs) between the letters to avoid any confusion
about which letter is joining. This can facilitate the analysis of different
Arabic script contextual forms used in a text, particularly using PrimerPrep."""
#
# by Jeff Heath
#
# © 2019 SIL International
#
# Inspired by the pip arabic-reshaper module, Website: http://mpcabd.xyz
# which was written by Abdullah Diab (mpcabd@gmail.com)
#
# Modifications:
# 2.2 JCH Oct 2019
#    Use U+2060 Word Joiner instead of U+200B Zero Width Space (ZWS), since that is
#    used in Khmer, etc. for identifying word breaks
# 2.1 JCH Jun 2019
#    In reshape, make sure prevAS is initialized if first letter in line is not AS
# 2.0 JCH Jun 2019
#    Rather than using arabic-reshaper module, rolled our own reshape function
#    which uses lists of harakat, and characters with different joining characteristics
#    and adds required ZWSs between AS letters, and ZWJs to force contextual forms
# 
# 

import argparse
import re


# define Zero Width Joiner and Zero Width Space
ZWJ = '\u200d'
WJ = '\u2060'

# define Arabic vowels (joining happens through them)
ArabicHarakat = [ '\u0610', '\u0611', '\u0612', '\u0613', '\u0614', '\u0615', '\u0616', '\u0617',
                  '\u0618', '\u0619', '\u061A', '\u064B', '\u064C', '\u064D', '\u064E', '\u064F',
                  '\u0650', '\u0651', '\u0652', '\u0653', '\u0654', '\u0655', '\u0656', '\u0657',
                  '\u0658', '\u0659', '\u065A', '\u065B', '\u065C', '\u065D', '\u065E', '\u065F',
                  '\u0670', '\u06D6', '\u06D7', '\u06D8', '\u06D9', '\u06DA', '\u06DB', '\u06DC',
                  '\u06DF', '\u06E0', '\u06E1', '\u06E2', '\u06E3', '\u06E4', '\u06E7', '\u06E8',
                  '\u06EA', '\u06EB', '\u06EC', '\u06ED', '\u08D3', '\u08D4', '\u08D5', '\u08D6',
                  '\u08D7', '\u08D8', '\u08D9', '\u08DA', '\u08DB', '\u08DC', '\u08DD', '\u08DE',
                  '\u08DF', '\u08E0', '\u08E1', '\u08E3', '\u08E4', '\u08E5', '\u08E6', '\u08E7',
                  '\u08E8', '\u08E9', '\u08EA', '\u08EB', '\u08EC', '\u08ED', '\u08EE', '\u08EF',
                  '\u08F0', '\u08F1', '\u08F2', '\u08F3', '\u08F4', '\u08F5', '\u08F6', '\u08F7',
                  '\u08F8', '\u08F9', '\u08FA', '\u08FB', '\u08FC', '\u08FD', '\u08FE', '\u08FF']

# define joining Arabic letters
DualJoining = [ '\u0620', '\u0626', '\u0628', '\u062A', '\u062B', '\u062C', '\u062D', '\u062E',
                '\u0633', '\u0634', '\u0635', '\u0636', '\u0637', '\u0638', '\u0639', '\u063A',
                '\u063B', '\u063C', '\u063D', '\u063E', '\u063F', '\u0641', '\u0642', '\u0643',
                '\u0644', '\u0645', '\u0646', '\u0647', '\u0649', '\u064A', '\u066E', '\u066F',
                '\u0678', '\u0679', '\u067A', '\u067B', '\u067C', '\u067D', '\u067E', '\u067F',
                '\u0680', '\u0681', '\u0682', '\u0683', '\u0684', '\u0685', '\u0686', '\u0687',
                '\u069A', '\u069B', '\u069C', '\u069D', '\u069E', '\u069F', '\u06A0', '\u06A1',
                '\u06A2', '\u06A3', '\u06A4', '\u06A5', '\u06A6', '\u06A7', '\u06A8', '\u06A9',
                '\u06AA', '\u06AB', '\u06AC', '\u06AD', '\u06AE', '\u06AF', '\u06B0', '\u06B1',
                '\u06B2', '\u06B3', '\u06B4', '\u06B5', '\u06B6', '\u06B7', '\u06B8', '\u06B9',
                '\u06BA', '\u06BB', '\u06BC', '\u06BD', '\u06BE', '\u06BF', '\u06C1', '\u06C2',
                '\u06CC', '\u06CE', '\u06D0', '\u06D1', '\u06FA', '\u06FB', '\u06FC', '\u06FF',
                '\u0750', '\u0751', '\u0752', '\u0753', '\u0754', '\u0755', '\u0756', '\u0757',
                '\u0758', '\u075C', '\u075D', '\u075E', '\u075F', '\u0760', '\u0761', '\u0762',
                '\u0763', '\u0764', '\u0765', '\u0766', '\u0767', '\u0768', '\u0769', '\u076A',
                '\u076D', '\u076E', '\u076F', '\u0770', '\u0772', '\u0775', '\u0776', '\u0777',
                '\u077A', '\u077B', '\u077C', '\u077D', '\u077E', '\u077F', '\u08A0', '\u08A1',
                '\u08A2', '\u08A3', '\u08A4', '\u08A5', '\u08A6', '\u08A7', '\u08A8', '\u08A9',
                '\u08AF', '\u08B0', '\u08B3', '\u08B4', '\u08B6', '\u08B7', '\u08B8', '\u08BA',
                '\u08BB', '\u08BC', '\u08BD' ]
RightJoining = [ '\u0622', '\u0623', '\u0624', '\u0625', '\u0627', '\u0629', '\u062F', '\u0630',
                 '\u0631', '\u0632', '\u0648', '\u0671', '\u0672', '\u0673', '\u0675', '\u0676',
                 '\u0677', '\u0688', '\u0689', '\u068A', '\u068B', '\u068C', '\u068D', '\u068E',
                 '\u068F', '\u0690', '\u0691', '\u0692', '\u0693', '\u0694', '\u0695', '\u0696',
                 '\u0697', '\u0698', '\u0699', '\u06C0', '\u06C3', '\u06C4', '\u06C5', '\u06C6',
                 '\u06C7', '\u06C8', '\u06C9', '\u06CA', '\u06CB', '\u06CD', '\u06CF', '\u06D2',
                 '\u06D3', '\u06D5', '\u06EE', '\u06EF', '\u0759', '\u075A', '\u075B', '\u076B',
                 '\u076C', '\u0771', '\u0773', '\u0774', '\u0778', '\u0779', '\u08AA', '\u08AB',
                 '\u08AC', '\u08AE', '\u08B1', '\u08B2', '\u08B9' ]
AllJoining = DualJoining + RightJoining


def reshape(line):
    if not line:
        # if input is empty, return an empty string
        return ''
    # store first letter in the line
    letter = line[0]
    output = [ line[0] ]
    prevAS = False
    if letter in AllJoining:
        prevAS = True
        idx = 0
    for letter in line[1:]:
        if letter in AllJoining:
            # this is a joining Arabic letter, may need some special processing
            if prevAS:
                # always include a Zero Width Space between Arabic letters
                output.append(WJ)
                attaching = False
                if output[idx] in DualJoining:
                    # change it to attaching form
                    output.insert(idx+1, ZWJ)
                    attaching = True
                if attaching and letter in AllJoining:
                    # current letter also needs a ZWJ to connect on right
                    output.append(ZWJ)
            output.append(letter)
            prevAS = True
            idx = len(output) - 1
        elif letter in ArabicHarakat:
            # for vowels we maintain prevAS and idx, but don't adjust connections
            if prevAS:
                # always include a Zero Width Space between Arabic letters
                output.append(WJ)
            output.append(letter)
        else:
            prevAS = False
            output.append(letter)
    
    return ''.join(output)



def main():
    parser = argparse.ArgumentParser(description=description, epilog=epilog)
    parser.add_argument('filename', type=str,
                        help='Name of file with Arabic text to convert to contextual forms')
    parser.add_argument('-o', '--output', type=str, dest='output', 
                        help='Name of output file (default adds -forms to filename)')
    args = parser.parse_args()
    
    if not args.output:
        args.output = re.sub(r'(\.\w+)', '-forms\\1', args.filename)
    
    # open the output file
    fout = open(args.output, mode='w', encoding='utf-8-sig')
    with open(args.filename, mode='r', encoding='utf-8-sig') as fin:
        for line in fin:
            reshaped_line = reshape(line)
            fout.write(reshaped_line)
    fout.close()
    
    print('\nFreezeArabicForms has processed the file "{}".'.format(args.filename))
    print('All of the Arabic script letters were frozen to their Arabic Presentation Forms.')
    print('The resulting text was written to "{}".'.format(args.output))


if __name__ == '__main__':
    main()

