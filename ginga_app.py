import subprocess
import webbrowser
from PyQt5 import QtWidgets
import sys

def run_flask():
    subprocess.Popen(["python", "app.py"])

def open_browser():
    webbrowser.open("http://127.0.0.1:5000")

def main():
    app = QtWidgets.QApplication(sys.argv)
    
    # Create main window
    window = QtWidgets.QMainWindow()
    window.setWindowTitle("Pregnancy Risk Prediction")
    window.resize(400, 200)

    # Create a button to start Flask
    button = QtWidgets.QPushButton("Run Flask App", window)
    button.setGeometry(100, 70, 200, 40)
    button.clicked.connect(run_flask)

    # Create a button to open browser
    button2 = QtWidgets.QPushButton("Open Web App", window)
    button2.setGeometry(100, 120, 200, 40)
    button2.clicked.connect(open_browser)

    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
