import os
import sys

# Add the directory containing the .pyd file to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'AIWine', 'build'))

# Check if the path is correctly added
print("Sys path: ", sys.path)

try:
    import gomoku_ai
    print("Module imported successfully")
except ImportError as e:
    print("ImportError: ", e)
