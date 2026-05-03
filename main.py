import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
from database import init_db, connect
from dialog import TransactionDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Smart Expense Tracker")
        self.setMinimumSize(800, 500)

        self.selected_id = None

        # TABLE
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Tanggal", "Nama", "Jumlah", "Kategori", "Tipe", "Prioritas"
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.itemSelectionChanged.connect(self.get_selected)

        # BUTTON
        self.btn_add = QPushButton("Tambah")
        self.btn_edit = QPushButton("Edit")
        self.btn_delete = QPushButton("Hapus")
        self.btn_refresh = QPushButton("Refresh")

        self.btn_edit.setEnabled(False)
        self.btn_delete.setEnabled(False)

        # LABEL SUMMARY
        self.label_income = QLabel("Pemasukan: 0")
        self.label_expense = QLabel("Pengeluaran: 0")
        self.label_balance = QLabel("Saldo: 0")

        # LAYOUT
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_edit)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addWidget(self.btn_refresh)

        summary_layout = QHBoxLayout()
        summary_layout.addWidget(self.label_income)
        summary_layout.addWidget(self.label_expense)
        summary_layout.addWidget(self.label_balance)

        main_layout = QVBoxLayout()
        main_layout.addLayout(btn_layout)
        main_layout.addLayout(summary_layout)
        main_layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # SIGNAL
        self.btn_add.clicked.connect(self.add_data)
        self.btn_edit.clicked.connect(self.edit_data)
        self.btn_delete.clicked.connect(self.delete_data)
        self.btn_refresh.clicked.connect(self.load_data)

        # MENU
        menu = self.menuBar()
        about_menu = menu.addMenu("Tentang")

        about_action = QAction("Tentang Aplikasi", self)
        about_action.triggered.connect(self.show_about)
        about_menu.addAction(about_action)

        self.load_data()

    # SELECT
    def get_selected(self):
        row = self.table.currentRow()
        if row < 0:
            self.selected_id = None
            self.btn_edit.setEnabled(False)
            self.btn_delete.setEnabled(False)
            return

        self.selected_id = int(self.table.item(row, 0).text())
        self.btn_edit.setEnabled(True)
        self.btn_delete.setEnabled(True)

    # ADD
    def add_data(self):
        dialog = TransactionDialog()

        if dialog.exec():
            data = dialog.get_data()
            conn = connect()
            cur = conn.cursor()

            cur.execute("""
            INSERT INTO transactions (date, name, amount, category, type, priority)
            VALUES (?, ?, ?, ?, ?, ?)
            """, data)

            conn.commit()
            conn.close()
            self.load_data()

    # EDIT
    def edit_data(self):
        if not self.selected_id:
            return

        conn = connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM transactions WHERE id=?", (self.selected_id,))
        data = cur.fetchone()
        conn.close()

        dialog = TransactionDialog(data)

        if dialog.exec():
            new_data = dialog.get_data()

            conn = connect()
            cur = conn.cursor()

            cur.execute("""
            UPDATE transactions
            SET date=?, name=?, amount=?, category=?, type=?, priority=?
            WHERE id=?
            """, (*new_data, self.selected_id))

            conn.commit()
            conn.close()
            self.load_data()

    # DELETE
    def delete_data(self):
        if not self.selected_id:
            return

        confirm = QMessageBox.question(
            self,
            "Konfirmasi",
            "Hapus data?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            conn = connect()
            cur = conn.cursor()
            cur.execute("DELETE FROM transactions WHERE id=?", (self.selected_id,))
            conn.commit()
            conn.close()
            self.load_data()

    # LOAD DATA
    def load_data(self):
        conn = connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM transactions")
        rows = cur.fetchall()
        conn.close()

        self.table.setRowCount(len(rows))

        income = 0
        expense = 0

        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))

            if row[5] == "Pemasukan":
                income += row[3]
            else:
                expense += row[3]

        self.label_income.setText(f"Pemasukan: {income}")
        self.label_expense.setText(f"Pengeluaran: {expense}")
        self.label_balance.setText(f"Saldo: {income - expense}")

        self.selected_id = None
        self.btn_edit.setEnabled(False)
        self.btn_delete.setEnabled(False)

    # ABOUT
    def show_about(self):
        QMessageBox.information(
            self,
            "Tentang",
            "Smart Expense Tracker\nNama: Muhammad izzul islam\nNIM: F1D02410077"
        )

import os

if __name__ == "__main__":
    app = QApplication(sys.argv)
    init_db()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    qss_path = os.path.join(base_dir, "style.qss")

    try:
        with open(qss_path, "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print(f"Error: File {qss_path} tidak ditemukan!")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())