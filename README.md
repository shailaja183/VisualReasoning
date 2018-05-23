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

+--- Nlvr-master <br /> 
|    +--- test <br /> 
| 	 |    +--- clingo (this directory will be created after running main.py) <br /> 
| 	 |	  +--- images <br /> 
|	 | 	  test.json <br /> 
|    +--- train <br /> 
| 	 |	  +--- clingo (this directory will be created after running main.py) <br /> 
| 	 |	  +--- images <br /> 
|	 | 	  train.json <br /> 

Stanford Parser Dependencies: <br /> 
-----------------------------
Download stanford-parser-full-2018-02-27 from https://nlp.stanford.edu/software/lex-parser.shtml#Download under heading 'Download Stanford Parser version 3.9.1'.

Followed by that, click on 'English Models' to download ''

Copy stanford-parser.jar from stanford-parser-full-2018-02-27 in the parent directory (stanford-parser), unzip and move to edu/stanford/nlp/ inside. 

+--- Stanford-Parser <br /> 
| >> englishPCFG.ser.gz <br /> 
| >> +--- stanford-parser-full-2018-02-27 <br /> 
| >> | >> stanford-parser.jar <br />  
| >> | >> stanford-parser-3.9.1-models.jar <br /> 

> +--- Stanford-Parser 
>> | englishPCFG.ser.gz 


Visual Reasoning Code Files: <br /> 
----------------------------

Clone VisualReasoning repository from https://github.com/shailaja183/VisualReasoning 

+--- VisualReasoning <br /> 
| 	 |	  clingo_rules_generator <br /> 
| 	 |	  color_shape_size_classifier.py <br /> 
| 	 |	  image_parser.py <br /> 
| 	 |	  main.py <br /> 
| 	 |	  query_parser.py <br />  

Running the project:
====================

python -i xxx -p xxx 