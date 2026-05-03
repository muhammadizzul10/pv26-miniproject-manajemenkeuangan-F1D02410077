from PySide6.QtWidgets import *
from PySide6.QtCore import QDate

class TransactionDialog(QDialog):
    def __init__(self, data=None):
        super().__init__()
        self.setWindowTitle("Form Transaksi")

        layout = QFormLayout()

        self.date = QDateEdit()
        self.date.setCalendarPopup(True)
        self.date.setDate(QDate.currentDate())

        self.name = QLineEdit()
        self.amount = QLineEdit()

        self.category = QComboBox()
        self.category.addItems(["Makanan", "Transport", "Hiburan", "Kuliah", "Lainnya"])

        self.type = QComboBox()
        self.type.addItems(["Pemasukan", "Pengeluaran"])

        self.priority = QComboBox()
        self.priority.addItems(["Penting", "Tidak Penting"])

        self.btn_save = QPushButton("Simpan")

        layout.addRow("Tanggal", self.date)
        layout.addRow("Nama", self.name)
        layout.addRow("Jumlah", self.amount)
        layout.addRow("Kategori", self.category)
        layout.addRow("Tipe", self.type)
        layout.addRow("Prioritas", self.priority)
        layout.addRow(self.btn_save)

        self.setLayout(layout)

        self.btn_save.clicked.connect(self.accept)

        if data:
            self.date.setDate(QDate.fromString(data[1], "yyyy-MM-dd"))
            self.name.setText(data[2])
            self.amount.setText(str(data[3]))
            self.category.setCurrentText(data[4])
            self.type.setCurrentText(data[5])
            self.priority.setCurrentText(data[6])

    def get_data(self):
        try:
            amount = int(self.amount.text())
        except:
            amount = 0

        return (
            self.date.date().toString("yyyy-MM-dd"),
            self.name.text(),
            amount,
            self.category.currentText(),
            self.type.currentText(),
            self.priority.currentText()
        )