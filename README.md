# VisualReasoning
Visual Reasoning on CNLVR Dataset Using Answer Set Programming
==============================================================

This repository contains files for Visual Reasoning using Answer Set Programming on CNLVR Dataset. We have developed and tested our system on following envrionment;
Check out provided links for more details about each component.

Python2 (2.7.13 and 3.6.4)
OpenCV (3.3.0) (https://opencv.org/)
Stanford Parser (with englishPCFG.ser.gz) (https://nlp.stanford.edu/software/lex-parser.shtml)
Clingo (5.2.2) (http://potassco.sourceforge.net/clingo.html)

Directory Structure for Visual Reasoning:
=========================================

NLVR Dataset:
The dataset can be downloadd from Github repository https://github.com/clic-lab/nlvr

+--- nlvr-master 
|    +--- dev
|    +--- train
|    +--- test
|    license.txt
|    metrics_images.py
|    metrics_structured_rep.py

VisReason Repository:

Stanford Parser Dependencies:
Download stanford-parser-full-2018-02-27

Running the project:
====================

python -i xxx -p xxx 