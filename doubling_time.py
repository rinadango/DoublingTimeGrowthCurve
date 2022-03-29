#!/usr/bin/python
"""

@author: Paulina Frolovaite
"""

from tkinter import filedialog
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import os
import tkinter as tk
import sys

root = tk.Tk()
root.withdraw()

print(' !!! IMPORTANT: TIME in the EXCEL file must be in HOURS and first column!!! \nOtherwise, change time format and proceed again.')
enter = input("\nPress ENTER to load file ")    
if enter == '':
    file_path = filedialog.askopenfilename()
else:
    print('WRONG INPUT. EXITING the script!')
    sys.exit(1)
    
time = input("In hours or minutes? (input 'h' or 'm'): ").casefold()

# Read table where the first column is Time (h)
# TIME MUST BE IN HOURS (SINCE THE CELLS TAKE TIME TO GROW)
table = pd.read_excel(file_path)

# file name of import
basename = os.path.basename(file_path)
without_extension = os.path.splitext(basename)[0]
#print(without_extension)

db_t = []
def doubling_time_cell_growth_curve(table, time_format: str):
    
    x_time = table.iloc[:,0].to_numpy()
    #x_time
    cells_y = table.drop(table.columns[0],axis = 1)
    colls = cells_y.columns

    _names = []

    for i in colls:
        
        _names.append(i)
        
        k = cells_y[[i]].to_numpy()
        #print(k)
        
        # y = AeBx
        if time_format == 'm':
            minutes = x_time * 60
            y = np.polyfit(minutes, np.log(k), 1)
            
        elif time_format == 'h':
            y = np.polyfit(x_time, np.log(k), 1)
        
        else:
            print('WRONG INPUT! EXITING the script')
            sys.exit(1)
        
        # B values of every y array
        B_vals = y[0]
        
        # Doubling time calculation
        for b_value in B_vals:
            #print(b_value)
            
            Td = math.log(2)/b_value
            db_t.append(Td)
            print(f'Doubling time for {i}:', Td)
    
    if time_format == 'm':
        plt.plot(minutes, cells_y, label = _names, marker = 'o')
        plt.scatter(cells_y)
        plt.xlabel('Time (mins)')
    else: 
        plt.plot(x_time, cells_y, label = _names, marker = 'o')
        plt.xlabel('Time (h)')
        
    plt.legend(colls)   
    plt.ylabel('Cell count')
    plt.tight_layout()
    plt.savefig(f'{without_extension}_growth_curve.png', dpi = 300)

    print('\nNOTICE: Growth curve plot has been made as .png file')
            
doubling_time_cell_growth_curve(table, time)

aveg_ = int(input("\nDo you want the average (mean) time of your samples? Enter 1 for YES and 0 for NO: "))

if aveg_ == 1:
    print("Average time: ", sum(db_t)/len(db_t))
elif aveg_ == 0:
    print("Average will not be calculated")
    sys.exit(1)
else:
    print('\nWRONG INPUT. EXITING the script!')
    sys.exit(1)
    