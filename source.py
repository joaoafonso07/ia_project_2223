        for row in range(board_size):
            for col in range(board_size):
                piece = board.grid[row][col]
                if piece == 'C':
                    boats['boat1'] -= 1
                    if row == 0:
                        if col == 0:
                            board.grid[row+1][col] = 'W'
                            board.grid[row][col+1] = 'W'
                            board.grid[row+1][col+1] = 'W'
                        elif col == 9:
                            board.grid[row+1][col] = 'W'
                            board.grid[row][col-1] = 'W'
                            board.grid[row+1][col-1] = 'W'
                        else:
                            board.grid[row][col-1] = 'W'
                            board.grid[row][col+1] = 'W'
                            board.grid[row+1][col] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row+1][col+1] = 'W'
                    elif row == 9:
                        if col == 0:
                            board.grid[row-1][col] = 'W'
                            board.grid[row][col+1] = 'W'
                            board.grid[row-1][col+1] = 'W'
                        elif col == 9:
                            board.grid[row-1][col] = 'W'
                            board.grid[row][col-1] = 'W'
                            board.grid[row-1][col-1] = 'W'
                        else:
                            board.grid[row][col-1] = 'W'
                            board.grid[row][col+1] = 'W'
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row-1][col+1] = 'W'
                    else:
                        if col == 0:
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row][col+1] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row+1][col] = 'W'
                        elif col == 9:
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row][col-1] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row+1][col] = 'W'
                        else:
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row][col-1] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row+1][col] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row][col+1] = 'W'
                            board.grid[row-1][col+1] = 'W'

                elif piece == 'T':
                    if row == 0:
                        if col == 0:
                            board.grid[row][col+1] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row+2][col+1] = 'W'
                        elif col == 9:
                            board.grid[row][col-1] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row+2][col-1] = 'W'
                        else:
                            board.grid[row][col-1] = 'W'
                            board.grid[row][col+1] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row+2][col-1] = 'W'
                            board.grid[row+2][col+1] = 'W'
                    elif row == 8:
                        if col == 0:
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row][col+1] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row+1][col] = 'B'
                            boats['boat2'] -= 1
                            
                        elif col == 9:
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row][col-1] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row+1][col] = 'B'
                            boats['boat2'] -= 1
                        else:
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row][col-1] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row][col+1] = 'W'
                            board.grid[row+1][col] = 'B'
                            boats['boat2'] -= 1
                    elif row == 9:
                        return None
                    else:
                        if col == 0:
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row][col+1] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row+2][col+1] = 'W'
                        elif col == 9:
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row][col-1] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row+2][col-1] = 'W'
                        else:
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row][col-1] = 'W'
                            board.grid[row][col+1] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row+2][col-1] = 'W'
                            board.grid[row+2][col+1] = 'W'

                elif piece == 'B':
                    if row == 0:
                        return None
                    elif row == 1:
                        if col == 0:
                            board.grid[row+1][col] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row][col+1] = 'W'
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row-1][col] = 'T'
                            boats['boat2'] -= 1
                            
                        elif col == 9:
                            board.grid[row+1][col] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row][col-1] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row-1][col] = 'T'
                            boats['boat2'] -= 1
                        else:
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row+1][col] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row][col-1] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row][col+1] = 'W'
                            board.grid[row-1][col] = 'T'
                            boats['boat2'] -= 1

                    elif row == 9:
                        if col == 0:
                            board.grid[row][col+1] = 'W'
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row-2][col+1] = 'W'
                        elif col == 9:
                            board.grid[row][col-1] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row-2][col-1] = 'W'
                        else:
                            board.grid[row][col-1] = 'W'
                            board.grid[row][col+1] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row-2][col-1] = 'W'
                            board.grid[row-2][col+1] = 'W'                       
                    else:
                        if col == 0:
                            board.grid[row+1][col] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row][col+1] = 'W'
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row-2][col+1] = 'W'
                        elif col == 9:
                            board.grid[row+1][col] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row][col-1] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row-2][col-1] = 'W'
                        else:
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row+1][col] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row][col-1] = 'W'
                            board.grid[row][col+1] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row-2][col-1] = 'W'
                            board.grid[row-2][col+1] = 'W'

                elif piece == 'L':
                    if col == 0:
                        if row == 0:
                            board.grid[row+1][col] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row+1][col+2] = 'W'
                        elif row == 9:
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row-1][col+2] = 'W'
                        else:
                            board.grid[row-1][col] = 'W'
                            board.grid[row+1][col] = 'W'
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row-1][col+2] = 'W'
                            board.grid[row+1][col+2] = 'W'
                    elif col == 8:
                        if row == 0:
                            board.grid[row][col-1] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row+1][col] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row][col+1] = 'R'
                            boats['boat2'] -= 1
                            
                        elif row == 9:
                            board.grid[row][col-1] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row][col+1] = 'R'
                            boats['boat2'] -= 1
                        else:
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row][col-1] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row+1][col] = 'W'
                            board.grid[row][col+1] = 'R'
                            boats['boat2'] -= 1
                    elif col == 9:
                        return None
                    else:
                        if row == 0:
                            board.grid[row][col-1] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row+1][col] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row+1[col+2]] = 'W'
                        elif row == 9:
                            board.grid[row][col-1] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row-1][col+2] = 'W'
                        else:
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row][col-1] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row-1][col] = 'W'
                            board.grid[row+1][col] = 'W'
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row-1][col+2] = 'W'
                            board.grid[row+1][col+2] = 'W'

                elif piece == 'R':
                    if col == 0:
                        return None
                    
                    elif col == 1:
                        if row == 0:
                            board.grid[row][col+1] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row+1][col] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row][col-1] = 'L'
                            boats['boat2'] -= 1
                            
                        elif row == 9:
                            board.grid[row][col+1] = 'W'
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row][col-1] = 'L'
                            boats['boat2'] -= 1
                        else:
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row][col+1] = 'W'
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row+1][col] = 'W'
                            board.grid[row][col-1] = 'R'

                    if col == 9:
                        if row == 0:
                            board.grid[row+1][col] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row+1][col-2] = 'W'
                        elif row == 9:
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row-1][col-2] = 'W'
                        else:
                            board.grid[row-1][col] = 'W'
                            board.grid[row+1][col] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row-1][col-2] = 'W'
                            board.grid[row+1][col-2] = 'W'  
                            boats['boat2'] -= 1
                    
                    else:
                        if row == 0:
                            board.grid[row][col+1] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row+1][col] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row+1[col-2]] = 'W'
                        elif row == 9:
                            board.grid[row][col+1] = 'W'
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row-1][col-2] = 'W'
                        else:
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row][col+1] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row-1][col] = 'W'
                            board.grid[row+1][col] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row-1][col-2] = 'W'
                            board.grid[row+1][col-2] = 'W'    

                elif piece == 'M':
                    if row == 0:
                        if col == 0 or col == 9:
                            return None  
                        elif col == 1:
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row+1][col] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row][col-1] = 'L'
                        elif col == 8:
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row+1][col] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row][col+1] = 'R'
                        else:
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row+1][col] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row+1][col-2] = 'W'
                            board.grid[row+1][col+2] = 'W'
                            
                        #NOT FINISHED [DOWN]

                    elif row == 1:
                        if col == 0:
                            return None
                            
                        elif col == 9:
                            return None
                        else:
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row+1][col] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row][col-1] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row][col+1] = 'W'
                            board.grid[row-1][col] = 'T'
                            boats['boat2'] -= 1

                    elif row == 8:
                        if col == 0:
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row][col+1] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row+1][col] = 'B'
                            boats['boat2'] -= 1
                            
                        elif col == 9:
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row][col-1] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row+1][col] = 'B'
                            boats['boat2'] -= 1
                        else:
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row][col-1] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row][col+1] = 'W'
                            board.grid[row+1][col] = 'B'
                            boats['boat2'] -= 1
                    elif row == 9:
                        return None
                    else:
                        if col == 0:
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row][col+1] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row+2][col+1] = 'W'
                        elif col == 9:
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row][col-1] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row+2][col-1] = 'W'
                        else:
                            board.grid[row-1][col-1] = 'W'
                            board.grid[row-1][col] = 'W'
                            board.grid[row-1][col+1] = 'W'
                            board.grid[row][col-1] = 'W'
                            board.grid[row][col+1] = 'W'
                            board.grid[row+1][col-1] = 'W'
                            board.grid[row+1][col+1] = 'W'
                            board.grid[row+2][col-1] = 'W'
                            board.grid[row+2][col+1] = 'W'   