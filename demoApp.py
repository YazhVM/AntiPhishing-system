# The screenshots of this are included in the screenshots folder
import sys
#from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit, QPushButton, QMessageBox
# load json and create model
json_file = open('model3conv_200.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model3conv_200.h5")
print("Loaded model from disk")
class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Phishing Website Detection'
        self.left = 10
        self.top = 10
        self.width = 600
        self.height = 600
        self.initUI()
   
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
   
        # Create textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(280,40)
       
        # Create a button in the window
        self.button = QPushButton('Enter', self)
        self.button.move(20,80)
       
        # connect button to function on_click
        self.button.clicked.connect(self.on_click)
        self.show()
   
    @pyqtSlot()
    def on_click(self):
        url = self.textbox.text()
        #url=[]
        #url.append(textboxValue)
        # Step 1: Convert raw URL string in list of lists where characters that are contained in "printable" are stored encoded as integer 
        url_int_tokens = [[printable.index(x) + 1 for x in url if x in printable]]
        # Step 2: Cut URL string at max_len or pad with zeros if shorter
        max_len=75
        X = sequence.pad_sequences(url_int_tokens, maxlen=max_len)
        y_prob = loaded_model.predict(X,batch_size=1)
        #print(url)
        QMessageBox.question(self, "Results","The URL is:" + print_result(y_prob), QMessageBox.Ok, QMessageBox.Ok)
        self.textbox.setText("")
if __name__ == "__main__":
    import sys
    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    AppWindow = QtWidgets.QMainWindow()
    ui = App()
    sys.exit(app.exec_())