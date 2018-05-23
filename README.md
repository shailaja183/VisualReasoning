# VisualReasoning
Visual Reasoning on CNLVR Dataset Using Answer Set Programming
==============================================================

This repository contains files for Visual Reasoning using Answer Set Programming on CNLVR Dataset. We have developed and tested our system on following envrionment.
Check out provided links for more details about each component.

Python2 (2.7.13 and 3.6.4) <br /> 
OpenCV (3.3.0) (https://opencv.org/) <br /> 
Stanford Parser (3.9.1 with englishPCFG.ser.gz) (https://nlp.stanford.edu/software/lex-parser.shtml) <br /> 
Clingo (5.2.2) (http://potassco.sourceforge.net/clingo.html) 

Required Directory Structure for running the project:
=====================================================

The following 3 directry structures should be maintained and they must be put under a same parent directory. (files/directories that are not relevant here are not shown)

NLVR Dataset: <br /> 
-------------
The dataset can be downloadd from Github repository https://github.com/clic-lab/nlvr 

+--- nlvr-master <br /> 
| &nbsp;&nbsp;&nbsp;&nbsp; +--- test <br /> 
| &nbsp;&nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;&nbsp; +--- clingo (this directory will be created after running main.py) <br /> 
| &nbsp;&nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;&nbsp; +--- images <br /> 
| &nbsp;&nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;&nbsp; test.json <br /> 
| &nbsp;&nbsp;&nbsp;&nbsp; +--- train <br /> 
| &nbsp;&nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;&nbsp; +--- clingo (this directory will be created after running main.py) <br /> 
| &nbsp;&nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;&nbsp; +--- images <br /> 
| &nbsp;&nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;&nbsp; train.json <br /> 

Stanford Parser Dependencies: <br /> 
-----------------------------
Download stanford-parser-full-2018-02-27 from https://nlp.stanford.edu/software/lex-parser.shtml#Download under heading 'Download Stanford Parser version 3.9.1' and unzip.

Copy stanford-parser-3.9.1-models.jar from stanford-parser-full-2018-02-27. Convert it to zip format and unzip. Then navigate to edu/stanford/nlp/models/lexparser. Copy englishPCFG.ser.gz and paste in parent directory (StanfordParser).

+--- StanfordParser <br /> 
| &nbsp;&nbsp;&nbsp;&nbsp; englishPCFG.ser.gz <br /> 
| &nbsp;&nbsp;&nbsp;&nbsp; +--- stanford-parser-full-2018-02-27 <br /> 
| &nbsp;&nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;&nbsp; stanford-parser.jar <br />  
| &nbsp;&nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;&nbsp; stanford-parser-3.9.1-models.jar <br /> 

Visual Reasoning Code Files: <br /> 
----------------------------

Clone VisualReasoning repository from https://github.com/shailaja183/VisualReasoning 

+--- VisualReasoning <br /> 
| &nbsp;&nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;&nbsp; clingo_rules_generator.py <br /> 
| &nbsp;&nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;&nbsp; color_shape_size_classifier.py <br /> 
| &nbsp;&nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;&nbsp; image_parser.py <br /> 
| &nbsp;&nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;&nbsp; main.py <br /> 
| &nbsp;&nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;&nbsp; query_parser.py <br />  

Running the project:
====================

Navigate to the VisualReasoning directory.

python2 main.py -i <path to image in train or test set>
(for example: python2 main.py -i ../nlvr-master/test/images/1/test-100-0-1.png)

The script will generate -
1. Annoted image after image parsing, press Enter to move forward. 
2. Clingo rules, file will be stored under nlvr-master/train/clingo or nlvr-master/test/clingo directory based on input image path.  
3. Parse tree after query parsing, Close the window to continue.


