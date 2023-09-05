import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QWidget, QGraphicsDropShadowEffect, QMessageBox
from PyQt5.QtGui import QTextCursor, QColor, QPalette
from PyQt5.QtCore import QTimer, QPropertyAnimation, QEasingCurve, Qt, QRect

from qm_auto import QuineMcCluskeyPyEDA

class QMApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window Configurations
        self.setWindowTitle("Simplificador Quine-McCluskey")
        self.setGeometry(100, 100, 700, 550)
        self.setStyleSheet("background-color: #1B1B2F;")

        # Main Layout
        self.layout = QVBoxLayout()
        self.layout.setSpacing(30)
        # Header
        self.header_label = QLabel(self)
        self.header_label.setText("<center><h2>MÉTODO DE SIMPLIFICACIÓN QUINE-McCLUSKEY</h2>"
                                  "<h3>ELECTRÓNICA DIGITAL</h3>"
                                  "ALEXANDER CASTAÑEDA<br>"
                                  "JOSE FELIPE DUARTE</center>")
        self.header_label.setStyleSheet("color: #F8F8FF; margin-bottom: 20px;")
        self.layout.addWidget(self.header_label)
        
        # Add shadow effect
        def add_shadow(widget):
            shadow = QGraphicsDropShadowEffect(self)
            shadow.setBlurRadius(15)
            shadow.setColor(QColor(0, 0, 0, 180))
            shadow.setOffset(4, 4)
            widget.setGraphicsEffect(shadow)

        # Minterms label and entry
        self.label_minterms = QLabel("Minterminos (separados por comas):", self)
        self.label_minterms.setStyleSheet("color: #F8F8FF; font-size: 16pt;")
        add_shadow(self.label_minterms)
        self.layout.addWidget(self.label_minterms)

        self.entry_minterms = QLineEdit(self)
        self.entry_minterms.setStyleSheet("background-color: #3A3B3C; color: #F8F8FF; font-size: 14pt; padding: 10px; border-radius: 5px;")
        add_shadow(self.entry_minterms)
        self.layout.addWidget(self.entry_minterms)

        # Buttons
        self.btn_simplify = QPushButton("Simplificar", self)
        self.btn_simplify.setStyleSheet("background-color: #4B49A1; color: #F8F8FF; font-size: 14pt; padding: 10px; border: none; border-radius: 5px;")
        add_shadow(self.btn_simplify)
        self.btn_simplify.clicked.connect(self.simplify_expression)
        self.layout.addWidget(self.btn_simplify)

        self.btn_clear = QPushButton("Limpiar", self)
        self.btn_clear.setStyleSheet("background-color: #4B49A1; color: #F8F8FF; font-size: 14pt; padding: 10px; border: none; border-radius: 5px;")
        add_shadow(self.btn_clear)
        self.btn_clear.clicked.connect(self.clear_fields)
        self.layout.addWidget(self.btn_clear)

        # Result label and text box
        self.label_result = QLabel("Resultado:", self)
        self.label_result.setStyleSheet("color: #F8F8FF; font-size: 16pt;")
        add_shadow(self.label_result)
        self.layout.addWidget(self.label_result)

        self.result_text = QTextEdit(self)
        self.result_text.setReadOnly(True)
        self.result_text.setStyleSheet("background-color: #3A3B3C; color: #F8F8FF; font-size: 14pt; border-radius: 5px;")
        add_shadow(self.result_text)
        self.layout.addWidget(self.result_text)

        # Set layout
        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)
    def animate_button(self, button):
        start_rect = button.geometry()
        end_rect = QRect(button.x(), button.y() + 10, button.width(), button.height())

        animation = QPropertyAnimation(button, b"geometry", self)
        animation.setDuration(100)
        animation.setStartValue(start_rect)
        animation.setEndValue(end_rect)
        animation.setEasingCurve(QEasingCurve.InOutQuart)
        
        reverse_animation = QPropertyAnimation(button, b"geometry", self)
        reverse_animation.setDuration(100)
        reverse_animation.setStartValue(end_rect)
        reverse_animation.setEndValue(start_rect)
        reverse_animation.setEasingCurve(QEasingCurve.InOutQuart)

        animation.finished.connect(reverse_animation.start)
        animation.start()


    def simplify_expression(self):
        self.animate_button(self.btn_simplify)
        minterms_input = self.entry_minterms.text().strip()

        # Verificar si el campo minterms está vacío
        if not minterms_input:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Por favor, ingrese minterminos.")  # Esto establece el texto principal
            msg.setWindowTitle("Error")
            msg.exec_()
            return

        try:
            minterms_list = [int(x.strip()) for x in minterms_input.split(',')]
            
            qm = QuineMcCluskeyPyEDA(minterms=minterms_list)
            result = qm.simplify(minterms_list)

            self.result_text.clear()

            # Create a QTimer to insert the result with some delay to create animation
            self.timer = QTimer(self)
            self.result_string = result
            self.result_index = 0

            def insert_result():
                if self.result_index < len(self.result_string):
                    self.result_text.textCursor().insertText(self.result_string[self.result_index])
                    self.result_index += 1
                else:
                    self.timer.stop()

            self.timer.timeout.connect(insert_result)
            self.timer.start(3)  # 3 ms delay between characters

        except Exception as e:
            self.result_text.clear()
            self.result_text.insertPlainText(f"Error: {str(e)}")

    def clear_fields(self):
        self.animate_button(self.btn_clear)
        self.entry_minterms.clear()
        self.result_text.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Setting a modern palette to the app
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Highlight, QColor(142, 45, 197).lighter())
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(dark_palette)
    window = QMApp()
    window.show()
    sys.exit(app.exec_())
