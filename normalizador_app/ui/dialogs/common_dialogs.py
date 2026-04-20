from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


def show_text_dialog(parent, title: str, text: str, size=(680, 480), tr=None):
    tr = tr or (lambda key, **kwargs: key)
    dialog = QDialog(parent)
    dialog.setWindowTitle(title)
    dialog.resize(*size)
    layout = QVBoxLayout(dialog)

    text_box = QTextEdit()
    text_box.setObjectName("monoText")
    text_box.setReadOnly(True)
    text_box.setPlainText(text)
    layout.addWidget(text_box)

    button = QPushButton(tr("dialog_close"))
    button.clicked.connect(dialog.accept)
    layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignRight)
    dialog.exec()


def open_settings_dialog(parent, input_value: str, output_value: str, tr=None):
    tr = tr or (lambda key, **kwargs: key)
    dialog = QDialog(parent)
    dialog.setWindowTitle(tr("settings_title"))
    dialog.resize(620, 210)
    layout = QVBoxLayout(dialog)

    form = QFormLayout()
    input_path = QLineEdit(input_value)
    output_path = QLineEdit(output_value)

    input_row = QWidget(dialog)
    input_row_layout = QHBoxLayout(input_row)
    input_row_layout.setContentsMargins(0, 0, 0, 0)
    input_row_layout.setSpacing(8)
    input_row_layout.addWidget(input_path)
    btn_input_browse = QPushButton(tr("settings_browse"))
    btn_input_browse.setFixedWidth(100)
    input_row_layout.addWidget(btn_input_browse)

    output_row = QWidget(dialog)
    output_row_layout = QHBoxLayout(output_row)
    output_row_layout.setContentsMargins(0, 0, 0, 0)
    output_row_layout.setSpacing(8)
    output_row_layout.addWidget(output_path)
    btn_output_browse = QPushButton(tr("settings_browse"))
    btn_output_browse.setFixedWidth(100)
    output_row_layout.addWidget(btn_output_browse)

    form.addRow(tr("settings_input"), input_row)
    form.addRow(tr("settings_output"), output_row)
    layout.addLayout(form)

    buttons = QHBoxLayout()
    save_btn = QPushButton(tr("settings_save"))
    save_btn.setObjectName("primary")
    cancel_btn = QPushButton(tr("settings_cancel"))
    buttons.addStretch()
    buttons.addWidget(cancel_btn)
    buttons.addWidget(save_btn)
    layout.addLayout(buttons)

    result = {"accepted": False, "input": input_value, "output": output_value}

    def choose_input_folder():
        selected = QFileDialog.getExistingDirectory(dialog, tr("pick_input_folder"))
        if selected:
            input_path.setText(selected)

    def choose_output_folder():
        selected = QFileDialog.getExistingDirectory(dialog, tr("pick_output_folder"))
        if selected:
            output_path.setText(selected)

    def on_save():
        result["accepted"] = True
        result["input"] = input_path.text()
        result["output"] = output_path.text()
        dialog.accept()

    save_btn.clicked.connect(on_save)
    cancel_btn.clicked.connect(dialog.reject)
    btn_input_browse.clicked.connect(choose_input_folder)
    btn_output_browse.clicked.connect(choose_output_folder)

    dialog.exec()
    return result
