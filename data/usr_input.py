


# all sorts of allowed instructions
newi = ['n','N','new','NEW']
numi = ['-l','l', 'list'] # -l for people used to midifiers
inserti = ['i', 'I', 'insert']
filei = ['f','F','file','FILE']
demoi = ['d','D','demo','DEMO']
endi = ['e','E','end','END','q','Q','quit','QUIT']
helpi = ['h','H','help','HELP']
instructions = newi + numi + inserti + filei + demoi + endi + helpi 


# allowed for insert
allowed = [chr(i) for i in range(ord('0'),ord('9')+1)] + ['i', 'I']
stop = ['e','E']
newl = ['n','N']

# maximal allowed size of the palyfield
max_h = 1024
max_w = 1024

def pattern_from_file(file):
    pattern = []
    with open(file,'r') as f:
        for line in f:
            L = [c.strip() for c in line.split()]
            pattern.append(L)
    return pattern

# reads a pattern from standard input or an open file (script)
def pattern_from_input(read_file = False,file = None):
    pattern = []
    while True:
        if read_file:
            I = [i.strip() for i in file.readline()]
        else: I = [i.strip() for i in input()]
        if I == []: return pattern
        for i in I:
            if i in stop: return pattern
            #if i in allowed + newl:
            pattern += i


#inserts a pattern into the field according to the rules:
#'0' = dead cell, '1' - '9' = cell that lives given number of generations
#'i','I' = immortal cell
#'n','N' = new line, 'e','E' = end of the pattern
def insert(P,x0,y0,pattern):
    x = x0 #start column coordinate
    y = y0 #start row coordinate
    for r in pattern:
        for c in r:
            if c in stop: break
            if c in newl: 
                y = P.nextr(y)
                x = x0
                continue
            if c in allowed:
                #marking non-empty rows and first and last index
                if c != '0' and P.PG[y][x] == '0':
                    P.R[y] += 1
                    P.C[x] += 1
                elif c == '0' and P.PG[y][x] != '0':
                    P.R[y] -= 1
                    P.C[x] -= 1
                P.PG[y][x] = c
            x = P.nextc(x)
        if c in stop: break



# to get user defined size of the field
def get_size(y,x,hm,wm,file_read = False,file = None):
    end = False
    def get_num():
        r = 0
        # if we're running a script from inside the program, we need to read from the file
        if file_read: i = file.readline().strip()
        else: i = input().strip()
        if i in stop: 
            end = True
            return 0
        try:
            h = int(i)
            return h
        except:
            print("not an integer")
        return 0
    h = -1
    while h < 0 and end == False:
        if file_read == False:
            print(f"{y} (0-{hm}):", end=' ')
        h = get_num()
    w = -1
    while w < 0 and end == False:
        if file_read == False:
            print(f"{x} (0-{wm}):", end=' ')
        w = get_num()
    return (h,w)
    # having the result (-1,-1) would mean failure to get height and width, because the user wanted to stop


# this is mostly to filter out nonsense and streamline user input
# since "user don't follow no made up rules"
# basicaly a switch statemnet
def read_inst(read_file = False, file = None):
    # default output that should pretty much just print the current state of the field
    a,b = 'false',0
    def streamline(c):
        if c in endi: return 'e'
        if c in helpi: return 'h'
        if c in newi: return 'n'
        if c in inserti: return 'i'
        if c in filei: return 'f'
        if c in demoi: return 'd'
        if c in numi: return 'true'
        return 'false'
    n = -1
    # we might need to read from a file
    if read_file:
        I = [i.strip() for i in file.readline().split()]
    else: I = [i.strip() for i in input().split()]
    if len(I) == 0: 
        return (a,b)
    if len(I) > 1: l = 2
    else: l = 1
    for i in range(l):
        # check if it's a number
        try:
            n = int(I[i])
        except ValueError:
            n = -1
        # number is stored in the second variable
        if n >= 0:
            b = n
            continue
        a = streamline(I[i])
    return (a,b)
