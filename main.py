from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QLabel, QWidget
from pyautogui import FailSafeException
from keyboard import add_hotkey
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from sys import argv, exit
from random import randint
import pyautogui as pyag
from time import sleep


class MyWindow(QMainWindow):
    def __init__(self, width: int, height: int):
        super().__init__()
        self.setWindowTitle("Stumble Farm v1.31")
        self.setWindowIcon(QIcon("images\\icon.ico"))
        self.setFixedSize(width, height)
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.setStyleSheet("background-image: url(images/background.png)")
        self.label = QLabel("Enable - Press 9\n\nDisable - Press 0\n\nDisabled", self)
        layout.addWidget(self.label)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text_style = "QLabel { font-family: Arial; font-size: 16px; color: white;}"
        self.label.setStyleSheet(text_style)

        buttons_info = (("1 Event", self.first_event_farm),
                        ("2 Event", self.second_event_farm),
                        ("3 Event", self.third_event_farm),
                        ("Default Game", self.default_game_farm),
                        ("Exit", exit))

        for button_text, function in buttons_info:
            button = QPushButton(button_text, self)
            button_style = "QPushButton { font-family: FreeMono; font-size: 16px; color: white;}" \
                           "QPushButton:hover { font-family: FreeMono; font-size: 16px; color: gray;}"
            button.setStyleSheet(button_style)
            button.clicked.connect(function)
            layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)

    def first_event_farm(self):
        global event
        self.label.setText("Enable - Press 9\n\nDisable - Press 0\n\nAutoFarm: 1 Event")
        event = 1

    def second_event_farm(self):
        global event
        self.label.setText("Enable - Press 9\n\nDisable - Press 0\n\nAutoFarm: 2 Event")
        event = 2

    def third_event_farm(self):
        global event
        self.label.setText("Enable - Press 9\n\nDisable - Press 0\n\nAutoFarm: 3 Event")
        event = 3

    def default_game_farm(self):
        global event
        self.label.setText("Enable - Press 9\n\nDisable - Press 0\n\nAutoFarm: Default Game")
        event = 4


app = QApplication(argv)
window = MyWindow(200, 300)
leave_x = 250
leave_y = 1000
take_x = 1777
take_y = 1000
event = 0
pyag.FAILSAFE = True
app.setStyle("Fusion")
# 2 потока только если всё работает правильно


def autofarm() -> None:
    """
    This function enables autofarm.
    :return: None
    """
    global working
    working = True
    while working:
        try:
            sleep(randint(3, 6))
            if event != 4:
                pyag.click(1500, 800)
                sleep(1)
                if event == 1:
                    pyag.click(470, 985)

                if event == 2:
                    pyag.click(1250, 985)

                if event == 3:
                    pyag.click(1800, 985)
            else:
                pyag.click(1600, 970)
            sleep(randint(3, 6))
            while working:
                pixel_check = pyag.pixel(leave_x, leave_y)
                if pixel_check[0] > 230 and 90 > pixel_check[1] > 65 and 63 > pixel_check[2] > 49:
                    pyag.press("esc")
                    break

                if pixel_check[0] > 65 and pixel_check[1] > 180 and 30 > pixel_check[2] > 15:
                    pyag.click(take_x, take_y)
                    break
                    # TODO: исправить баги
                else:
                    sleep(0.1)
        except FailSafeException:
            break


def off_autofarm() -> None:
    """
    This function disables autofarm.
    :return: False
    """
    global working
    working = False
    # Функция не срабатывает


if __name__ == "__main__":
    add_hotkey("9", autofarm)
    add_hotkey("0", off_autofarm)
    window.show()
    exit(app.exec())
