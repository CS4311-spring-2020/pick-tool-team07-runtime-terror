# PICK Tool by Team 7-Runtime Terror


### Dependencies
- Python 3
- PyQt5
```
python3 -m pip install PyQt5
```
- QGraphViz
```
python3 -m pip install QGraphViz
```
- Pymongo: you need to install Mongodb in your machine in order for this to work, I used the following link https://docs.mongodb.com/manual/tutorial/install-mongodb-on-debian/    (be aware that this link is only for linux-debian systems)
```
python3 -m pip install pymongo
```

- OCR: Pytesseract: It was never specefied which OCR software to use in SRS and it was also not specified which we couldnt use.
```
python3 -m pip install filetype
python3 -m pip install pytesseract

You have to install the OCR engine, so the following will work on linux machines: 
sudo apt install tesseract-ocr
sudo apt install libtesseract-dev
```
### Running PICK system
Shell script was provided, this shell script is only meant to be run in Linux environments
it also does not check if the necessary services are installed in the machine, so need to 
write another script that checks for that and installes the necessary services. 
To run the script you have to do the following: 
```
chmod u+x pick.sh

./pick.sh
```

chmod command only has to be run once, this command gives executable permissions to the script. Once you run it once you dont have to do it again. 

