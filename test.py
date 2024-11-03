import io
import sys

from PyQt6 import uic  # Импортируем uic
from PyQt6.QtWidgets import QApplication, QMainWindow

template = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>WINDOW</class>
 <widget class="QMainWindow" name="WINDOW">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>790</width>
    <height>308</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Файловая статистика</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QWidget" name="gridLayoutWidget">
    <property name="geometry">
     <rect>
      <x>0</x>
      <y>0</y>
      <width>801</width>
      <height>281</height>
     </rect>
    </property>
    <layout class="QGridLayout" name="gridLayout">
     <item row="2" column="2">
      <widget class="QLineEdit" name="minEdit">
       <property name="text">
        <string>0</string>
       </property>
      </widget>
     </item>
     <item row="0" column="1">
      <widget class="QLineEdit" name="filenameEdit"/>
     </item>
     <item row="2" column="0" colspan="2">
      <widget class="QLabel" name="label_3">
       <property name="text">
        <string>Минимальное значение:</string>
       </property>
      </widget>
     </item>
     <item row="1" column="0" colspan="2">
      <widget class="QLabel" name="label_2">
       <property name="text">
        <string>Максимальное значение:</string>
       </property>
      </widget>
     </item>
     <item row="0" column="0">
      <widget class="QLabel" name="label">
       <property name="text">
        <string>Имя файла</string>
       </property>
      </widget>
     </item>
     <item row="0" column="2">
      <widget class="QPushButton" name="button">
       <property name="text">
        <string>Рассчитать</string>
       </property>
      </widget>
     </item>
     <item row="1" column="2">
      <widget class="QLineEdit" name="maxEdit">
       <property name="text">
        <string>0</string>
       </property>
      </widget>
     </item>
     <item row="3" column="2">
      <widget class="QLineEdit" name="avgEdit">
       <property name="text">
        <string>0,00</string>
       </property>
      </widget>
     </item>
     <item row="3" column="0" colspan="2">
      <widget class="QLabel" name="label_4">
       <property name="text">
        <string>Среднее значение:</string>
       </property>
      </widget>
     </item>
    </layout>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>790</width>
     <height>26</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
"""


class EmptyFileError(Exception):
    pass


class FileStat(QMainWindow):
    def __init__(self):
        super().__init__()
        f = io.StringIO(template)
        uic.loadUi(f, self)  # Загружаем дизайн

        self.button.clicked.connect(self.f)

    def f(self):
        filename = self.filenameEdit.text()
        try:
            with open(filename) as f:
                numbers = [int(i) for i in f.read().split()]
                if not numbers:
                    raise EmptyFileError

            max_num = max(numbers)
            min_num = min(numbers)
            avg_num = f'{sum(numbers) / len(numbers):.2f}'

            self.maxEdit.setText(str(max_num))
            self.minEdit.setText(str(min_num))
            self.avgEdit.setText(avg_num)
            with open('out.txt', 'w') as f1:
                f1.write(
                    f'Максимальное значение = {max_num}\n'
                    f'Минимальное значение = {min_num}\n'
                    f'Среднее значение = {avg_num}'
                )
        except FileNotFoundError:
            self.statusbar.showMessage('Указанный файл не существует')
            self.maxEdit.setText('0')
            self.minEdit.setText('0')
            self.avgEdit.setText('0,00')
        except ValueError:
            self.statusbar.showMessage('Файл содержит некорректные данные')
            self.maxEdit.setText('0')
            self.minEdit.setText('0')
            self.avgEdit.setText('0,00')
        except EmptyFileError:
            self.statusbar.showMessage('Указанный файл пуст')
            self.maxEdit.setText('0')
            self.minEdit.setText('0')
            self.avgEdit.setText('0,00')


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileStat()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
