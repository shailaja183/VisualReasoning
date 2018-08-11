import csv
import json
import os
from main import Main

stanfordpath = '../StanfordParser/'
		
m = Main()

for subdir, dirs, files in os.walk('../nlvr-master/test/images/'):
    for file in files:
    	filepath = subdir + os.sep + file
        if filepath.endswith("-0.png"):
    		m.main(filepath, stanfordpath)
    		
        	




	


