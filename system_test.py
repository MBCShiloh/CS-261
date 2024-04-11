import sys

original_stdout = sys.stdout
with open('output.txt', 'w') as f:
    sys.stdout = f


    cur_version = sys.version_info
    if cur_version >= (3, 10):
        print("This is an acceptable version of Python, version " + str(cur_version[0]) + '.' + str(cur_version[1]) + '.')
    else:
        print("Your Python version is too low, it needs to be 3.10 or greater and this is " + str(cur_version[0]) + '.' + str(cur_version[1]) + '.')

    print("This will also go to output.txt")

# Reset stdout
sys.stdout = original_stdout  # Reset the standard output to its original value

print("This will print to the console.")
