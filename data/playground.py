# PlayGround definition and some basic functions:
# functions for cycling through a looped field
# printpg - prints the playground with attached arrays for counting live cells
# console_print - can print a specified slice of the looped field
# insert - inserts a pattern into the playground
import shutil
from interface import allowed_printsize
class PlayGround:
    def __init__(self,w,h):
        self.h,self.w = h,w
    #playground (field), h - height, w - width
        self.PG = [['0' for i in range(w+1)] for j in range(h+1)]
        self.R = [0 for i in range(h+1)]
        self.C = [0 for i in range(w+1)]
        #array C is mostly useful for printing to the console. We want to calculate the largest gap in the playgorund

    #cycling functions probably useful for both inserting and writing out
    #previous row (vertical index)
    def prevr(self,index):
        if index == 0: return self.h
        return index - 1

    #previous column (horizontal index)
    def prevc(self,index):
        if index == 0: return self.w
        return index - 1

    #next row
    def nextr(self,index):
        if index == self.h: return 0
        return index + 1

    #next column
    def nextc(self,index):
        if index == self.w: return 0
        return index + 1

    #basic print field showing R and C arrays on the sides - mostly for debugging
    def printpg(self):
        print(' ', end = ' ')
        for i in range(0,self.h+1):
            print(self.C[i], end = ' ')
        print()

        for r in range(0,self.h+1):
            print(self.R[r], end = ' ')
            for c in range(0,self.w+1):
                if self.PG[r][c] != '0': print(self.PG[r][c], end = ' ')
                else: print('-', end = ' ')
            print()

    # looking for a largest gap in rows or columns of the playground using arrays R and C
    def get_gap(self,array,border):
        s,e = 0,border 
        # we start at 0
        i = 0
        # there is a possibility that we're in the middle of the largest gap, so we save separate values for it
        s0 = -1
        e0 = 0
        l0 = 0
        # this matters if array[0] is 0 and we have to measure the rest of the gap here
        if array[0] == 0:
            s0 = 0
            while e0 < border + 1 and array[e0] == 0: 
                e0 += 1
            e0 -= 1
            l0 = e0
        if e0 == border: return (s,e,l0)
        # we have the initial maybe-half gap, now we continue until the end
        i = e0+1
        m = 0
        while i < border + 1:
            l = 0
            while array[i] != 0:
                if i == border: return (e,s,l)
                i += 1
                if array[i] == 0 and i < border and array[i+1] != 0: i += 1 # we're not really interested in one unit gaps
            si = i #start of A gap
            while i < border + 1 and array[i] == 0:
                i += 1
            l = i - si
            # we hit the border and we had a 0 at s0, so we need to add the l0 gap to this one
            if i - 1 == border and s0 == 0:
                l += l0
                if m <= l: # and return it, if it is the largest one
                    s = si
                    e = e0
                    return (e,s,l)
            if m < l: # we compare the sizes and rewrite the variables if appropriate
                m = l
                s = si
                e = i - 1
        return (e,s,l)

    #there were issues when get_gap() called on its own
    def row_gap(self):
        return self.get_gap(self.R,self.h)

    def col_gap(self):
        return self.get_gap(self.C,self.w)    


    # printing function intended for output
    # the playground is looped, so we want to print a different slice of it than the default
    # 
    def console_print(self,ys = 0,ye = -1 ,xs = 0,xe = -1):
        # allowed_printsize depends on the console
        h,w = allowed_printsize()
        # we could print more lines then the console height, but it might not be so convenient
        if ye == -1:
            ys,ye,yl = self.row_gap()
            # initial yl is the size of the gap = the largest 000 area 
            # we want the size of the complement = playground width - gap
            yl = self.h - yl
            if yl == 0 or yl == self.h:
                ys,ye = 0,h
            while yl > h:
                ye = self.prevr(ye)
                yl -= 1
        # we cannot really print a field that is larger than the terminal width, so we shrink it
        if xe == -1:
            xs,xe,xl = self.col_gap()
            xl = self.w - xl
            if xl == 0 or xl == self.w:
                xs,xe = 0,w
            while xl > w:
                xe = self.prevc(xe)
                xl -= 1
        
        # print info about where we're starting
        print(f"start row, col: {ys}, {xs}")
        # function to give us '-' instead of '0'
        def symbol(ch):
            if ch == '0': return '-'
            return ch
        
        # the main printing:
        while ys != ye:
            i = xs
            while i != xe:
                print(symbol(self.PG[ys][i]), end = ' ')
                i = self.nextc(i)
            print(symbol(self.PG[ys][xe]))
            ys = self.nextr(ys)
        i = xs
        while i != xe:
            print(symbol(self.PG[ye][i]), end = ' ')
            i = self.nextc(i)
        print(symbol(self.PG[ye][xe]))

        # print info about where we're ending and an empty line
        print(f"end row, col: {ye}, {xe}")
        print()
