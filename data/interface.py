import os
import shutil

# there will be an initial 1024x1024 field
welcome = "Welcome to the GGS!\nDefault field size 1024x1024\n"
def welcome_msg():
    print(welcome)

# nobody remembers the controlls -> remind them at every opportunity
insts ="\nint - num generations, N - new field, I - insert, F - file,\nD - demo, E - end program, H - help\n"
def inst_msg():
    print(insts)

# gets the max size of the field that fits the terminal window, considering the way it is written out (spaces)
def allowed_printsize():
    s = shutil.get_terminal_size()
    h = s[1] 
    w = s[0]//2
    return (h,w)

# prints the help file
def print_help():
    print()
    with open('help.txt','r') as hf:
        for line in hf:
            print(line, end='')
    print()

filef = 'files'
demof = 'demos'
# writes out contents of a folder, but also makes a list of files that can be used immediately
def filels(folder,show = True):
    lsfiles = os.listdir(folder)
    files = ['..']
    files += [f for f in lsfiles if len(f) > 3 and f[len(f)-3:] == "txt"]
    if show:
        for i in range(1,len(files)):
            print(f"{i} - {files[i]}")
    print()
    return files