import datetime as dt


file = open(r'C:\Users\16099\Documents\AOC_21\aoc15_risk_path.txt')
by = file.read()

text_lines = by.split("\n")

class Node:

    def __init__(self):

        self.risk = 0
        self.lowest_path_risk = 10**5


class Grid:

    def __init__(self, rows, cols):
        self.cols = cols
        self.rows = rows

        self._grid = [[Node() for _ in range(cols)] for _ in range(rows)]

    def get_lowest_path_risk(self,row,col):
        return self._grid[row][col].lowest_path_risk

    def get_node_risk(self, row, col):
        return self._grid[row][col].risk

    def find_lowest_path_risk(self,row,col):
        adj_explored_nodes = self.get_adj_nodes(row,col)

        node_risk = self.get_node_risk(row,col)

        risk_lowered = False

        for adj_node in adj_explored_nodes:
            adj_node_row = adj_node[0]
            adj_node_col = adj_node[1]
            adj_node_risk = self.get_lowest_path_risk(adj_node_row, adj_node_col)

            current_path_risk = self.get_lowest_path_risk(row,col)
            
            if adj_node_risk + node_risk < current_path_risk:
                risk_lowered = True
                self.set_lowest_path_risk(row,col,adj_node_risk + node_risk)

        if risk_lowered:
            return self.get_adj_nodes(row,col)
        else:
            return []
                

    def set_node_risk(self,row,col,risk):
        self._grid[row][col].risk = risk

    def set_lowest_path_risk(self,row,col,risk):
        self._grid[row][col].lowest_path_risk = risk

    def set_queued(self, row, col):
        self._grid[row][col].queued = True

    def get_adj_nodes(self,row,col):
        node_list = []

        # left and up
        
        if row != 0 and col != 0:
            node_list.append((row-1,col))
            node_list.append((row,col-1))
        if row == 0 and col != 0:
            node_list.append((row,col-1))
        if row != 0 and col == 0:
            node_list.append((row-1,col))

        # right and down

        if row != self.rows - 1 and col != self.cols - 1:
            node_list.append((row+1,col))
            node_list.append((row,col+1))

        if row == self.rows - 1 and col != self.cols - 1:
            node_list.append((row,col+1))
 
        if row != self.rows - 1 and col == self.cols - 1:
            node_list.append((row+1,col))

        return node_list
        
    
grid = Grid(len(text_lines), len(text_lines[0]))

for row_index, line in enumerate(text_lines):
    for col_index, risk in enumerate(line):
        grid.set_node_risk(row_index,col_index,int(risk))

grid.set_node_risk(0,0,0)
grid.set_lowest_path_risk(0,0,0)

# the indices are (row, col)
node_queue = [(0,1),(1,0)]

while node_queue != []:

    explore_cell = node_queue.pop(0)
    
    adj_cells_if_lowered = grid.find_lowest_path_risk(row = explore_cell[0],col = explore_cell[1])

    for node_indices in adj_cells_if_lowered:

        node_queue.append(node_indices)
    



    
        
