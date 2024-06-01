import subprocess
import time
import os

engine = os.path.join("pbrain-embryo21_s.exe")
# engine = os.path.join("pbrain_embryo.exe")
rule = '1'
timeout_turn = 0 # miliseconds
timeout_match = 0 # miliseconds
game_type = 1
time_left = 2146435072
max_memory = 83886080
num_thread = 12
class Embryo:
    def __init__(self, size):
        self.size = size
        self.p = None

    def init(self):
        self.p = subprocess.Popen(
            engine, 
            stdin=subprocess.PIPE, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT
        )

        if self.p.poll() is None:
            # print('Log: File opened')
            # print("log: START SETUP")
            self.p.stdin.write(f"INFO rule {rule}\n".encode())
            self.p.stdin.write(f"INFO timeout_turn {timeout_turn}\n".encode())
            self.p.stdin.write(f"INFO timeout_match {timeout_match}\n".encode())
            self.p.stdin.write(f"INFO game_type {game_type}\n".encode())
            self.p.stdin.write(f"INFO time_left {time_left}\n".encode())
            self.p.stdin.write(f"INFO max_memory {max_memory}\n".encode())
            # self.p.stdin.write(f"INFO num_thread {num_thread}\n".encode())
            self.p.stdin.write(f"START {self.size}\n".encode())
            self.p.stdin.flush()
            # print("Log: START GAME")

    def turn_move(self, x, y):
        print(f'TURN {x},{y}\n')
        self.p.stdin.write(f'TURN {x},{y}\n'.encode())
        self.p.stdin.flush()

    def turn_best(self, _begin):
        if _begin:
            self.p.stdin.write(f'BEGIN\n'.encode())
            self.p.stdin.flush()

        move_found = False;
        while not move_found:
            out = self.p.stdout.readline()
            out = out.decode()
            if out == '':
                break
            out = out.replace('\n', '')
            # print(f"Log: {out}")
            if out.find('MESSAGE') == -1 and out.find('DEBUG') == -1 and out.find('OK') == -1:
                out = out.replace('\n', '')
                engine_move = out.split(',')
                x, y = int(engine_move[0]), int(engine_move[1])
                if x == -self.size:
                    break
                move_found = True
                return (x, y)

    def stop(self):
        if self.p:
            self.p.terminate()
            self.p = None
