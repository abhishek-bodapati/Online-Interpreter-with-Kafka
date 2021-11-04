import json
from threading import Timer
import subprocess
import os
import shlex

def compile_code(message):
    message = json.loads(message)
    code = message["message"]
    inputs = message["inputs"]
    return compile_code_helper(code, inputs)

def compile_code_helper(code, inputs):
    to_be_sent = ""
    # Create .py file
    filePath = 'x.py'
    try:
        outFile = open(filePath, 'w')
        outFile.write(code)
        outFile.close()
    except IOError as e:
        errno, strerror = e.args
        print("I/O error({0}): {1}".format(errno, strerror))

    # Run python file
    p = subprocess.Popen(shlex.split("python x.py"), stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    p.stdin.write(inputs)
    timeout_sec = 100
    timer = Timer(timeout_sec, p.kill)

    # Set a timer
    try: 
        timer.start()
        output, errors = p.communicate()
        if p.returncode:
            print(errors)
            to_be_sent = errors
        else:
            print(output)
            to_be_sent = output

    except:
        timer.cancel()

    # Delete the .py file
    os.remove("x.py")

    return to_be_sent
