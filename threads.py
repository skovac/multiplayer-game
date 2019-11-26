import threading
import time

class test:
    def __init__(self):
        self.testValue = 0

def target_function(obj):
    while True:
        obj.testValue += 1
        #time.sleep(1)

def main():
    obj = test()
    x = threading.Thread(target=target_function, args=(obj,))
    x.start()

    while True:
        print(obj.testValue)
        #time.sleep(1)


if __name__ == "__main__":
    main()
