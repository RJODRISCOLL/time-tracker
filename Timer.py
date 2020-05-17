from __future__ import print_function
from AppKit import NSWorkspace
import time
import csv
from os import system
from Foundation import *
from dateutil import parser
import datetime
from urllib.parse import urlparse
import re
import os


def find_csv_filenames(suffix=".csv" ):
    filenames = os.listdir()
    return [ filename for filename in filenames if filename.endswith( suffix ) ]


active_window_name = ""
activity_name = ""
start_time = datetime.datetime.now()
current_window = ""

currentDT = datetime.datetime.now()
today = currentDT.strftime("%d_%m_%y")

os.chdir('/Users/ruairi/Google Drive/Code/Python/time tracker/Outputs/')





path = str('Mac_timer_' + today + '.csv')
result = find_csv_filenames(suffix=path)




# check if entry exists for today
if len(result) < 1:
    print('First entry of the day, creating file.')
    outputFile = open(path, 'w', newline='')
    outputWriter = csv.writer(outputFile)
    outputWriter.writerow(['Location', 'Date', 'Start'])

elif len(result) > 0 :
    print('Not the first entry of the day, appending to existing file.')
    outputFile =open(path, 'a')
    outputWriter = csv.writer(outputFile)



try:
    while True:
        # get the current window
        new_window =(NSWorkspace.sharedWorkspace()
        .activeApplication()['NSApplicationName'])
        window_start_time = datetime.datetime.now()
        window_start_time = window_start_time.strftime("%H:%M:%S")


        # if the window changes
        if current_window != new_window:

            result = new_window
            print(window_start_time, result)

            if 'Google Chrome' in new_window:
                textOfMyScript = """tell app "google chrome" to get the url of the active tab of window 1"""
                s = NSAppleScript.initWithSource_(
                        NSAppleScript.alloc(), textOfMyScript)
                results, err = s.executeAndReturnError_(None)
                parsed_uri = urlparse(results.stringValue())
                result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
                result = re.sub('https://', '', result)
                result = re.sub('/', '', result)
                print(window_start_time, result)


            outputWriter.writerow([result, today, window_start_time])
            current_window = new_window

        time.sleep(1)






except KeyboardInterrupt:
    print('Killed with ctrl + c')
    outputFile.close()
