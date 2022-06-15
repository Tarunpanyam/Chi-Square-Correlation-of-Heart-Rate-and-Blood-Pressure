import os
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget
from PyQt5.QtGui import QPixmap
import csv
import pandas as pd
import sqlite3


class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("welcomescreen.ui",self)
        self.PD.clicked.connect(self.gotoPD)
        self.TD.clicked.connect(self.gotoTD)
        self.CC.clicked.connect(self.gotoCC)


    def gotoPD(self):
        pd = PatientDetails()
        widget.addWidget(pd)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoTD(self):
        td = TestDetails()
        widget.addWidget(td)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoCC(self):
        c = Corelations()
        widget.addWidget(c)
        widget.setCurrentIndex(widget.currentIndex()+1)



class PatientDetails(QDialog):
    #pid ,pname ,dob ,addr1 ,addr2 ,aadhar ,mobile 
    def __init__(self):
        super(PatientDetails, self).__init__()
        loadUi("patientdetails.ui",self)
        self.store.clicked.connect(self.storefuntion)
        self.back.clicked.connect(self.homefuntion)
    def storefuntion(self):
        df1 = pd.read_csv("test.csv")
        pid=str(df1.shape[0]+1)
        #pid=self.pid.text()
        dob=self.dob.text()
        pname=self.pname.text()
        addr1=self.addr1.text()
        addr2=self.addr2.text()
        aadhar=self.aadhar.text()
        mobile=self.mobile.text()
        if len(pid)==0 or len(dob)==0 or len(pname)==0 or len(addr1)==0 or len(aadhar)==0 or len(mobile)==0:
            self.error.setText("Please fill in all inputs.")
        else:
            conn = sqlite3.connect("test.db")
            cur = conn.cursor()

            user_info = [pid,pname ,dob ,addr1 ,addr2 ,aadhar ,mobile]
            try:
                cur.execute('INSERT INTO patient (pid,pname ,dob ,addr1 ,addr2 ,aadhar ,mobile) VALUES (?,?,?,?,?,?,?)', user_info)
                self.error.setText("successful !!!")
            except:
                self.error.setText("Unsuccessful !!! Enter previous patient test results")
            conn.commit()
            conn.close()
    def homefuntion(self):
        home = WelcomeScreen()
        widget.addWidget(home)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
class TestDetails(QDialog):
    def __init__(self):
        super(TestDetails, self).__init__()
        loadUi("testdetails.ui",self)
        self.store.clicked.connect(self.storefuntion)
        self.back.clicked.connect(self.homefuntion)

    def storefuntion(self):
        df1 = pd.read_csv("test.csv")
        pid=str(df1.shape[0]+1)
        #pid=self.pid.text()
        hr=self.hr.text()
        bp=self.bp.text()
        # def friend_exists(friend):
        #     reader = csv.reader(open("test.csv", "r"), delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        #     for row in reader:
        #         if (row == friend):
        #             return True
        #     return False
        def add_friend(id, bp, hr):
            friend = [id, bp, hr]
            # if friend_exists(friend):
            #     return False 
            writer = csv.writer(open("test.csv", "a"),lineterminator='\r', delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(friend)
            return True
        if len(pid)==0 or len(hr)==0 or len(bp)==0:
            self.error.setText("Please fill in all inputs.")
        else:
            # conn = sqlite3.connect('train.db')
            # c = conn.cursor()
            # user_info = [pid,hr,bp]
            # c.execute('INSERT INTO  results(pid,hr,bp) VALUES (?,?,?)', user_info)
            # self.error.setText("successful !!!")
            # conn.commit()
            # conn.close()
            if(add_friend(pid, bp, hr)):
                self.error.setText("successful !!!")
            else:
                self.error.setText("Unsuccessful !!!")


    def homefuntion(self):
        home = WelcomeScreen()
        widget.addWidget(home)
        widget.setCurrentIndex(widget.currentIndex()+1)

class Corelations(QDialog):
    def __init__(self):
        super(Corelations, self).__init__()
        loadUi("statistics.ui",self)
        os.system("python sam5.py> output.txt")
        self.result.clicked.connect(self.Display_Tweets)
        self.back.clicked.connect(self.homefuntion)

    def Display_Tweets(self):
        readtweets = open("output.txt", "r")
        tweetlist = readtweets.readlines()
        for x in tweetlist:
            self.output.append(x)
        readtweets.close()

    def homefuntion(self):
        home = WelcomeScreen()
        widget.addWidget(home)
        widget.setCurrentIndex(widget.currentIndex()+1)


# main
app = QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(800)
widget.setFixedWidth(1200)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")