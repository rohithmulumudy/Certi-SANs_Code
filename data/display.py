# Date: 10/09/2020
# Author: rohith mulumudy
# Description: Displays progress bar


import sys
import time

class Display:    
    def __init__(self):
        self.total_count = 0

    def start_progress(self,title,total_count=100):
        self.total_count = total_count

        sys.stdout.write(title + ": " + "[ 00%]" + " [" + "-"*40 + "]")
        sys.stdout.flush()
        sys.stdout.write(chr(8)*49)

    def progress(self,value):
        percentage = int((value/(self.total_count))*100)
        x = int(percentage * 40 // 100)
        sys.stdout.write("[ {:02d}%]".format(percentage) + " [" + ("#" * x) + "-"*(40-x) + "]")
        sys.stdout.flush()
        sys.stdout.write(chr(8)*(49))

    def end_progress(self):
        sys.stdout.write("[100%]" + " [" + ("#" * 40) + "]\n")
        sys.stdout.flush()
