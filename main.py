import sys
import shutil
import time

sys.path.insert(0,'./data')
from playground import PlayGround
from next_state import next_state
from interface import *
from usr_input import *


#function to print either an n-th generation, or all the generations uptil n
def live(P,n,l):
    for i in range(0,n):
        P.next_state()
        if l: 
            P.console_print()
            time.sleep(1)
    if not l:
        P.console_print()


# shot my own leg so I need this for the next function
def conv_to_bool(bl):
    if bl == 'true': return True
    return False

# this goes into the "while run" loop, but we need to be able to actually call this whole process by scripts 
def run_loop(P,insta,instb,rf = False, file = None):
    # (false,b):live(P,b,False)
    # (true,b):live(P,b,True)        
    if insta in ['true', 'false']:
        live(P,instb,conv_to_bool(insta))
        return
    # 'f' inserting a pattern from a file
    if insta == 'f':
        if instb < 1: files = filels('files')
        else: 
            files = filels('files',False)
            if len(files) - 1 < instb: return
            pattern = pattern_from_file('files/'+files[instb])
            y,x = get_size('col','row',P.h,P.w,rf,file)
            if x < 0 or y < 0: return
            insert(P,x,y,pattern)
        return

    # 'i' manual insert through stdin
    if insta == 'i':
        y,x = get_size('col','row',P.h,P.w,rf,file)
        if x < 0 or y < 0: return
        pattern = pattern_from_input(rf,file)
        insert(P,x,y,pattern)
        return

    # 'e' needs to either stop a current process or the program
    if insta == 'e':
        return
    

def main_run():
    # default field initiation
    P = PlayGround(max_h,max_w)
    # you need to be welcomed only once
    welcome_msg()
    run = True
    while run:
        # print basic instruction list
        inst_msg()
        print("command us!:",end=' ')
        # read instructions: there can be max 2 instructions: isntruction a, isnstruction b
        # a defaults to 'false' string, b defaults to 0
        insta, instb = read_inst()
        run_loop(P,insta,instb)

        # 'e' needs to either stop a current process or the program
        if insta == 'e':
            return
                    
        # 'h' just prints the help.txt file to the screen
        if insta == 'h':
            print_help()
            continue

        # basically wipes the playground and let's the user to redefine its size
        # except I've made it limited to 1024, which could be changed in the code
        if insta == 'n':
            h,w = get_size('width','height',max_h,max_w)
            if h < 0 or w < 0: continue
            del P
            P = PlayGround(h,w)
            continue

        # 'd' is for running a demo scritp that doesn't really require inst_msq and so on on the screen
        if insta == 'd':
            if instb < 1: files = filels('demos')# writes out the contents
            else: 
                files = filels('demos',False)
                if len(files) < 1 or len(files)-1 < instb : continue
                D = PlayGround(max_h,max_w)
                with open('demos/'+files[instb],'r') as demo:
                    
                    read_script = True
                    while read_script:
                        a,b = read_inst(True,demo)
                        if a == 'e': break
                        run_loop(D,a,b,True,demo)

if __name__ == '__main__':
    main_run()