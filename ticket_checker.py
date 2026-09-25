import sys
import requests
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem, QHeaderView,
    QFrame, QAbstractItemView
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont, QColor

API_URL = "https://www.totelepep.mu/WebApi/GetTicketStatus"

HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Origin": "https://www.totelepep.mu",
    "Referer": "https://www.totelepep.mu/",
}

STATUS_COLORS = {
    "WINNER": "#2ecc71",
    "LOSER": "#e74c3c",
    "UNDECIDED": "#f1c40f",
}

LEG_COLORS = {
    "WIN": QColor("#1e3d2f"),
    "LOS": QColor("#3d1e1e"),
    "UND": QColor("#3d3a1e"),
}

LEG_TEXT_COLORS = {
    "WIN": QColor("#2ecc71"),
    "LOS": QColor("#e74c3c"),
    "UND": QColor("#f1c40f"),
}


class TicketWorker(QThread):
    finished = Signal(dict, str)

    def __init__(self, ticket_id):
        super().__init__()
        self.ticket_id = ticket_id

    def run(self):
        try:
            response = requests.post(
                API_URL, headers=HEADERS,
                data=f"TicketNumber={self.ticket_id}", timeout=15
            )
            response.raise_for_status()
            self.finished.emit(response.json(), "")
        except Exception as e:
            self.finished.emit({}, str(e))


def clean_competition_name(raw_name):
    parts = [p.strip() for p in raw_name.split(" - ") if p.strip()]
    return " / ".join(parts)


class TicketChecker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Totelepep.mu Ticket Checker")
        self.resize(900, 620)
        self.worker = None
        self._build_ui()
        self._apply_theme()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        title = QLabel("Ticket Status Checker")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        layout.addWidget(title)

        input_row = QHBoxLayout()
        self.ticket_input = QLineEdit()
        self.ticket_input.setPlaceholderText("Paste ticket number e.g. AA5-6516723")
        self.ticket_input.returnPressed.connect(self.search_ticket)
        self.search_btn = QPushButton("Submit")
        self.search_btn.clicked.connect(self.search_ticket)
        input_row.addWidget(self.ticket_input)
        input_row.addWidget(self.search_btn)
        layout.addLayout(input_row)

        self.status_label = QLabel("")
        self.status_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        layout.addWidget(self.status_label)

        self.meta_label = QLabel("")
        self.meta_label.setFont(QFont("Segoe UI", 10))
        layout.addWidget(self.meta_label)

        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        layout.addWidget(divider)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["Time", "Match", "Market", "Pick", "Odds", "Result"]
        )
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.NoSelection)
        self.table.setAlternatingRowColors(False)
        layout.addWidget(self.table)

    def _apply_theme(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2e;
                color: #e0e0e0;
                font-family: 'Segoe UI';
            }
            QLineEdit {
                background-color: #2a2a3d;
                border: 1px solid #3d3d55;
                border-radius: 6px;
                padding: 8px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #7c5cff;
            }
            QPushButton {
                background-color: #7c5cff;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #6a4de8;
            }
            QPushButton:disabled {
                background-color: #4a4a5e;
            }
            QTableWidget {
                background-color: #16161f;
                border: 1px solid #3d3d55;
                border-radius: 6px;
                gridline-color: #2a2a3d;
                font-size: 11px;
            }
            QHeaderView::section {
                background-color: #2a2a3d;
                color: #e0e0e0;
                padding: 6px;
                border: none;
                font-weight: bold;
            }
        """)

    def search_ticket(self):
        ticket_id = self.ticket_input.text().strip()
        if not ticket_id:
            return
        self.search_btn.setEnabled(False)
        self.search_btn.setText("Searching...")
        self.status_label.setText("")
        self.meta_label.setText("")
        self.table.setRowCount(0)

        self.worker = TicketWorker(ticket_id)
        self.worker.finished.connect(self.on_result)
        self.worker.start()

    def on_result(self, data, error):
        self.search_btn.setEnabled(True)
        self.search_btn.setText("Submit")

        if error or not data.get("isSuccess"):
            self.status_label.setText("ERROR")
            self.status_label.setStyleSheet("color: #e74c3c;")
            self.meta_label.setText(error or data.get("errorMessage", "Unknown error"))
            return

        transaction = data.get("transaction", {})
        status = transaction.get("status", "UNKNOWN")
        color = STATUS_COLORS.get(status, "#e0e0e0")
        self.status_label.setText(status)
        self.status_label.setStyleSheet(f"color: {color};")

        booking_ref = transaction.get("bookingRef", "N/A")
        booking_date = transaction.get("bookingDate", "N/A")
        self.meta_label.setText(f"Ref: {booking_ref}    Booked: {booking_date}")

        bets = transaction.get("bets", [])
        self.table.setRowCount(len(bets))

        for row, bet in enumerate(bets):
            raw_name = bet.get("competitionName", "")
            outcome = "UND"
            for tag in ("WIN", "LOS", "UND"):
                if raw_name.strip().endswith(tag):
                    outcome = tag
                    raw_name = raw_name.rsplit("-", 1)[0].strip()
                    break

            match_name = clean_competition_name(raw_name)
            market = (bet.get("marketCode") or "").strip()
            pick = bet.get("optionName", "N/A")
            odd = bet.get("optionOdd", "N/A")
            bet_time = bet.get("betTime", "N/A")

            values = [bet_time, match_name, market, pick, str(odd), outcome]
            bg = LEG_COLORS.get(outcome, QColor("#16161f"))
            fg = LEG_TEXT_COLORS.get(outcome, QColor("#e0e0e0"))

            for col, val in enumerate(values):
                item = QTableWidgetItem(val)
                item.setBackground(bg)
                if col == 5:
                    item.setForeground(fg)
                    item.setFont(QFont("Segoe UI", 10, QFont.Bold))
                self.table.setItem(row, col, item)

        self.table.resizeRowsToContents()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TicketChecker()
    window.show()
    sys.exit(app.exec())