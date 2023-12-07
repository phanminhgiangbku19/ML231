#This is folder of group 07
--------------------------------

## Menber of group:
-Nguyễn Thanh Toàn : 2014777.
-Nguyễn Hoàng Hiếu : 2011189.
** Supervisor: Nguyễn Khánh Lợi. **
--------------------------------
## Title of project: Sentiment Analysis on feedback from airline passengers
-Mission: Biuld a model marchine learnning to predict sentiment of feedback.
-Model: 
	.Input: A text (length about 50 word, maximum 100 word).
	.Embedding layer.
	.Conv1D layer.
	.Maxpolling1D layer.
	.Flatten layer.
	.Fully connected layer.
	.Ouput layer: A numberic (if more than 0.5, text in input is positive, if less than 0.5, text in input is negative).
-Specification: Accurracy more than 0.7
------------------------------
## User manual source code
### 1. Request:
- In your PC have tenserflow library.
- RAM useable more than 50MB.
- This program can run without GPU, but if you have a GPU it will be run faster.
- Make sure you put all file into the same folder.
### 2. If first time run program
**Check in your folder, if file vocab2.txt is not exist please follow some step below.**
. Run file Addvocab2.py
''''
>> python Addvocab2.py
''''
. After done Addvocab2.py then close this program.
. Run airline.py
''''
>> python airline.py
''''
.Enjoy your program. 
**If file vocab2.txt is exist you can skip step run file Addvocab2,py**

---------------------------------------
**Thank for reading :))**


