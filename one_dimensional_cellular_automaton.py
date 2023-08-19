# One dimensional cellular automaton
import copy

import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import tkinter as tk


def change_rule_num(value):
    global rule_number, rule_number_bin_str, r, rule, label_rule
    rule_number = int(value)
    rule_number_bin_str = format(rule_number, '08b')
    r = rule_number_bin_str
    rule = "111:" + r[0] + ", 110:" + r[1] + ", 101:" + r[2] + ", 100:" + r[3] \
           + ", 011:" + r[4] + ", 010:" + r[5] + ", 001:" + r[6] + ", 000:" + r[7]
    # print(rule)
    label_rule["text"] = rule
    ax.set_title("One dimensional cellular automaton (Rule number:" + str(rule_number) + ")")
    clear_cells()
    initialize_cells0()


def boundary_row(n):    # Boundary condition
    if n >= row:
        return 0
    elif n < 0:
        return row - 1
    else:
        return n


def boundary_col(n):    # Boundary condition
    if n >= col:
        return 0
    elif n < 0:
        return col - 1
    else:
        return n


def eval_neighbours(cl):
    global cells0, row_current, rule_number_bin_str
    # result = 0
    cell_left = cells0[row_current][boundary_row(cl - 1)]
    cell_self = cells0[row_current][cl]
    cell_right = cells0[row_current][boundary_row(cl + 1)]
    pattern = str(int(cell_left)) + str(int(cell_self)) + str(int(cell_right))
    # print(pattern)
    if pattern == "111":
        result = int(rule_number_bin_str[0])
    elif pattern == "110":
        result = int(rule_number_bin_str[1])
    elif pattern == "101":
        result = int(rule_number_bin_str[2])
    elif pattern == "100":
        result = int(rule_number_bin_str[3])
    elif pattern == "011":
        result = int(rule_number_bin_str[4])
    elif pattern == "010":
        result = int(rule_number_bin_str[5])
    elif pattern == "001":
        result = int(rule_number_bin_str[6])
    elif pattern == "000":
        result = int(rule_number_bin_str[7])
    else:
        result = 9
    return int(result)


def next_generation():
    global cells0, row_current, rule_number, is_play
    # print(current_row)
    for j in range(col):
        result = eval_neighbours(j)
        cells0[boundary_row(row_current + 1)][j] = result
    row_current += 1
    if row_current > row - 1:
        row_current = 0
        if is_auto:
            rule_number += 1
            if rule_number > 255:
                rule_number = 0
            change_rule_num(rule_number)
            var_rn.set(rule_number)
            is_play = True


def clear_cells():
    global cells0, cnt, row_current, is_play, cnt
    for i in range(row):
        for j in range(col):
            cells0[i][j] = 0
    cnt = 0
    tx_step.set_text("Step=" + str(cnt))
    draw_cell()
    current_row = 0
    is_play = False
    cnt = 0


def randomize_cells0():
    global cells0, row_current
    for j in range(col):
        cells0[0][j] = random.randint(0, 1)
    draw_cell()
    current_row = 0


def initialize_cells0():
    global cells0, row_current
    cells0[0][row // 2] = 1
    current_row = 0


def draw_cell():
    global cells0, x, y, scat, s
    # For adjustment maker size
    bbox = fig.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    width = bbox.width * fig.dpi
    height = bbox.height * fig.dpi
    # print((width, height))
    x_size = width / (x_max - x_min)
    # print(x_size)
    # draw cells
    x.clear()
    y.clear()
    s.clear()
    for i in range(row):
        for j in range(col):
            if cells0[i][j] == 1:
                y.append(i + cells_offset)
                x.append(j + cells_offset)
                s.append(x_size ** 2 * 0.04)
    scat.set_offsets(np.column_stack([x, y]))
    scat.set_sizes(s)


def mouse_motion(event):
    global cells0
    if event.dblclick == 1:
        # print("double click")
        pass
    elif event.button == 1:
        # print("left click")
        # print(event.xdata, event.ydata)
        if str(event.xdata) != "None" and str(event.ydata) != "None":
            mouse_col = int(event.xdata)
            mouse_row = int(event.ydata)
            # print(mouse_col, mouse_row)
            if mouse_row == 0:
                if cells0[mouse_row][mouse_col] == 0:
                    cells0[mouse_row][mouse_col] = 1
                else:
                    cells0[mouse_row][mouse_col] = 0
            draw_cell()
    elif event.button == 3:
        # print("right click")
        pass


def on_change_window(e):
    if not is_play:
        draw_cell()


def switch_auto():
    global is_auto, is_play
    if is_auto:
        is_auto = False
    else:
        is_auto = True
        change_rule_num(0)
        var_rn.set(rule_number)
        is_play = True


def switch():
    global is_play
    if is_play:
        is_play = False
    else:
        is_play = True


def update(f):
    global cells0, x, y, scat, tx_step, cnt
    if is_play:
        tx_step.set_text("Step=" + str(cnt))
        cnt += 1
        # evaluate cells
        next_generation()
        # Draw cells
        draw_cell()


# Global variables
x_min = 0.
x_max = 80.
y_min = 0
y_max = 80

row = 80
col = 80
cells0 = np.zeros((row, col))   # Cells plane

cells_offset = 0.5   # Offset in plt.scatter

is_play = False
is_auto = False
cnt = 0

row_current = 0

rule_number = int(30)
rule_number_bin_str = format(rule_number, '08b')
r = rule_number_bin_str
rule = "111:" + r[0] + ", 110:" + r[1] + ", 101:" + r[2] + ", 100:" + r[3]\
       + ", 011:" + r[4] + ", 010:" + r[5] + ", 001:" + r[6] + ", 000:" + r[7]

# Set initial live cells
initialize_cells0()

# Generate figure and axes
fig = Figure()
ax = fig.add_subplot(111)
ax.set_title("One dimensional cellular automaton (Rule number:" + str(rule_number) + ")")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_aspect("equal")
ax.grid()
ax.invert_yaxis()

# Generate items
x = []
y = []
s = []  # maker size
scat = ax.scatter(x, y, marker='s', s=6)
tx_step = ax.text(x_min, y_max * 0.05, "Step=" + str(0))
draw_cell()

# Tkinter
root = tk.Tk()
root.title("One dimensional cellular automaton")
canvas = FigureCanvasTkAgg(fig, root)
canvas.get_tk_widget().pack(expand=True, fill='both')
canvas.mpl_connect('button_press_event', mouse_motion)

toolbar = NavigationToolbar2Tk(canvas, root)
canvas.get_tk_widget().pack()

# Play and pause button
btn_pp = tk.Button(root, text="Play/Pause", command=switch)
btn_pp.pack(side='left')

# Random button
btn_clr = tk.Button(root, text="Random", command=randomize_cells0)
btn_clr.pack(side='left')

# Clear button
btn_clr = tk.Button(root, text="Clear", command=clear_cells)
btn_clr.pack(side='left')

# Auto Play button
btn_at = tk.Button(root, text="Auto", command=switch_auto)
btn_at.pack(side='left')

# Role number
label_rn = tk.Label(root, text="Rule number:")
label_rn.pack(side='left')
var_rn = tk.IntVar(root)  # variable for spinbox-value
var_rn.set(rule_number)  # Initial value
s_n = tk.Spinbox(
    root, textvariable=var_rn, from_=0, to=255, increment=1,
    command=lambda: change_rule_num(var_rn.get()), width=5
    )
s_n.pack(side='left')
label_rule = tk.Label(root, text=rule)
label_rule.pack(side='left')

# Draw animation
anim = animation.FuncAnimation(fig, update, interval=50)
root.bind('<Configure>', on_change_window)
root.mainloop()
