import os


print("Starting")
with open("neg.txt.","w") as f:
    for filename in os.listdir("negative"):
        print(filename)
        f.write("negative/" + filename + "\n")