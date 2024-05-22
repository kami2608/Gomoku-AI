import os
import sys

# Add the directory containing the .pyd file to sys.path
pyd_path = os.path.join(os.path.dirname(__file__), 'AIWine', 'build')
sys.path.append(pyd_path)

# Add directory containing DLLs to DLL search path
dll_path = os.path.join(os.path.dirname(__file__), 'AIWine', 'build')
os.add_dll_directory(dll_path)

# Check if the path is correctly added
print("Sys path: ", sys.path)

# List files in the directory to check if the .pyd file is present
print("Files in build directory: ", os.listdir(pyd_path))

try:
    import gomoku_ai
    print("Module imported successfully")
except ImportError as e:
    print("ImportError: ", e)

    # Detailed information on the error
    import traceback
    print(traceback.format_exc())
