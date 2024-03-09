import threading
import subprocess

def run_script(script_name):
    subprocess.run(["python", script_name])

script1_thread = threading.Thread(target=run_script, args=("clientOne.py"))
script2_thread = threading.Thread(target=run_script, args=("clientTwo.py"))
script3_thread = threading.Thread(target=run_script, args=("clientThree.py"))

script1_thread.start()
script2_thread.start()
script3_thread.start()

script1_thread.join()
script2_thread.join()
script3_thread.join()

print("All scripts have finished executing.")
    