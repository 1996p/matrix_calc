from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator

from main_ui import Ui_MainWindow
from funtion import matrix_multiplier, matrix_sum

class CalcWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(CalcWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

        self.matrix_A = [
            [],
        ]
        self.matrix_B = [
            [],
        ]

        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setBold(True)
        font.setWeight(75)
        font.setPointSize(15)


        self.ui.result.setMargin(10)
        self.ui.result.setFont(font)
        self.ui.result.hide()

        #CONST
        self.START_A_INPUT_X = 30
        self.START_B_INPUT_X = 0

        # SETTINGS MATRIX A
        self.START_A_INPUT_X = 30
        self.START_A_INPUT_Y = 150

        #SETTINGS MATRIX B
        self.START_B_INPUT_X = 400
        self.START_B_INPUT_Y = 150


        self.set_input_validators()
        self.btn_functions()
        self.show()



    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = None

    def mouseMoveEvent(self, event):
        if not self.old_pos:
            return

        delta = event.pos() - self.old_pos
        self.move(self.pos() + delta)

    def btn_functions(self):
        self.ui.multiplier.clicked.connect(self.get_input_value)
        self.ui.sum.clicked.connect(self.get_matrix_sum)
        self.ui.columnsInA_input.textChanged.connect(lambda x: self.create_inputs(matrix='A'))
        self.ui.rowsInA_input.textChanged.connect(lambda x: self.create_inputs(matrix='A'))
        self.ui.columnsInB_input.textChanged.connect(lambda x: self.create_inputs(matrix='B'))
        self.ui.rowsInB_input.textChanged.connect(lambda x: self.create_inputs(matrix='B'))
        self.ui.closeBtn.clicked.connect(self.close)


    def set_input_validators(self):
        self.ui.rowsInB_input.setValidator(QIntValidator(-1, 1))
        self.ui.rowsInA_input.setValidator(QIntValidator(-1, 1))
        self.ui.columnsInB_input.setValidator(QIntValidator(-1, 1))
        self.ui.columnsInA_input.setValidator(QIntValidator(-1, 1))

    def start_error_animation(self):
        self.anim = QtCore.QPropertyAnimation(self.ui.multiplierError, b'geometry')
        self.anim.setEasingCurve(QtCore.QEasingCurve.OutQuad)
        self.anim.setDuration(500)
        self.anim.setStartValue(QtCore.QRect(250, -16, 301, 41))
        self.anim.setEndValue(QtCore.QRect(250, 24, 301, 41))
        self.anim.start()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.end_error_animation)
        self.timer.start(3500)
        self.anim.start()

    def end_error_animation(self):
        self.anim = QtCore.QPropertyAnimation(self.ui.multiplierError, b'geometry')
        self.anim.setEasingCurve(QtCore.QEasingCurve.OutQuad)
        self.anim.setDuration(500)
        self.anim.setStartValue(QtCore.QRect(250, 24, 301, 41))
        self.anim.setEndValue(QtCore.QRect(250, -16, 301, 41))
        self.anim.start()
        self.timer.stop()

    def get_matrix_sum(self):
        if self.count_of_rows_A != self.count_of_rows_B or self.count_of_columns_A != self.count_of_columns_B:
            self.ui.multiplierError.setText('Размерности матриц не совпадают')
            self.start_error_animation()
            return
        self.matrix_A_content = []
        for i in self.matrix_A:
            self.matrix_A_content_buff = []
            for n in i:
                try:
                    self.matrix_A_content_buff.append(int(n.text()))
                except Exception:
                    self.ui.multiplierError.setText('Матрица A не заполнена')
                    self.start_error_animation()
                    return
            self.matrix_A_content.append(self.matrix_A_content_buff)
        print('MATRIX A: ', self.matrix_A_content)

        self.matrix_B_content = []
        for i in self.matrix_B:
            self.matrix_B_content_buff = []
            for n in i:
                try:
                    self.matrix_B_content_buff.append(int(n.text()))
                except Exception:
                    self.ui.multiplierError.setText('Матрица B не заполнена')
                    self.start_error_animation()
                    return
            self.matrix_B_content.append(self.matrix_B_content_buff)
        print('MATRIX B: ', self.matrix_B_content)

        self.sum_result = matrix_sum(self.matrix_A_content, self.matrix_B_content)
        self.show_result(self.sum_result)

    def get_input_value(self):
        if self.count_of_rows_A == 1 and self.count_of_columns_A == 1:
            self.matrix_A_content = self.get_matrix_content(self.matrix_A, type_of_matrix='first_multiplier' )
            self.matrix_B_content = self.get_matrix_content(self.matrix_B, type_of_matrix='first_multiplier')

            self.multiplier_result = matrix_multiplier(self.matrix_A_content, self.matrix_B_content)
            self.show_result(self.multiplier_result)

        elif self.count_of_rows_A != self.count_of_columns_B:
            self.ui.multiplierError.setText('Неверная размерность матрицы')
            self.start_error_animation()
            return
        else:
            self.matrix_A_content = self.get_matrix_content(self.matrix_A, type_of_matrix='first_multiplier' )

            self.matrix_B_content = self.get_matrix_content(self.matrix_B, type_of_matrix='second_multiplier' )
            if self.matrix_A_content is not None and self.matrix_B_content is not None:
                self.multiplier_result = matrix_multiplier(self.matrix_A_content, self.matrix_B_content)
                self.show_result(self.multiplier_result)

    def create_inputs(self, matrix):
        self.ui.result.hide()

        try:
            self.count_of_columns_A = int(self.ui.columnsInA_input.text())
        except ValueError:
            self.count_of_columns_A = 1
        try:
            self.count_of_rows_A = int(self.ui.rowsInA_input.text())
        except ValueError:
            self.count_of_rows_A = 1
        try:
            self.count_of_columns_B = int(self.ui.columnsInB_input.text())
        except ValueError:
            self.count_of_columns_B = 1
        try:
            self.count_of_rows_B = int(self.ui.rowsInB_input.text())
        except ValueError:
            self.count_of_rows_B = 1

        if matrix == 'A':
            for i in self.matrix_A:
                for n in i:
                    try:
                        n.deleteLater()
                    except Exception:
                        pass
            self.matrix_A = []

            for i in range(0, self.count_of_columns_A):
                self.matrix_A.append([])

            self.widget_y = self.START_A_INPUT_Y

            for e in self.matrix_A:
                self.widget_x = 0
                for i in range(0, self.count_of_rows_A):
                    self.widget = QtWidgets.QLineEdit(self.ui.centralwidget)
                    self.widget.setText("")
                    self.widget.setAlignment(QtCore.Qt.AlignCenter)
                    self.widget.setPlaceholderText('...')
                    self.widget.show()
                    self.widget_x += 40
                    self.widget.setValidator(QIntValidator(-1000, 100))
                    self.widget.setGeometry(QtCore.QRect(self.widget_x, self.widget_y, 30, 30))
                    e.append(self.widget)
                self.widget_y += 50
        elif matrix == "B":
            for i in self.matrix_B:
                for n in i:
                    try:
                        n.deleteLater()
                    except Exception:
                        pass
            self.matrix_B = []

            for i in range(0, self.count_of_columns_B):
                self.matrix_B.append([])

            self.widget_y = self.START_B_INPUT_Y

            for e in self.matrix_B:
                self.widget_x = 0
                for i in range(0, self.count_of_rows_B):
                    self.widget = QtWidgets.QLineEdit(self.ui.centralwidget)
                    self.widget.setText("")
                    self.widget.setAlignment(QtCore.Qt.AlignCenter)
                    self.widget.setPlaceholderText('...')
                    self.widget.show()
                    self.widget.setValidator(QIntValidator(-1000, 100))
                    self.widget_x += 40
                    self.widget.setGeometry(QtCore.QRect(self.widget_x + 420, self.widget_y, 30, 30))
                    e.append(self.widget)
                self.widget_y += 50

    def show_result(self, result):
        self.result = ''''''
        for i in result:
            for n in i:
                self.result += (" " + str(n) + " ")
            self.result += '\n'
        self.ui.result.setText(str(self.result))
        self.ui.result.adjustSize()
        self.ui.result.show()

    def get_matrix_content(self, matrix, type_of_matrix):
        if type_of_matrix == 'first_multiplier':
            matrix_content = []

            for i in matrix:
                matrix_content_buff = []
                for n in i:
                    try:
                        matrix_content_buff.append(int(n.text()))
                    except Exception:
                        self.ui.multiplierError.setText('Матрица A не заполнена')
                        self.start_error_animation()
                        return
                matrix_content.append(matrix_content_buff)

            print('MATRIX A: ', matrix_content)
            return matrix_content

        elif type_of_matrix == 'second_multiplier':
            matrix_content = []

            for i in range(0, len(matrix[0])):
                matrix_content_buff = []
                for n in matrix:
                    try:
                        matrix_content_buff.append(int(n[i].text()))
                    except Exception:
                        self.ui.multiplierError.setText('Матрица B не заполнена')
                        self.start_error_animation()
                        return
                matrix_content.append(matrix_content_buff)
            print('MATRIX B: ', matrix_content)

            return matrix_content

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    load = CalcWindow()
    sys.exit(app.exec_())