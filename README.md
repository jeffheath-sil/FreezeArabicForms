# FreezeArabicForms
Utility to "freeze" Arabic letter forms in their contextual forms (initial, medial, final) for additional analysis

(from in-program help, "FreezeArabicForms -h")
Freeze Arabic script letters in their contextual forms.

positional arguments:
  filename              Name of file with Arabic text to convert to contextual
                        forms

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Name of output file (default adds -forms to filename)

In most cases Arabic script letters are automatically displayed in their
proper contextual forms depending on their position in the word (initial,
medial, final, or isolated). This program identifies the proper contextual
form of each Arabic script letter in an input text file and "freezes" it
into its proper contextual form, using Zero Width Joiners (ZWJs), and by
placing Word Joiners (WJs) between the letters to avoid any confusion
about which letter is joining. This can facilitate the analysis of different
Arabic script contextual forms used in a text, particularly using PrimerPrep.
