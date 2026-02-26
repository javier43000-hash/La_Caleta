import sys
import os
import csv
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, 
                             QLabel, QComboBox, QHeaderView, QMessageBox)
from datetime import datetime
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from datetime import datetime

class LaCaleta(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("La Caleta - Control de Gastos 💰")
        self.setMinimumSize(700, 550) # Un poco más ancha para que respire
        self.archivo_datos = "gastos.csv"
        self.init_ui()
        self.cargar_datos()

    def init_ui(self):
        # Layout principal con márgenes internos
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(20, 20, 20, 20)
        layout_principal.setSpacing(15)

        # --- Fila de entrada mejorada ---
        fila_entrada = QHBoxLayout()
        fila_entrada.setSpacing(10)
        
        self.txt_descripcion = QLineEdit()
        self.txt_descripcion.setPlaceholderText("Descripción (ej: Supermercado)")
        self.txt_descripcion.setFixedHeight(35)
        
        self.combo_categoria = QComboBox()
        self.combo_categoria.addItems(["Comida 🍎", "Servicios ⚡", "Casa 🏠", "Varios ✨"])
        self.combo_categoria.setFixedHeight(35)

        self.txt_monto = QLineEdit()
        self.txt_monto.setPlaceholderText("Monto")
        self.txt_monto.setFixedWidth(80)
        self.txt_monto.setFixedHeight(35)

        btn_agregar = QPushButton("Registrar")
        btn_agregar.setFixedWidth(100)
        btn_agregar.setFixedHeight(35)
        btn_agregar.setCursor(Qt.PointingHandCursor)
        btn_agregar.setStyleSheet("""
            QPushButton {
                background-color: #2ECC71; 
                color: white; 
                font-weight: bold; 
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #27AE60;
            }
        """)
        btn_agregar.clicked.connect(self.agregar_gasto)

        # Añadimos con "stretch" para que la descripción sea la que crezca
        fila_entrada.addWidget(self.txt_descripcion, stretch=4)
        fila_entrada.addWidget(self.combo_categoria, stretch=2)
        fila_entrada.addWidget(self.txt_monto, stretch=1)
        fila_entrada.addWidget(btn_agregar)

        # --- Tabla estilizada ---
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(3)
        self.tabla.setColumnCount(4) # Antes era 3
        self.tabla.setHorizontalHeaderLabels(["Fecha", "Descripción", "Categoría", "Monto"])        
        self.tabla.setAlternatingRowColors(True)
        self.tabla.setStyleSheet("""
            QTableWidget {
                gridline-color: #DCDDE1;
                border: 1px solid #DCDDE1;
                alternate-background-color: #F5F6FA;
            }
            QHeaderView::section {
                background-color: #34495E;
                color: white;
                font-weight: bold;
                border: none;
                height: 30px;
            }
        """)
        
        # --- Total ---
        self.lbl_total = QLabel("Total Gastado: $0.00")
        self.lbl_total.setAlignment(Qt.AlignRight)
        self.lbl_total.setStyleSheet("""
            font-size: 20px; 
            font-weight: bold; 
            color: #E74C3C; 
            padding: 10px; 
            background-color: #FDEDEC;
            border-radius: 10px;
        """)

        layout_principal.addLayout(fila_entrada)
        layout_principal.addWidget(self.tabla)
        layout_principal.addWidget(self.lbl_total)

        self.setLayout(layout_principal)

    def agregar_gasto(self):
        desc = self.txt_descripcion.text().strip()
        cat = self.combo_categoria.currentText()
        monto_str = self.txt_monto.text().replace(',', '.')

        if not desc or not monto_str:
            return

        try:
            monto_float = float(monto_str)
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)
            self.tabla.setItem(row, 0, QTableWidgetItem(desc))
            self.tabla.setItem(row, 1, QTableWidgetItem(cat))
            
            # Formatear el monto a dos decimales
            item_monto = QTableWidgetItem(f"{monto_float:.2f}")
            item_monto.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tabla.setItem(row, 2, item_monto)
            
            self.txt_descripcion.clear()
            self.txt_monto.clear()
            self.actualizar_total()
            self.guardar_datos()
        except ValueError:
            QMessageBox.warning(self, "Formato Incorrecto", "Por favor, ingresa un número válido.")

    def actualizar_total(self):
        total = 0.0
        for i in range(self.tabla.rowCount()):
            item = self.tabla.item(i, 2)
            if item:
                total += float(item.text())
        self.lbl_total.setText(f"Total Gastado: ${total:.2f}")

    def guardar_datos(self):
        # Usamos ';' como separador y añadimos el BOM para los emojis
        with open(self.archivo_datos, "w", encoding="utf-8-sig", newline='') as f:
            escritor = csv.writer(f, delimiter=';') 
            for i in range(self.tabla.rowCount()):
                row_data = [
                    self.tabla.item(i, 0).text(),
                    self.tabla.item(i, 1).text(),
                    self.tabla.item(i, 2).text()
                ]
                escritor.writerow(row_data)

    def cargar_datos(self):
        if os.path.exists(self.archivo_datos):
            try:
                with open(self.archivo_datos, "r", encoding="utf-8") as f:
                    lector = csv.reader(f)
                    for datos in lector:
                        if len(datos) == 3:
                            row = self.tabla.rowCount()
                            self.tabla.insertRow(row)
                            for col, valor in enumerate(datos):
                                item = QTableWidgetItem(valor)
                                if col == 2: item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                                self.tabla.setItem(row, col, item)
                self.actualizar_total()
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = LaCaleta()
    ventana.show()
    sys.exit(app.exec_())