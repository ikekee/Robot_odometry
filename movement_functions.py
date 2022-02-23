from socket import *
import numpy as np

L = 2 * np.pi * 0.04

HOST = '127.0.0.1'
PORT = 10007
ADDR = (HOST, PORT)

tcp_socket = socket()
tcp_socket.connect(ADDR)


def going_back_rectangular(current_coordinates: np.array, direction: np.array) -> None:
    while (direction != [0, 1]).all():
        _, direction = turn_90_deg(direction, left=True)
    horizontal_degree = np.abs(current_coordinates[0]) * 360 / L
    vertical_degree = np.abs(current_coordinates[1]) * 360 / L
    if current_coordinates[0] > 0 and current_coordinates[1] > 0:
        _, direction = turn_90_deg(direction, left=True)
        for _ in range(int(horizontal_degree / 10)):
            _, current_coordinates = move_forward(100, current_coordinates, direction)
        _, direction = turn_90_deg(direction, left=True)
        for _ in range(int(vertical_degree / 10)):
            _, current_coordinates = move_forward(100, current_coordinates, direction)
    elif current_coordinates[0] > 0 and current_coordinates[1] < 0:
        for _ in range(int(vertical_degree / 10)):
            _, current_coordinates = move_forward(100, current_coordinates, direction)
        _, direction = turn_90_deg(direction, left=True)
        for _ in range(int(horizontal_degree / 10)):
            _, current_coordinates = move_forward(100, current_coordinates, direction)
    elif current_coordinates[0] < 0 and current_coordinates[1] > 0:
        _, direction = turn_90_deg(direction, left=False)
        for _ in range(int(horizontal_degree / 10)):
            _, current_coordinates = move_forward(100, current_coordinates, direction)
        _, direction = turn_90_deg(direction, left=False)
        for _ in range(int(vertical_degree / 10)):
            _, current_coordinates = move_forward(100, current_coordinates, direction)
    elif current_coordinates[0] < 0 and current_coordinates[1] < 0:
        for _ in range(int(vertical_degree / 10)):
            _, current_coordinates = move_forward(100, current_coordinates, direction)
        _, direction = turn_90_deg(direction, left=False)
        for _ in range(int(horizontal_degree / 10)):
            _, current_coordinates = move_forward(100, current_coordinates, direction)


def going_back_forwardly(current_coordinates: np.array, direction: np.array) -> bytes:
    while (direction != [0, 1]).all():
        _, direction = turn_90_deg(direction, left=True)
    degrees_to_turn = np.degrees(np.arctan(np.abs(current_coordinates[0]) / np.abs(current_coordinates[1])))
    degrees_for_wheel_to_turn = degrees_to_turn * 0.075 / 0.04
    distance = np.sqrt(np.square(current_coordinates[0]) + np.square(current_coordinates[1]))
    degrees_for_wheel = 360 * distance / L
    if current_coordinates[0] > 0 and current_coordinates[1] > 0:
        for _ in range(2):
            _, direction = turn_90_deg(direction, left=True)
        turn_n_deg(degrees_for_wheel_to_turn, left=False)
        for _ in range(int(degrees_for_wheel / 10)):
            output, _ = move_forward(100, current_coordinates, direction)
            print(output.split()[7])
    elif current_coordinates[0] > 0 and current_coordinates[1] < 0:
        turn_n_deg(degrees_for_wheel_to_turn, left=True)
        for _ in range(int(degrees_for_wheel / 10)):
            output, _ = move_forward(100, current_coordinates, direction)
            if int(output.split()[7][1:]) == 1:
                break
    elif current_coordinates[0] < 0 and current_coordinates[1] > 0:
        _, direction = turn_90_deg(direction, left=False)
        turn_n_deg(degrees_for_wheel_to_turn, left=False)
        for _ in range(int(degrees_for_wheel / 10)):
            output, _ = move_forward(100, current_coordinates, direction)
            if int(output.split()[7][1:]) == 1:
                break
    elif current_coordinates[0] < 0 and current_coordinates[1] < 0:
        turn_n_deg(degrees_for_wheel_to_turn, left=False)
        for _ in range(int(degrees_for_wheel / 10)):
            output, _ = move_forward(100, current_coordinates, direction)
            if int(output.split()[7][2:]) == 1:
                break
    return output


def send_data(data_to_send: str) -> bytes:
    to_send = str.encode(data_to_send)
    tcp_socket.send(to_send)
    return tcp_socket.recv(1024)


def turn_n_deg(n: float, left=True) -> None:
    # Turns left by default. If 'left'=false, then it turns right
    if left:
        for _ in range(int(n / 10)):
            send_data('0xFF 0xFF L-100 R100 D0 0xEE')
        tuning_degr = n - int(n / 10) * 10
        send_data(f'0xFF 0xFF L-{tuning_degr} R{tuning_degr} D0 0xEE')
    else:
        for _ in range(int(n / 10)):
            send_data('0xFF 0xFF L100 R-100 D0 0xEE')
        tuning_degr = n - int(n / 10) * 10
        send_data(f'0xFF 0xFF L{tuning_degr} R-{tuning_degr} D0 0xEE')


def turn_90_deg(direction: np.array, left=True) -> (str, np.array):
    # Turns left by default. If 'left'=false, then it turns right
    # 337 degrees need to be rolled by wheel for robot to make 90 degrees turn
    if left:
        for i in range(16):
            send_data('0xFF 0xFF L-100 R100 D0 0xEE')
        if direction[0] == 0:
            direction = direction - direction[1]
        elif direction[1] == 0:
            direction[0], direction[1] = direction[1], direction[0]
        return send_data('0xFF 0xFF L-87 R87 D0 0xEE'), direction
    else:
        for i in range(16):
            send_data('0xFF 0xFF L100 R-100 D0 0xEE')
        if direction[0] == 0:
            direction[0], direction[1] = direction[1], direction[0]
        elif direction[1] == 0:
            direction = direction - direction[0]
        return send_data('0xFF 0xFF L87 R-87 D0 0xEE'), direction


def move_forward(speed_deg: int, current_coordinates: np.array, direction: np.array) -> (str, np.array):
    current_coordinates[np.nonzero(direction)[0][0]] = current_coordinates[np.nonzero(direction)[0][0]] + direction[
        np.nonzero(direction)[0][0]] * L * speed_deg / 3600
    return send_data(f'0xFF 0xFF L{speed_deg} R{speed_deg} D0 0xEE'), current_coordinates


def distance_movement(distance: int, coordinates: np.array, current_direction: np.array) -> (int, str, np.array):
    mission_flag = 0
    output_data = ''
    for _ in range(int(distance)):
        output_data, coordinates = move_forward(100, coordinates, current_direction)
        if int(output_data.split()[4][1:]) == 1:
            mission_flag = 1
            return mission_flag, output_data, coordinates
    return mission_flag, output_data, coordinates
