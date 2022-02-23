from movement_functions import *
from graph_func import plot_trajectory
import numpy as np


FORWARD_DISTANCE = 420
HORIZONTAL_DISTANCE = 19
BREAK_FLAG = 0
UPPER_BORDER_DISTANCE = 210

# At the beginning robot is oriented to y axis (x=0, y=1)
direction = np.array([0, 1])
# Starting coordinates is (0, 0)
current_coordinates = np.array([0, 0], dtype=float)

# Moving to start position
print('Moving to start position')
for i in range(UPPER_BORDER_DISTANCE):
    output, current_coordinates = move_forward(100, current_coordinates, direction)
output, direction = turn_90_deg(direction, left=True)
for i in range(UPPER_BORDER_DISTANCE):
    output, current_coordinates = move_forward(100, current_coordinates, direction)
output, direction = turn_90_deg(direction, left=True)
print('At starting position...')
while True:
    print('Moving down...')
    BREAK_FLAG, output, current_coordinates = distance_movement(FORWARD_DISTANCE, current_coordinates, direction)
    if BREAK_FLAG == 1:
        break
    print('Turning left...')
    output, direction = turn_90_deg(direction, left=True)
    BREAK_FLAG, output, current_coordinates = distance_movement(HORIZONTAL_DISTANCE, current_coordinates, direction)
    if BREAK_FLAG == 1:
        break
    print('Turning left to move up...')
    output, direction = turn_90_deg(direction, left=True)
    print('Moving up...')
    BREAK_FLAG, output, current_coordinates = distance_movement(FORWARD_DISTANCE, current_coordinates, direction)
    if BREAK_FLAG == 1:
        break
    print('Turning to move down...')
    output, direction = turn_90_deg(direction, left=False)
    BREAK_FLAG, output, current_coordinates = distance_movement(HORIZONTAL_DISTANCE, current_coordinates, direction)
    if BREAK_FLAG == 1:
        break
    output, direction = turn_90_deg(direction, left=False)
send_data('0xFF 0xFF L0 R0 D20 0xEE')
send_data('0xFF 0xFF L0 R0 D0 0xEE')
going_back_forwardly(current_coordinates, direction)
plot_trajectory()
tcp_socket.close()
