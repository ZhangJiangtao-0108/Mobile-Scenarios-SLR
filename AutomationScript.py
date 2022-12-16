import subprocess


## 进行模型分类
Mobiles = ["walk", "up-the-stairs", "down-the-stairs"]
# Mobiles = ["down-the-stairs"]

for Mobile in Mobiles:
    # subprocess.run(["python", r".\Analysis.py", "--Mobile", Mobile], shell=True)

    # subprocess.run(["python", r".\CompositeSignals.py", "--Mobile", Mobile], shell=True)

    subprocess.run(["python", r".\DTWCompare.py", "--Mobile", Mobile], shell=True)


    
