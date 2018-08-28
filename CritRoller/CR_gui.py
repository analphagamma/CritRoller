#!/usr/local/bin/python3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys, os
from dbhandler import DBHandler



class CreateDBWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(CreateDBWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle('New DB')

        layout = QVBoxLayout()
        layout_b = QHBoxLayout()

        text_w = QLabel('Enter database name:')
        layout.addWidget(text_w)
        
        self.db_name = QLineEdit()
        layout.addWidget(self.db_name)

        confirm_button = QPushButton('Confirm')
        cancel_button = QPushButton('Cancel')
        layout_b.addWidget(confirm_button)
        layout_b.addWidget(cancel_button)
        confirm_button.pressed.connect(self.confirm_create)
        cancel_button.pressed.connect(self.cancel_create)

        layout.addLayout(layout_b)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def confirm_create(self):
        db_filename = self.db_name.text() + '.sqlite'
        global dbobj
        dbobj = DBHandler(db_filename)
        dbobj.initialize_db()
        self.close()
        
    def cancel_create(self):
        self.close()



class AddWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(AddWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle('Add a Crit or a Fumble')
        layout = QGridLayout()
        
        #Textboxes
        self.author = QLineEdit()
        layout.addWidget(self.author, 1, 0)
        self.name = QLineEdit()
        layout.addWidget(self.author, 1, 0)
        layout.addWidget(self.name, 3, 0)
        self.text_body = QTextEdit()
        layout.addWidget(self.text_body, 5, 0)
        
        
        layout.addWidget(QLabel('Author'), 0, 0)
        layout.addWidget(QLabel('Name'), 2, 0)
        layout.addWidget(QLabel('Text'), 4, 0)

        #Dropdown menu - category 
        self.dropdown = QComboBox()
        self.dropdown.addItem('--Choose category--')
        self.dropdown.addItem('Crit')
        self.dropdown.addItem('Fumble')
        layout.addWidget(self.dropdown, 0, 3)

        #Dropdown menu - crit type
        self.dropdown2 = QComboBox()
        self.dropdown2.addItem('--Choose attack type--')
        self.dropdown2.addItem('magic')
        self.dropdown2.addItem('bludgeoning')
        self.dropdown2.addItem('piercing')
        self.dropdown2.addItem('slashing')
        layout.addWidget(self.dropdown2, 3, 3)

        #Text area
        self.text_area = QLabel('')
        layout.addWidget(self.text_area, 6, 0)
        
        #Buttons
        confirm_button = QPushButton('Confirm')
        confirm_button.pressed.connect(self.confirm_action)
        layout.addWidget(confirm_button, 6, 2)

        cancel_button = QPushButton('Cancel')
        cancel_button.pressed.connect(self.close_window)
        layout.addWidget(cancel_button, 6, 3)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def confirm_action(self):
        dbobj.add_entry(self.dropdown.currentText(),
                        self.author.text(),
                        self.name.text(),
                        self.text_body.toPlainText(),
                        self.dropdown2.currentText())

        self.text_area.setText('Entry added.\n' + self.name.text())
        self.author.clear()
        self.name.clear()
        self.text_body.clear()
        
    def close_window(self):
        self.close()

    

class AboutWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(AboutWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle('About')

        layout = QVBoxLayout()

        about_text = '''
        CritRoller alpha version

        Created by: Peter Bocz 2018
        Source code: http://github.com/analphagamma/CritRoller

        This software is under Creative Commons licence.
        You are free to share, use and modify this software
        for non-commercial uses but
        you must cite the original creator\'s name.'''

        layout.addWidget(QLabel(about_text))

        back = QPushButton('Back')
        back.pressed.connect(self.close_window)
        layout.addWidget(back)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def close_window(self):
        self.close()


        
class HelpWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(HelpWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle('Help')

        layout = QVBoxLayout()

        with open('../README.txt', 'r') as f: help_text = f.read()

        layout.addWidget(QLabel(help_text))

        back = QPushButton('Back')
        back.pressed.connect(self.close_window)
        layout.addWidget(back)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def close_window(self):
        self.close()



class ResetWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(ResetWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle('Reset \'used\' tags')

        layout = QHBoxLayout()
        layout2 = QVBoxLayout()
        
        #Reset button
        reset_button_crit = QPushButton('Reset \'used\' Crits!')
        layout.addWidget(reset_button_crit)
        self.reset_crit_dialog = ResetConfirmWindowCrit(self)
        reset_button_crit.pressed.connect(self.reset_crit_action)
        
        reset_button_fumble = QPushButton('Reset \'used\' Fumbles!')
        layout.addWidget(reset_button_fumble)
        self.reset_fumble_dialog = ResetConfirmWindowFumble(self)
        reset_button_fumble.pressed.connect(self.reset_fumble_action)

        cancel_button = QPushButton('Cancel')
        layout2.addWidget(cancel_button)
        cancel_button.pressed.connect(self.cancel_action)

        layout.addLayout(layout2)
        widget = QWidget()
        widget.setLayout(layout)
        
        self.setCentralWidget(widget)

    def reset_crit_action(self):
        self.reset_crit_dialog.show()

    def reset_fumble_action(self):
        self.reset_fumble_dialog.show()

    def cancel_action(self):
        self.close()

        
class ResetConfirmWindowCrit(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(ResetConfirmWindowCrit, self).__init__(*args, **kwargs)

        self.setWindowTitle('Confirm reset?')

        layout = QVBoxLayout()
        layout_b = QVBoxLayout()

        layout.addWidget(QLabel('Are you sure you want to reset the crits?'))

        confirm_button = QPushButton('Confirm')
        cancel_button = QPushButton('Cancel')
        layout_b.addWidget(confirm_button)
        layout_b.addWidget(cancel_button)
        confirm_button.pressed.connect(self.confirm_reset)
        cancel_button.pressed.connect(self.cancel_reset)

        layout.addLayout(layout_b)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def confirm_reset(self):
        dbobj.reset_used('Crits')
        self.close()

    def cancel_reset(self):
        self.close()


        
class ResetConfirmWindowFumble(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(ResetConfirmWindowFumble, self).__init__(*args, **kwargs)

        self.setWindowTitle('Confirm reset?')

        layout = QVBoxLayout()
        layout_b = QHBoxLayout()

        layout.addWidget(QLabel('Are you sure you want to reset the fumbles?'))

        confirm_button = QPushButton('Confirm')
        cancel_button = QPushButton('Cancel')
        layout_b.addWidget(confirm_button)
        layout_b.addWidget(cancel_button)
        confirm_button.pressed.connect(self.confirm_reset)
        cancel_button.pressed.connect(self.cancel_reset)

        layout.addLayout(layout_b)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def confirm_reset(self):
        dbobj.reset_used('Fumbles')
        self.close()

    def cancel_reset(self):
        self.close()

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle('CritRoller')
        
        layout_reset = QVBoxLayout()
        layout_main = QHBoxLayout()
        layout_text = QVBoxLayout()
        layout_dropdown = QVBoxLayout()
        layout_checkbox = QVBoxLayout()

        ####################################
        
        #Menu
        menu = self.menuBar()

        file_menu = menu.addMenu('&Menu')
        about_menu = menu.addMenu('&About')
        
        #Menu actions
        createdb_action = QAction('Create Database...', self)
        createdb_action.setStatusTip('Creates a new set of crits/fumbles')
        createdb_action.triggered.connect(self.create_database)
        self.create_dialog = CreateDBWindow(self)

        add_action = QAction('Add Crit/Fumble...', self)
        add_action.setStatusTip('Add a new entry to the current database')
        add_action.triggered.connect(self.add_menu)
        self.add_dialog = AddWindow(self)

        reset_action = QAction('Reset \'used\' tags...', self)
        reset_action.setStatusTip('Remove the used tag so it can be rolled again')
        reset_action.triggered.connect(self.reset_action)
        self.reset_dialog = ResetWindow(self)
        
        exit_action = QAction('&Exit', self)
        exit_action.setStatusTip('Exit the application')
        exit_action.triggered.connect(self.on_exit_click)
        
        file_menu.addAction(createdb_action)
        file_menu.addAction(add_action)
        file_menu.addAction(reset_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        #About menu actions
        help_action = QAction('Help', self)
        help_action.setStatusTip('Opens the Readme')
        help_action.triggered.connect(self.open_help)
        self.help_dialog = HelpWindow(self)

        about_action = QAction('About', self)
        about_action.setStatusTip('About the application and the creator')
        about_action.triggered.connect(self.open_about)

        about_menu.addAction(help_action)
        about_menu.addAction(about_action)
        self.about_dialog = AboutWindow(self)

        ####################################
        
        #Dropdown - current database
        self.db_dropdown = QComboBox()
        self.db_dropdown.addItem('--Select database--')
        for item in self.get_db_files():
            self.db_dropdown.addItem(item[:-7])
        layout_dropdown.addWidget(self.db_dropdown)

        #Dropdown - weapon type
        self.wt_dropdown = QComboBox()
        self.wt_dropdown.addItem('--Select attack type--')
        self.wt_dropdown.addItem('magic')
        self.wt_dropdown.addItem('bludgeoning')
        self.wt_dropdown.addItem('piercing')
        self.wt_dropdown.addItem('slashing')
        layout_dropdown.addWidget(self.wt_dropdown)
        
        #Checkbox
        self.checkbox = QCheckBox('Use all?')
        layout_checkbox.addWidget(self.checkbox)
        
        #Main buttons
        crit_button = QPushButton('Roll a Crit!')
        fumb_button = QPushButton('Roll a Fumble!')

        crit_button.pressed.connect(self.roll_crit)
        fumb_button.pressed.connect(self.roll_fumble)

        layout_main.addWidget(crit_button)
        layout_main.addWidget(fumb_button)
        
        #Label
        self.textlabel = QLabel('')
        self.textlabel.setFrameShape(QFrame.Panel)
        self.textlabel.setFrameShadow(QFrame.Sunken)
        self.textlabel.setAlignment(Qt.AlignCenter)
        layout_text.addWidget(self.textlabel)

        #Layout-nesting
        layout_reset.addLayout(layout_checkbox)
        layout_reset.addLayout(layout_dropdown)
        layout_reset.addLayout(layout_main)
        layout_reset.addLayout(layout_text)
        
        widget = QWidget()
        widget.setLayout(layout_reset)
        
        self.setCentralWidget(widget)

    def get_db_files(self):
        return [f for f in os.listdir('databases') if f[-7:] == '.sqlite']

    def create_database(self):
        self.create_dialog.show()

    def roll(self, crit_type, database, weapon_type):

        if database == '--Select database--' or weapon_type == '--Select weapon type--':
            self.textlabel.setText('Invalid input.\nCheck the dropdown menus.')
            return
            
        db_filename = database + '.sqlite'
        global dbobj
        dbobj = DBHandler(db_filename)
        
        if self.checkbox.isChecked():
            crit = dbobj.select_random(crit_type, 1, weapon_type)
            if crit == None:
                self.textlabel.setText('No crits in the database!')
                return
        else:
            crit = dbobj.select_random(crit_type, 0, weapon_type)
            if crit == None:
                self.textlabel.setText('No more unused crits.\nUntick \'used\' box or reset')
                return
            dbobj.set_used(crit[2], crit_type)
                
        crittext = 'Author: {}\nName: {}\n\n{}'.format(crit[1], crit[2], crit[3])
        self.textlabel.setText(crittext)
        
    def roll_fumble(self):
        self.roll('Fumble', self.db_dropdown.currentText(), self.wt_dropdown.currentText())
        
    def roll_crit(self):
        self.roll('Crit', self.db_dropdown.currentText(), self.wt_dropdown.currentText())
        
    def add_menu(self):
        self.add_dialog.show()

    def reset_action(self):
        self.reset_dialog.show()

    def open_help(self):
        self.help_dialog.show()

    def open_about(self):
        self.about_dialog.show()

    def on_exit_click(self):
        sys.exit(0)



