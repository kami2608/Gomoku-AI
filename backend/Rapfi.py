import subprocess
import time

class Rapfi:
    def __init__(self, executable_path, size=15):
        self.size = size
        self.executable_path = executable_path
        self.process = None

    def init(self):
        self.process = subprocess.Popen(
            self.executable_path, 
            stdin=subprocess.PIPE, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT
        )

        if self.process.poll() is None:
            print('Log: File opened')
            self.process.stdin.write(f'START {self.size}\n'.encode())
            self.process.stdin.flush()
            out = self.process.stdout.readline()
            if not out:
                print('Log: cannot read any line')
            else:
                out = out.decode()
                print(f'Log: {out}')

    def turn_move(self, x, y):
        print(f'TURN {x},{y}\n')
        self.process.stdin.write(f'TURN {x},{y}\n'.encode())
        self.process.stdin.flush()

    def turn_best(self, _begin):
        if _begin:
            self.process.stdin.write(f'BEGIN\n'.encode())
        else:
            time.sleep(2)
            self.process.stdin.write(f'STOP\n'.encode())

        self.process.stdin.flush()

        while True:
            out = self.process.stdout.readline()
            if not out:
                continue
            out = out.decode()
            print(out)
            if 'message' not in out:
                if out[0] in '0123456789':
                    move = out.split(',')
                    return int(move[0]), int(move[1].strip())

    def stop(self):
        if self.process:
            self.process.terminate()
            self.process = None
