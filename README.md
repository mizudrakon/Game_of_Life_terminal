### Welcome to GGS (Glorified Glider Simulator)!

!!!!Run the program as python main.py!!!!

   * For instructions to control the program please read the 'help.txt' file (or
input 'h' or 'help' after the GGS prompt)

GGS is a text based Conway's Game of Life alternative that allows you to do basicly everything traditional Game of Life does:   
1. insert a pattern of life cells into a two dimensional field;
2. watch it evolve in accordance with a few basic rules:   
    2. 1. For a space that is 'populated':  
	     1. Each cell with one or no neighbors dies, as if by solitude.   
		 2. Each cell with four or more neighbors dies, as if by overpopulation.   
		 3. Each cell with two or three neighbors survives.   
	2. 2. For a space that is 'empty' or 'unpopulated'   
		 1. Each cell with three neighbors becomes populated.   

GGS works exactly alike for any patterns of 1s and 0s, but also allows
insertion of cells with greater survivability (up to nine generations) and cells that are immortal, so you can see how unbalanced the whole thing becomes with such nonsense.   

It uses algorithm that chacks every cell in spcified boundaries by counting live cells in a square of 9 with the cell as its center:   
1. For exactly 3 living cells, the central one lives whatever its current state;
2. For exactly 4, the central one keeps its current state;
3. For any other number the centeral dies or stays dead.

This playfield is looped, so patternes can migrate over the edges to opposite
ends of the field. The default size of the field is 1024x1024 and I set it as
the limit in the usr_input.py file (might change it later).   

evaluating the next state:   
	When evaluating the next state in the next_state function, there are two
arrays that count live cells in each row and column. The row_eval() function
is moved to the nearest following row that need to be evaluated, ignoring all
the empty ones.   
	 Then the xsearch() function looks for the first live cell in
the previous, current and the next row, because they can affect how the
current row cells evolve, the count_neigh() function and the subsequent
cashing is done only when the xsearch encounteres a live cell.   
	The new states are cashed into an array that gets written into the main
playfield only after the next row is also evaluated.   
	Since the playfield is looped, there must be a singe starting row that gets
evaluated first, but written in only after the rest of the playfiled is
finished.   

writing to the console:   
	We are using the extra arrays that count live cells in rows and
columns for calculating the largest gap in the playfield. The
console_print() is designed to use this information and skip the gap.   
	Another thing that needs to be considered is the size of the terminal
(console) window and how many characters fit there. We get these numbers from
shutil.get_terminal_size() and use this to limit how much of the area we
actually print. Hopefully it works on both Linux and Windows as with the
python os module that is used to load the files and demos.   

files and demos:   
	You can write patterns as txt files and insert them into the
playground by typing 'f n' where 'n' is the number of the desired file. You
can see the numbered list of files after inputing 'f' after the 'command us!:'
prompt.   
	Demos on the other hand are more like scripts that can be loaded and
left to run on their own. You need to create them using the commands and
pattern input rules, and put them in the 'demo' folder (as txt files).   

user instructions:
* write 'e' or 'E' to stop the program (mark the end of pattern input in part 3.)
0. command us!: specify what you want to do and press Enter
  available commands:   
    | op | modifier | explanation |
    |----|----------|---------|
	|(nothing)||-prints the current state on the playground|
	||integer|-returns the playground in the n-th generation from now|
	|-l |integer|-prints every step on the way|
	|i	|	|-insert a pattern as described below (1.,2.)|
	|f	|	|-lists the content of the 'files' folder|
	|f  |integer|-number specifies file that contains a pattern we want to insert, we'll have to specify (1.)|
	|d  |integer|-same as with files, demos are scripts that run in their entirety|
	|h	|	|-prints help|
	|e	|	|-stops the program (or ends pattern insertion)|


1. specify first row and column of your pattern input:   
  col (1-512): 10   
  row (1-512): 10   

2. pattern input:   
  0     -dead cell   
  x,X    -no change   
  1,2,3,4,5,6,7,8,9    -live cell (number of generation cell can survive on its own)   
  i,I    -immortal cell   
  n,N    -mark the end of row   
  e,E    -mark the end of pattern (and press ENTER) every other symbol is meaningless   
  
	i.e.:   
    	0 1 n   
		0 0 1 n   
		1 1 1 e   
	to make a glider :)   
	(there have to be spaces)   

If you want to stop the program, the best bet is to write 'e', 'E' or 'quit' as current input.
During insertion (2.), writing 'e' will mark the end of the pattern input
procedure and continues the program, but everywhere else it stops it entirely.
