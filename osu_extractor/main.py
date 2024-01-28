import sys
import zipfile

from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt6.QtGui import QIcon

from resources.ui import Ui_MainWindow


class OsuExtractor(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowIcon(QIcon("resources/Osu.png"))

        self.icon.setPixmap(QIcon("resources/Osu.png").pixmap(300, 300))

        self.selectbtn.clicked.connect(self.File_handler)

    def File_handler(self):
        dialog = QFileDialog()
        dialog.setNameFilter("Osu levels/skins (*.osz *.osk)")
        dialog_status = dialog.exec()

        if dialog_status == 1:
            file = dialog.selectedFiles()[0]
            file_data = file.split("/")[-1].split(".")
            try:
                with zipfile.ZipFile(file, "r") as osz_file:
                    if file_data[1] == "osz":
                        osz_file.extractall(f"../pyosu/songs/{' '.join(file_data[0].split(' ')[1:]).split(' - ')[1]}")
                    else:
                        osz_file.extractall(f"../pyosu/skins/{' '.join(file_data[0].split(' ')[1:]).split(' - ')[1]}")
                self.status.setText(f"Successfully added {' '.join(file_data[0].split(' ')[1:])}!")
            except zipfile.BadZipFile:
                self.status.setText(f"Something went wrong!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = OsuExtractor()
    ex.show()
    sys.exit(app.exec())
