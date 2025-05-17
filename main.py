import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QRadioButton,
    QPushButton, QVBoxLayout, QHBoxLayout, QButtonGroup, QTextEdit
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class VotingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Voting App")
        self.setFixedSize(350, 400)
        self.vote_file = "votes.txt"
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.show_vote_screen()

    def clear(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def show_vote_screen(self):
        self.clear()

        title = QLabel("VOTING APPLICATION")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(title)

        id_row = QHBoxLayout()
        id_row.addWidget(QLabel("ID:"))
        self.id_input = QLineEdit()
        id_row.addWidget(self.id_input)
        self.layout.addLayout(id_row)

        self.layout.addWidget(QLabel("CANDIDATES", alignment=Qt.AlignmentFlag.AlignCenter))

        self.bianca = QRadioButton("Bianca")
        self.edward = QRadioButton("Edward")
        self.felicia = QRadioButton("Felicia")

        self.group = QButtonGroup()
        self.group.addButton(self.bianca)
        self.group.addButton(self.edward)
        self.group.addButton(self.felicia)

        self.layout.addWidget(self.bianca)
        self.layout.addWidget(self.edward)
        self.layout.addWidget(self.felicia)

        self.submit_btn = QPushButton("SUBMIT VOTE")
        self.submit_btn.clicked.connect(self.vote)
        self.layout.addWidget(self.submit_btn)

        self.history_btn = QPushButton("VIEW HISTORY")
        self.history_btn.clicked.connect(self.show_history)
        self.layout.addWidget(self.history_btn)

        self.status = QLabel("")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status.setStyleSheet("color: green; font-weight: bold;")
        self.layout.addWidget(self.status)

    def vote(self):
        uid = self.id_input.text().strip()
        if not uid:
            self.status.setText("ID Required")
            self.status.setStyleSheet("color: red; font-weight: bold;")
            return

        if os.path.exists(self.vote_file):
            with open(self.vote_file, "r") as f:
                for line in f:
                    existing_id = line.strip().split(",")[0]
                    if uid == existing_id:
                        self.status.setText("Already voted")
                        self.status.setStyleSheet("color: red; font-weight: bold;")
                        return

        if self.bianca.isChecked():
            pick = "Bianca"
        elif self.edward.isChecked():
            pick = "Edward"
        elif self.felicia.isChecked():
            pick = "Felicia"
        else:
            self.status.setText("Select a Candidate")
            self.status.setStyleSheet("color: red; font-weight: bold;")
            return

        with open(self.vote_file, "a") as f:
            f.write(f"{uid},{pick}\n")

        self.status.setText("Vote Recorded")
        self.status.setStyleSheet("color: green; font-weight: bold;")
        self.id_input.clear()
        self.group.setExclusive(False)
        self.bianca.setChecked(False)
        self.edward.setChecked(False)
        self.felicia.setChecked(False)
        self.group.setExclusive(True)

    def show_history(self):
        self.clear()

        header = QLabel("VOTING HISTORY")
        header.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(header)

        self.text_box = QTextEdit()
        self.text_box.setReadOnly(True)

        if os.path.exists(self.vote_file):
            with open(self.vote_file, "r") as f:
                self.text_box.setText(f.read())
        else:
            self.text_box.setText("No votes recorded yet.")

        self.layout.addWidget(self.text_box)

        back_btn = QPushButton("BACK TO VOTING")
        back_btn.clicked.connect(self.show_vote_screen)
        self.layout.addWidget(back_btn)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = VotingApp()
    win.show()
    sys.exit(app.exec())