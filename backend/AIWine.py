import subprocess
import time
import os

engine = "pbrain-wine.exe"
rule = '1'
timeout_turn = 500
timeout_turn_down = 500
game_type = 1
timeout_match = 0
time_left = 2147483647
max_memory = 536870912
thread_num = 8

class Wine:
    def __init__(self, size):
        self.size = size
        self.p = None
        self.is_descreased = False

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
            # self.p.stdin.write(f"INFO rule {rule}\n".encode())
            self.p.stdin.write(f"INFO timeout_turn {timeout_turn}\n".encode())
            # self.p.stdin.write(f"INFO timeout_match {timeout_match}\n".encode())
            # self.p.stdin.write(f"INFO game_type {game_type}\n".encode())
            # self.p.stdin.write(f"INFO time_left {time_left}\n".encode())
            # self.p.stdin.write(f"INFO max_memory {max_memory}\n".encode())
            # self.p.stdin.write(f"INFO thread_num {thread_num}\n".encode())
            self.p.stdin.write(f"START {self.size}\n".encode())
            self.p.stdin.flush()
            # print("Log: START GAME")

    def turn_move(self, x, y):
        self.time_begin = time.time()
        print(f'TURN {x},{y}\n')
        self.p.stdin.write(f'TURN {x},{y}\n'.encode())
        self.p.stdin.flush()

    def descrease_timeout_turn(self):
        if not self.is_descreased:
            self.is_descreased = True
            print('Log: Descrease timeout_turn')
            self.p.stdin.write(f"INFO timeout_turn {timeout_turn_down}\n".encode())
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
            print(f"Log: {out}")
            if out.find('MESSAGE') == -1 and out.find('DEBUG') == -1 and out.find('OK') == -1:
                out = out.replace('\n', '')
                engine_move = out.split(',')
                x, y = int(engine_move[0]), int(engine_move[1])
                if x == -self.size:
                    break
                move_found = True
                self.time_end = time.time()  
                elapsed_time = self.time_end - self.time_begin 
                print(f"Time taken for move: {elapsed_time} seconds")
                return (x, y)

    def stop(self):
        if self.p:
            self.p.terminate()
            self.p = None
