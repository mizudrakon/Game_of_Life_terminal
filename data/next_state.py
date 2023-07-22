from playground import PlayGround

# PlayGround function to calculate the next state contain functions:
# ysearch, xsearch - are supposed to skip as much of empty space as possible without doing too many extra calculations
# count_neigh - count the number of live cells in a 9x9 field centered on x,y
# new_value - evaluates the result of count_neigh
# commit - writes the character returned by new_value into the playground, if it's supposed to go there
# row_eval - evaluates a specified row using ysearch, xsearch, count_neigh, new_value, writing the resuls into a cache field
# write_row - when appropriate writes a specified cache field into the playground
# flow() - just encapsulates the final puzzle, it could be called main()

def next_state(self):
    #searchy returns the first row index where the next row is non-empty
    def ysearch(index,limit):
        i = index
        while self.R[self.nextr(i)] == 0:
            if i == limit: return i
            i = self.nextr(i)
        return i

    #this will be called when (x,y) is in empty space == 3x3 square are all '0'
    #the purpose is to look at the next column of 3 on the right and just go on until wi hit something
    #we want to skip checking all 6 positions multiple times
    #the returned walue is an x coordinate that needs to be checked
    def xsearch(y,x):
        x = self.nextc(x)
        n = self.nextc(x)
        u = self.prevr(y)
        c = y
        d = self.nextr(y)
        while self.PG[u][n] + self.PG[c][n] + self.PG[d][n] == '000':
            if x == self.w: #we don't need to go beyond the width
                return x
            x = n #we're just going through the line with x
            n = self.nextc(x)
        return x

    #counts alive cells in the neighbourhood
    def count_neigh(y, x):
        sum = 0
        for r in [self.prevr(y), y, self.nextr(y)]:
            for c in [self.prevc(x), x, self.nextc(x)]:
                if self.PG[r][c] != '0': sum += 1
        return sum

    #evaluates the sum from count_neigh to decide what to do with it

    def new_value(sum):
        if sum == 3: return '1'
        if sum == 4: return 'x'
        else: return '0'


    #we need to compare our CF field values with the ones in PG to know if we're changing them
    #we also want to fix R (row) field that remembers if the row is empty
    def commit(ch, x,y):
        #dead cell comes to life
        if ch == '1' and self.PG[y][x] == '0':
            self.PG[y][x] = '1'
            self.R[y] += 1
            self.C[x] += 1
            return
        #normal cell dies
        if ch == '0' and self.PG[y][x] == '1':
            self.PG[y][x] = '0'
            self.R[y] -= 1
            self.C[x] -= 1
            return
        #immortal cell just does it's own thing
        if ch == '0' and self.PG[y][x] in ['I','i']:
            return
        #multi-generation cell gets closer to life
        if ch == '0' and self.PG[y][x] != '0':
            #sadly, we need to convert it to an int first, since it can be > 9
            num = 0
            for n in self.PG[y][x]:
                num += 10*num + (ord(n)-ord('0'))
            num -= 1
            self.PG[y][x] = chr(num + ord('0'))



    #row = the evaluated row, field = the array used to cache the results, start_index = the first index in the cache field
    def row_eval(row,field,start_index):
        i = 0 #index for moving through the evaluated PG row
        while i <= self.w: #we start checking in 0
            sum = count_neigh(row,i)
            if i < self.w and sum == 0:
                #stats in a 0 sum neighbourhood, stops when we hit the first live cell
                i = xsearch(row,i)
                #print(i)
                continue
            field[i+start_index] = new_value(sum)
            i += 1
        return field

    #row = the evaluated row, field = the array used to cache the results, start_index = the first index in the cache field
    def write_row(row, field, start_index):
        for i in range(0,self.w+1): #PG is changed into according to the field of changes used
            if field[i+start_index] != 'x':#no change needed marked by 'x'
                commit(field[i+start_index],i,row)#change in PG, R
                field[i+start_index] = 'x'#field of changes gets wiped


    #main body of the function
    def flow():
        #first row - evaluate first, write last cash field
        first_row = ['x' for i in range(self.w+1)]
        first_index = 0
        last = self.prevr(first_index)#for first_index = 0 last = h
        #assistant cash field of the two rows' length
        CF = ['x' for i in range(2*self.w+2)]
        cf0 = 0

        def cf0_change():
            #there are only 2 possibilities: 0 or w+1
            if cf0 == 0: return self.w + 1
            return 0
            #we evaluate the first row, but don't write it yet

        first_row = row_eval(first_index,first_row,0)
        #print(first_row[0:self.w+1])
        #jump to the second row
        r = first_index+1

        notEnd = True
        while notEnd:
            #we need to find the first row that needs to be evaluated (can be the current one)
            if self.R[r] == 0:
                r = ysearch(r,last)#searches until the last row or until a non-empty row - 1
                if r == last: notEnd = False#if it's the last row, we still need to evaluate it
            hit = True
            #unless we just looped through the whole PG, we're right next to a nonepty line,
            #and the current line needs to be evaluated

            #we need to start the cycle of evaluating and writing untill we hit an empty space 0,0 -> hit = false
            second = False
            while hit:
                CF = row_eval(r,CF,cf0)
                if self.R[r] + self.R[self.nextr(r)] == 0 or r == last:
                    hit = False #the row is currently empty, but we need to evaluate it because of the previous one
                    #so we don't stop the iteration of the cycle

                #CF is cyclic, after evaluating, we change the start index cf0 for the next row
                #BUT that is also the previous row that is already evaluated, and we need to use it to rewrite PG[r-1]
                cf0 = cf0_change()
                if second:#for the first evaluated row in the encountered pattern, we wait
                    write_row(self.prevr(r),CF,cf0)
                r = self.nextr(r)
                second = True #first loop will be second = false, the subsequent ones true
            if second:#if the loop happened, second = true, and we need to write the last evaluated row
                cf0 = cf0_change()
                write_row(self.prevr(r),CF,cf0)

        #at this point we have to be at the first row again, and the last row is evaluated and written into PG
        # we need to overwrite the first row in PG with the cashed one
        write_row(first_index,first_row,0)
        #thus the whole PG should be at the next state of being
    #end of flow()
    flow()
#end of next_state()

PlayGround.next_state = next_state
