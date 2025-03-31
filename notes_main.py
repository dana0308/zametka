import json
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout, QTextEdit, \
    QLabel, QListWidget, QPushButton, QLineEdit, QInputDialog, QMessageBox

app = QApplication([])
window = QWidget()
window.setWindowTitle('Умные заметки')
window.setWindowIcon(QtGui.QIcon('note.png'))

window.setMinimumSize(900, 600)

main_layout = QHBoxLayout()
col_left = QVBoxLayout()
text_note = QTextEdit()
col_left.addWidget(text_note)

col_right = QVBoxLayout()

layout1 = QVBoxLayout()

lst_notes_label = QLabel('Список заметок:')
layout1.addWidget(lst_notes_label)

lst_notes = QListWidget()
layout1.addWidget(lst_notes)

layout2 = QHBoxLayout()

btn_create_note = QPushButton('Создать заметку')
layout2.addWidget(btn_create_note)

btn_delete_note = QPushButton('Удалить заметку')
layout2.addWidget(btn_delete_note)

layout3 = QVBoxLayout()

btn_save_note = QPushButton('Сохранить заметку')
layout3.addWidget(btn_save_note)

tags_label = QLabel('Список тегов:')
layout3.addWidget(tags_label)

lst_tags = QListWidget()
layout3.addWidget(lst_tags)

edit_tag = QLineEdit()
edit_tag.setPlaceholderText('Введите тег...')
layout3.addWidget(edit_tag)

layout4 = QHBoxLayout()

btn_add_tag = QPushButton('Добавить к заметке')
layout4.addWidget(btn_add_tag)

btn_delete_tag = QPushButton('Открепить от заметки')
layout4.addWidget(btn_delete_tag)

layout5 = QHBoxLayout()
btn_search_by_tag = QPushButton('Искать заметки по тегу')
layout5.addWidget(btn_search_by_tag)

col_right.addLayout(layout1)
col_right.addLayout(layout2)
col_right.addLayout(layout3)
col_right.addLayout(layout4)
col_right.addLayout(layout5)
col_right.setSpacing(16)

main_layout.addLayout(col_left)
main_layout.addLayout(col_right)
window.setLayout(main_layout)

try:
    with open('notes.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
except FileNotFoundError:
    data = {}

lst_notes.addItems(data.keys())

def show_note():
    note_name = lst_notes.currentItem().text()
    n_text = data[note_name]["text"]
    n_tags = data[note_name]["tags"]

    text_note.setText(n_text)
    lst_tags.clear()
    lst_tags.addItems(n_tags)

lst_notes.itemClicked.connect(show_note)

def create_note():
    note_name, result = QInputDialog.getText(window, \
        "Добавить заметку", "Название заметки:")
    if result and not note_name in data.keys() and note_name != '':
        data[note_name] = {
        "text" : "",
        "tags" : []
    	}
        lst_notes.addItem(note_name)


btn_create_note.clicked.connect(create_note)

def save_all():
    with open('notes.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def save_note():
    if lst_notes.currentItem():
        note_name = lst_notes.currentItem().text()
        data[note_name]['text'] = text_note.toPlainText()
        save_all()

btn_save_note.clicked.connect(save_note)

def delete_note():
    if lst_notes.currentItem():
        note_name = lst_notes.currentItem().text()
        del data[note_name]

        cur_row = lst_notes.currentRow()
        lst_notes.takeItem(cur_row)

        lst_tags.clear()
        text_note.clear()
        
btn_delete_note.clicked.connect(delete_note)

def add_tag():
    tag_name, result = QInputDialog.getText(window, \
        "Добавить тег к заметке", "Название тега:")
    if lst_notes.currentItem() and result and len(tag_name) > 0:
        note_name = lst_notes.currentItem().text()
        data[note_name]['tags'].append(tag_name)
        lst_tags.addItem(tag_name)
        save_all()

btn_add_tag.clicked.connect(add_tag)

def delete_tag():
    if lst_notes.currentItem() and lst_tags.currentItem():
        note_name = lst_notes.currentItem().text()
        tag_name = lst_tags.currentItem().text()
        data[note_name]['tags'].remove(tag_name)

        cur_row = lst_tags.currentRow()
        lst_tags.takeItem(cur_row)
        save_all()

btn_delete_tag.clicked.connect(delete_tag)

def find_by_tag():
    if btn_search_by_tag.text() != 'Сбросить результаты поиска':
        if len(edit_tag.text()) > 0:
            text_to_find = edit_tag.text()
            result = {}
            for key, value in data.items():
                if text_to_find in value['tags']:
                    result[key] = value
            
            lst_notes.clear()
            lst_tags.clear()
            text_note.clear()
            lst_notes.addItems(result.keys())

            btn_search_by_tag.setText('Сбросить результаты поиска')
        else:
            msg = QMessageBox.warning(window, 'Предупреждение', 'Вы не ввели тег для поиска')
    else:
        lst_notes.clear()
        lst_tags.clear()
        text_note.clear()
        lst_notes.addItems(data.keys())
        btn_search_by_tag.setText('Искать заметки по тегу')

btn_search_by_tag.clicked.connect(find_by_tag)

window.show()
app.exec_()
