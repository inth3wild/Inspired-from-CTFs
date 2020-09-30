#!/usr/bin/env python
import argparse
import optparse
import subprocess


magic_bytes = {
    "jpeg": ["FF D8 FF DB"],
    "exe": ["5A 4D"],
    "png": ["89 50 4E 47 0D 0A 1A 0A",]
}

# xxd -r -p -o OFFSET <(echo NEW HEX SIGNATURE) FILE
# where OFFSET = 0, NEW HEX SIGNATURE = FF D8 FF DB and FILE = anyfile
# xxd -r -p -o 0 <(echo FF D8 FF DB) anyfile
# sed -i '1s/^/\n\n /' me.txt
# echo "0000000: FF D8 FF DB" | xxd -r - anyfile

parser = optparse.OptionParser()

parser.add_option("-o", "--offset", dest="offset", help="Position to inject")
parser.add_option("-t", "--filetype", dest="filetype", help="Type of file to create")
parser.add_option("-f", "--file", dest="file", help="The file to change")

(value, flag) = parser.parse_args()

offset  = value.offset
filetype = value.filetype
file = value.file

spaces = ""


def calc_spaces(filetype):
    global spaces
    no_of_spaces = len( magic_bytes[filetype][0].split(" ") ) 
    print("no of spaces:", no_of_spaces)
    for i in range(no_of_spaces):
        spaces = spaces + " "

calc_spaces(filetype)


subprocess.call( ["sed","-i",'1s/^/%s/'%spaces,file] )

# echo "0000000: FF D8 FF DB" | xxd -r - anyfile

subprocess.call( ["echo \"00000000: %s\" | xxd -r - %s"%(magic_bytes[filetype][0],file)], shell=True )
