#Sudoku Solver (applying constraint programming concepts)
#Description:
#	*Done using ortools library (offered by Google)
#	*Input: text file that has the sudoku (see example file for format)
#	*Outpu: solved sudoku displayed on console

from ortools.sat.python import cp_model

#To read input from text file (using default if no file provided)
def inputSudoku():
	filename = input("Enter file name: ")
	if filename == '':
		filename = 'sudoku_input.txt'
	fp = (open(filename, "r"))
	inp = (fp.read()).split()
	sudoku = []
	for ele in inp:
		if ele != '.':
			sudoku.append(int(ele))
		else:
			sudoku.append(0)
	fp.close()
	return sudoku

#To display the solved sudoku
def displaySolution(solver):
	for i in range(9):
		for j in range(9):
			ind = (chr(i+ord('0')), chr(j+ord('0')))
			print("%i" % solver.Value(globals()['x' + ''.join(ind)]), end = ' ')
		print()

#Getting input
sudoku = inputSudoku()

#Creating variable names using the indices of each cell i.e. [x00, x01, ... , x88]
indices = [(chr(row+ord('0')), chr(col+ord('0'))) for row in range(9) for col in range(9)]
for i in range(81):
	indices[i] = 'x'+''.join(indices[i])

#Creating the CP-SAT model
model = cp_model.CpModel()

#Adding variables to the model using variable names created earlier (each cell is a variable)
for num, ind in zip(sudoku, indices):
	if num == 0:
		globals()[ind] = model.NewIntVar(1, 9, ind)
	else:
		globals()[ind] = model.NewConstant(num)

#NOTE: globals()[<name>] creates dynamic variables


#Creating AllDifferent constraints for rows and columns (no two values in same row or column may be same)
num = 0
for c in range(9):

	rowIndices = [(chr(num+ord('0')), chr(col+ord('0'))) for col in range(9)]
	for i in range(9):
		rowIndices[i] = globals()['x'+''.join(rowIndices[i])]

	model.AddAllDifferent(rowIndices)

	colIndices = [(chr(row+ord('0')), chr(num+ord('0'))) for row in range(9)]
	for i in range(9):
		colIndices[i] = globals()['x'+''.join(colIndices[i])]

	model.AddAllDifferent(colIndices)

	num+=1

#Finally, creating AllDifferent constraints for 3x3 boxes 
rowNum = 0
while(rowNum < 9):
	colNum = 0
	while(colNum < 9):
		boxIndices = [(chr(row+ord('0')), chr(col+ord('0'))) for row in range(rowNum, rowNum+3) for col in range(colNum, colNum+3)]
		for i in range(9):
			boxIndices[i] = globals()['x'+''.join(boxIndices[i])]
		model.AddAllDifferent(boxIndices)

		colNum+=3
	rowNum+=3

#Creating and calling the CpSolver for the variables and constraints created
solver = cp_model.CpSolver()
status = solver.Solve(model)

#Displaying the solution
if status == cp_model.FEASIBLE:
	displaySolution(solver)
