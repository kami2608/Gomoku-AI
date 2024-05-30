import subprocess
import time
import os

engine = os.path.join("build", "pbrain-rapfi.exe")
rule = '0'
timeout_turn = 1000 # seconds
timeout_match = 50000 # seconds

class Rapfi:
    def __init__(self, size=15):
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
            print('Log: File opened')
            print("log: START SETUP")
            self.p.stdin.write(f"INFO rule {rule}\n".encode())
            self.p.stdin.write(f"INFO timeout_match {timeout_match}\n".encode())
            # self.p.stdin.write(f"INFO timeout_turn {timeout_turn}\n".encode())
            self.p.stdin.write(f"START {self.size}\n".encode())
            self.p.stdin.flush()
            print("Log: START GAME")

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
            print(f"Log: {out}")
            if out.find('MESSAGE') == -1 and out.find('OK') == -1:
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
