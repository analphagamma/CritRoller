from CR_gui import *
from dbhandler import *

if __name__ == '__main__':
    dbobj = DBHandler('test.sqlite')
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    #Start the event loop
    app.exec_()
