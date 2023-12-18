import sys
import pickle
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QTreeWidget, QTreeWidgetItem,
    QComboBox, QCalendarWidget, QLabel, QDialog, QDialogButtonBox,
    QMenu, QAction, QTextBrowser, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton



class ToDoListGUI(QWidget):
    def __init__(self, username):
        super().__init__()

        self.username = username
        self.tasks = []

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Enhanced To-Do List')
        self.setGeometry(100, 100, 800, 600)

        # Buttons
        add_task_button = QPushButton('Add Task', self)
        add_task_button.clicked.connect(self.add_task)
        self.style_button(add_task_button, "#2ecc71", font_size=1.2)  # Green color

        mark_complete_button = QPushButton('Mark Complete', self)
        mark_complete_button.clicked.connect(self.mark_complete)
        self.style_button(mark_complete_button, "#3498db", font_size=1.2)  # Blue color

        edit_task_button = QPushButton('Edit Task', self)
        edit_task_button.clicked.connect(self.edit_task)
        self.style_button(edit_task_button, "#e67e22", font_size=1.2)  # Orange color

        add_subtask_button = QPushButton('Add Subtask', self)
        add_subtask_button.clicked.connect(self.add_subtask)
        self.style_button(add_subtask_button, "#9b59b6", font_size=1.2)  # Purple color

        set_deadline_button = QPushButton('Set Deadline', self)
        set_deadline_button.clicked.connect(self.set_deadline)
        self.style_button(set_deadline_button, "#d35400", font_size=1.2)  # Pumpkin color

        filter_tasks_combo = QComboBox(self)
        filter_tasks_combo.addItems(["All", "Incomplete", "Complete"])
        filter_tasks_combo.currentIndexChanged.connect(self.filter_tasks)
        filter_tasks_combo.setStyleSheet("QComboBox { border: 2px solid #3498db; border-radius: 10px; padding: 5px; font-size: 1.1em; }")

        view_details_button = QPushButton('View Details', self)
        view_details_button.clicked.connect(self.view_details)
        self.style_button(view_details_button, "#8e44ad", font_size=1.2)  # Purple color

        save_button = QPushButton('Save To-Do List', self)
        save_button.clicked.connect(self.save_to_file)
        self.style_button(save_button, "#27ae60", font_size=1.2)  # Green color

        load_button = QPushButton('Load To-Do List', self)
        load_button.clicked.connect(self.load_from_file)
        self.style_button(load_button, "#c0392b", font_size=1.2)  # Red color

        # Task Entry
        self.task_entry = QLineEdit(self)
        self.task_entry.setPlaceholderText("Enter task...")
        self.task_entry.setStyleSheet("QLineEdit { border: 2px solid #3498db; border-radius: 10px; padding: 5px; font-size: 1.2em; }")

        # Due Date Picker
        self.due_date_picker = QCalendarWidget(self)
        self.due_date_picker.setStyleSheet("QCalendarWidget QAbstractItemView { selection-background-color: #3498db; }")

        # Priority ComboBox
        self.priority_combo = QComboBox(self)
        self.priority_combo.addItems(["Low", "Medium", "High"])
        self.priority_combo.setStyleSheet("QComboBox { border: 2px solid #3498db; border-radius: 10px; padding: 5px; font-size: 1.1em; }")

        # Task List
        self.task_tree = QTreeWidget(self)
        self.task_tree.setHeaderLabels(['Task', 'Due Date', 'Priority', 'Status', 'Deadline'])
        self.task_tree.setStyleSheet("QTreeWidget { border: 2px solid #3498db; border-radius: 10px; padding: 5px; font-size: 1.1em; }")
        self.task_tree.setDragDropMode(QTreeWidget.InternalMove)
        self.task_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.task_tree.customContextMenuRequested.connect(self.show_context_menu)
        self.task_tree.itemDoubleClicked.connect(self.view_details)

        # Task Details
        self.task_details_browser = QTextBrowser(self)
        self.task_details_browser.setStyleSheet("QTextBrowser { border: 2px solid #3498db; border-radius: 10px; padding: 5px; font-size: 1.1em; }")
        self.task_details_browser.setReadOnly(True)

        # Layout
        vbox = QVBoxLayout()

        vbox.addWidget(add_task_button)

        vbox.addWidget(self.task_entry)

        hbox_entry = QHBoxLayout()
        hbox_entry.addWidget(self.due_date_picker)
        hbox_entry.addWidget(self.priority_combo)
        vbox.addLayout(hbox_entry)

        hbox_buttons = QHBoxLayout()
        hbox_buttons.addWidget(mark_complete_button)
        hbox_buttons.addWidget(edit_task_button)
        hbox_buttons.addWidget(add_subtask_button)
        hbox_buttons.addWidget(set_deadline_button)
        vbox.addLayout(hbox_buttons)

        vbox.addWidget(filter_tasks_combo)

        vbox.addWidget(self.task_tree)

        vbox.addWidget(view_details_button)

        hbox_save_load = QHBoxLayout()
        hbox_save_load.addWidget(save_button)
        hbox_save_load.addWidget(load_button)
        vbox.addLayout(hbox_save_load)

        vbox.addWidget(self.task_details_browser)

        vbox.addStretch()  # Add stretch to push all widgets to the top

        self.setLayout(vbox)

    def style_button(self, button, color, font_size=1.0):
        button.setStyleSheet(f"QPushButton {{ background-color: {color}; color: white; border: none; border-radius: 8px; padding: 10px; font-size: {font_size}em; }}")
        button.setCursor(Qt.PointingHandCursor)

    def add_task(self):
        task = self.task_entry.text()
        if task:
            due_date = self.due_date_picker.selectedDate().toString("yyyy-MM-dd")
            priority = self.priority_combo.currentText()
            status = "Incomplete"
            deadline = ""
            task_item = QTreeWidgetItem([task, due_date, priority, status, deadline])
            self.task_tree.addTopLevelItem(task_item)
            self.tasks.append({'task': task, 'due_date': due_date, 'priority': priority, 'status': status, 'deadline': deadline, 'subtasks': []})
            self.task_entry.clear()
        else:
            pass  # Handle empty task

    def mark_complete(self):
        selected_item = self.task_tree.currentItem()
        if selected_item is not None:
            task = selected_item.text(0)
            task_index = self.find_task_index(task)
            if task_index != -1:
                self.tasks[task_index]['status'] = "Complete"
                selected_item.setText(3, "Complete")
        else:
            pass  # Handle no selected task

    def edit_task(self):
        selected_item = self.task_tree.currentItem()
        if selected_item is not None:
            task = selected_item.text(0)
            task_index = self.find_task_index(task)
            if task_index != -1:
                edited_task, ok = self.show_edit_dialog(task)
                if ok:
                    self.tasks[task_index]['task'] = edited_task
                    selected_item.setText(0, edited_task)
        else:
            pass  # Handle no selected task

    def add_subtask(self):
        selected_item = self.task_tree.currentItem()
        if selected_item is not None:
            task = selected_item.text(0)
            task_index = self.find_task_index(task)
            if task_index != -1:
                subtask, ok = self.show_edit_dialog("Add Subtask")
                if ok:
                    subtask_item = QTreeWidgetItem([subtask, "", "", "Incomplete", ""])
                    selected_item.addChild(subtask_item)
                    self.tasks[task_index]['subtasks'].append({'subtask': subtask, 'status': 'Incomplete', 'deadline': ""})
        else:
            pass  # Handle no selected task

    def set_deadline(self):
        selected_item = self.task_tree.currentItem()
        if selected_item is not None:
            task = selected_item.text(0)
            task_index = self.find_task_index(task)
            if task_index != -1:
                deadline, ok = self.show_edit_dialog("Set Deadline")
                if ok:
                    self.tasks[task_index]['deadline'] = deadline
                    selected_item.setText(4, deadline)
        else:
            pass  # Handle no selected task

    def filter_tasks(self, index):
        filter_text = self.sender().currentText()
        for i in range(self.task_tree.topLevelItemCount()):
            item = self.task_tree.topLevelItem(i)
            if filter_text == "All":
                item.setHidden(False)
            else:
                status = item.text(3)
                if status != filter_text:
                    item.setHidden(True)
                else:
                    item.setHidden(False)

    def view_details(self):
        selected_item = self.task_tree.currentItem()
        if selected_item is not None:
            task = selected_item.text(0)
            task_index = self.find_task_index(task)
            if task_index != -1:
                details = f"Task: {self.tasks[task_index]['task']}\n" \
                          f"Due Date: {self.tasks[task_index]['due_date']}\n" \
                          f"Priority: {self.tasks[task_index]['priority']}\n" \
                          f"Status: {self.tasks[task_index]['status']}\n" \
                          f"Deadline: {self.tasks[task_index]['deadline']}\n" \
                          f"Subtasks:\n"
                for subtask in self.tasks[task_index]['subtasks']:
                    details += f" - {subtask['subtask']} (Status: {subtask['status']}, Deadline: {subtask['deadline']})\n"
                self.task_details_browser.setPlainText(details)
        else:
            pass  # Handle no selected task

    def save_to_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save To-Do List", "", "Pickled Files (*.pkl)")
        if file_path:
            with open(file_path, 'wb') as file:
                pickle.dump(self.tasks, file)

    def load_from_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Load To-Do List", "", "Pickled Files (*.pkl)")
        if file_path:
            with open(file_path, 'rb') as file:
                self.tasks = pickle.load(file)
                self.populate_task_tree()

    def show_edit_dialog(self, title):
        dialog = TaskEditDialog(title)
        result = dialog.exec_()
        edited_text = dialog.get_edited_text()
        return edited_text, result == QDialog.Accepted

    def find_task_index(self, task):
        for i, t in enumerate(self.tasks):
            if t['task'] == task:
                return i
        return -1

    def populate_task_tree(self):
        self.task_tree.clear()
        for task in self.tasks:
            task_item = QTreeWidgetItem([task['task'], task['due_date'], task['priority'], task['status'], task['deadline']])
            for subtask in task['subtasks']:
                subtask_item = QTreeWidgetItem([subtask['subtask'], '', '', subtask['status'], subtask['deadline']])
                task_item.addChild(subtask_item)
            self.task_tree.addTopLevelItem(task_item)

    def show_context_menu(self, position):
        context_menu = QMenu(self)

        selected_item = self.task_tree.itemAt(position)
        if selected_item is not None:
            task_index = self.find_task_index(selected_item.text(0))

            mark_complete_action = QAction("Mark Complete", self)
            mark_complete_action.triggered.connect(self.mark_complete)
            context_menu.addAction(mark_complete_action)

            edit_task_action = QAction("Edit Task", self)
            edit_task_action.triggered.connect(self.edit_task)
            context_menu.addAction(edit_task_action)

            add_subtask_action = QAction("Add Subtask", self)
            add_subtask_action.triggered.connect(self.add_subtask)
            context_menu.addAction(add_subtask_action)

            set_deadline_action = QAction("Set Deadline", self)
            set_deadline_action.triggered.connect(self.set_deadline)
            context_menu.addAction(set_deadline_action)

            context_menu.addSeparator()

            delete_action = QAction("Delete", self)
            delete_action.triggered.connect(self.delete_item)
            context_menu.addAction(delete_action)

            context_menu.exec_(self.task_tree.mapToGlobal(position))

    def delete_item(self):
        selected_item = self.task_tree.currentItem()
        if selected_item is not None:
            task = selected_item.text(0)
            task_index = self.find_task_index(task)
            if task_index != -1:
                parent_item = selected_item.parent()
                if parent_item is not None:
                    parent_index = self.find_task_index(parent_item.text(0))
                    self.tasks[parent_index]['subtasks'].pop(task_index)
                else:
                    self.tasks.pop(task_index)
                self.task_tree.takeTopLevelItem(self.task_tree.indexOfTopLevelItem(selected_item))

    def closeEvent(self, event):
        reply = self.show_close_dialog()
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def show_close_dialog(self):
        close_dialog = QMessageBox()
        close_dialog.setIcon(QMessageBox.Question)
        close_dialog.setWindowTitle("Close Application")
        close_dialog.setText("Are you sure you want to close the application?")
        close_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        close_dialog.setDefaultButton(QMessageBox.No)
        return close_dialog.exec_()


class TaskEditDialog(QDialog):
    def __init__(self, title, parent=None):
        super(TaskEditDialog, self).__init__(parent)

        self.setWindowTitle(title)
        self.setGeometry(200, 200, 400, 100)

        self.init_ui()

    def init_ui(self):
        vbox = QVBoxLayout()

        label = QLabel(f"{self.windowTitle()}:")
        self.text_entry = QLineEdit()
        self.text_entry.setStyleSheet("QLineEdit { border: 2px solid #3498db; border-radius: 8px; padding: 5px; font-size: 1.1em; }")

        vbox.addWidget(label)
        vbox.addWidget(self.text_entry)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, parent=self)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        vbox.addWidget(button_box)

        self.setLayout(vbox)

    def get_edited_text(self):
        return self.text_entry.text()


def main():
    app = QApplication(sys.argv)
    
    # Provide a username when creating an instance of ToDoListGUI
    username = "YourUsername"  # Replace with the actual username
    todo_list_gui = ToDoListGUI(username)
    
    todo_list_gui.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()
