from __future__ import annotations

import json

from PySide6 import QtCore, QtGui, QtWidgets

from app.frontend.services.api_client import ApiClient
from app.frontend.viewmodels.request_vm import RequestViewModel


class JsonEditor(QtWidgets.QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.setTabStopDistance(4 * self.fontMetrics().horizontalAdvance(" "))
        self._format_timer = QtCore.QTimer(self)
        self._format_timer.setSingleShot(True)
        self._format_timer.timeout.connect(self._format_if_valid)
        self.textChanged.connect(self._schedule_format)

    def _schedule_format(self) -> None:
        self._format_timer.start(600)

    def _format_if_valid(self) -> None:
        text = self.toPlainText().strip()
        if not text:
            return
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            return

        formatted = json.dumps(parsed, indent=2, ensure_ascii=False, sort_keys=True)
        if formatted == text:
            return

        cursor = self.textCursor()
        old_pos = cursor.position()
        self.setPlainText(formatted)
        new_pos = min(old_pos, len(formatted))
        cursor.setPosition(new_pos)
        self.setTextCursor(cursor)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        pairs = {"\"": "\"", "{": "}", "[": "]", "(": ")"}
        key = event.text()

        if key in pairs and not self.textCursor().hasSelection():
            cursor = self.textCursor()
            cursor.insertText(key + pairs[key])
            cursor.movePosition(QtGui.QTextCursor.Left)
            self.setTextCursor(cursor)
            return

        if event.key() in (QtCore.Qt.Key_Backspace,):
            cursor = self.textCursor()
            if not cursor.hasSelection():
                pos = cursor.position()
                doc = self.document()
                if pos > 0:
                    left_char = doc.characterAt(pos - 1)
                    right_char = doc.characterAt(pos)
                    if left_char in pairs and right_char == pairs[left_char]:
                        cursor.setPosition(pos + 1)
                        cursor.deletePreviousChar()
                        cursor.deletePreviousChar()
                        return

        if event.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
            cursor = self.textCursor()
            cursor.movePosition(QtGui.QTextCursor.StartOfLine)
            cursor.movePosition(QtGui.QTextCursor.EndOfLine, QtGui.QTextCursor.KeepAnchor)
            line_text = cursor.selectedText()
            indent = len(line_text) - len(line_text.lstrip(" "))
            extra = 2 if line_text.rstrip().endswith(("{", "[")) else 0
            super().keyPressEvent(event)
            self.insertPlainText(" " * (indent + extra))
            return

        if key in ("}", "]", ")"):
            cursor = self.textCursor()
            cursor.movePosition(QtGui.QTextCursor.Right, QtGui.QTextCursor.KeepAnchor)
            next_char = cursor.selectedText()
            if next_char == key:
                cursor.clearSelection()
                cursor.movePosition(QtGui.QTextCursor.Right)
                self.setTextCursor(cursor)
                return

        super().keyPressEvent(event)


class RequestTab(QtWidgets.QWidget):
    def __init__(self, vm: RequestViewModel):
        super().__init__()
        self.vm = vm
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QtWidgets.QVBoxLayout(self)

        top_bar = QtWidgets.QHBoxLayout()
        self.method_combo = QtWidgets.QComboBox()
        self.method_combo.addItems(["GET", "POST", "PUT", "PATCH", "DELETE"])
        self.url_input = QtWidgets.QLineEdit()
        self.url_input.setPlaceholderText("https://api.example.com/v1/resource")
        self.url_input.setText("http://127.0.0.1:8001/api/")
        self.env_combo = QtWidgets.QComboBox()
        self.env_combo.setMinimumWidth(180)
        self.format_btn = QtWidgets.QPushButton("Format JSON")
        self.send_btn = QtWidgets.QPushButton("Send")

        top_bar.addWidget(self.method_combo)
        top_bar.addWidget(self.url_input, 1)
        top_bar.addWidget(self.env_combo)
        top_bar.addWidget(self.format_btn)
        top_bar.addWidget(self.send_btn)

        layout.addLayout(top_bar)

        splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation.Vertical)
        layout.addWidget(splitter, 1)

        editor_tabs = QtWidgets.QTabWidget()
        self.headers_editor = JsonEditor()
        self.headers_editor.setPlaceholderText('{"Accept": "application/json"}')
        self.headers_editor.setPlainText('{"Accept": "application/json"}')
        self.params_editor = JsonEditor()
        self.params_editor.setPlaceholderText('{"page": "1"}')
        self.body_editor = JsonEditor()
        self.body_editor.setPlaceholderText('{"name": "John"}')
        self.auth_editor = JsonEditor()
        self.auth_editor.setPlaceholderText('{"type": "bearer", "token": "..."}')

        editor_tabs.addTab(self.headers_editor, "Headers")
        editor_tabs.addTab(self.params_editor, "Params")
        editor_tabs.addTab(self.body_editor, "Body")
        editor_tabs.addTab(self.auth_editor, "Auth")

        splitter.addWidget(editor_tabs)

        response_box = QtWidgets.QGroupBox("Response")
        response_layout = QtWidgets.QVBoxLayout(response_box)
        self.response_meta = QtWidgets.QLabel("Status: - | Time: -ms | Size: -")
        self.response_view = QtWidgets.QPlainTextEdit()
        self.response_view.setReadOnly(True)
        response_layout.addWidget(self.response_meta)
        response_layout.addWidget(self.response_view, 1)

        splitter.addWidget(response_box)

        self.send_btn.clicked.connect(self._on_send)
        self.format_btn.clicked.connect(self._format_all)

    def set_envs(self, envs: list[dict]) -> None:
        self.env_combo.clear()
        self.env_combo.addItem("(no env)", None)
        for env in envs:
            self.env_combo.addItem(env.get("name", "env"), env.get("id"))

    def _format_all(self) -> None:
        for editor in (self.headers_editor, self.params_editor, self.body_editor, self.auth_editor):
            self._format_json_editor(editor)

    def _format_json_editor(self, editor: QtWidgets.QPlainTextEdit) -> None:
        text = editor.toPlainText().strip()
        if not text:
            return
        parsed = json.loads(text)
        editor.setPlainText(json.dumps(parsed, indent=2, ensure_ascii=False, sort_keys=True))

    def _on_send(self) -> None:
        try:
            self._format_all()
            headers = self._parse_json(self.headers_editor.toPlainText())
            params = self._parse_json(self.params_editor.toPlainText())
            body = self._parse_json(self.body_editor.toPlainText(), allow_any=True)
            auth = self._parse_json(self.auth_editor.toPlainText())
        except json.JSONDecodeError as exc:
            self.response_view.setPlainText(f"Invalid JSON: {exc}")
            return

        if headers is None or params is None or auth is None:
            self.response_view.setPlainText("Headers, Params, and Auth must be JSON objects")
            return

        payload = {
            "method": self.method_combo.currentText(),
            "url": self.url_input.text().strip(),
            "headers": headers,
            "params": params,
            "body_type": "json" if body else "none",
            "body": body,
            "auth": auth or {"type": "none"},
            "env_id": self.env_combo.currentData(),
        }

        if not payload["url"]:
            self.response_view.setPlainText("URL is required")
            return

        try:
            response = self.vm.execute(payload)
        except Exception as exc:
            self.response_view.setPlainText(f"Request failed: {exc}")
            return

        self.response_meta.setText(
            f"Status: {response.get('status_code')} | Time: {response.get('duration_ms')}ms | Size: {response.get('size_bytes')}"
        )

        body_out = response.get("body")
        if isinstance(body_out, (dict, list)):
            self.response_view.setPlainText(json.dumps(body_out, indent=2, ensure_ascii=False))
        else:
            self.response_view.setPlainText(str(body_out))

    @staticmethod
    def _parse_json(text: str, allow_any: bool = False):
        if not text.strip():
            return {} if not allow_any else None
        parsed = json.loads(text)
        if allow_any:
            return parsed
        return parsed if isinstance(parsed, dict) else None


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kanjakitude - MyPostman")
        self.resize(1200, 800)

        self.client = ApiClient()
        self.vm = RequestViewModel(self.client)
        self.envs_cache: list[dict] = []

        self._build_ui()
        self._load_envs()
        self._add_request_tab()

    def _build_ui(self) -> None:
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)

        layout = QtWidgets.QVBoxLayout(central)

        top_bar = QtWidgets.QHBoxLayout()
        self.new_tab_btn = QtWidgets.QPushButton("New Request")
        self.reload_envs_btn = QtWidgets.QPushButton("Reload Envs")
        top_bar.addWidget(self.new_tab_btn)
        top_bar.addWidget(self.reload_envs_btn)
        top_bar.addStretch(1)
        layout.addLayout(top_bar)

        self.request_tabs = QtWidgets.QTabWidget()
        self.request_tabs.setTabsClosable(True)
        self.request_tabs.tabCloseRequested.connect(self._close_tab)
        self.request_tabs.tabBarDoubleClicked.connect(self._rename_tab)
        layout.addWidget(self.request_tabs, 1)

        self.new_tab_btn.clicked.connect(self._add_request_tab)
        self.reload_envs_btn.clicked.connect(self._load_envs)

    def _add_request_tab(self) -> None:
        tab = RequestTab(self.vm)
        tab.set_envs(self.envs_cache)
        index = self.request_tabs.addTab(tab, f"Request {self.request_tabs.count() + 1}")
        self.request_tabs.setCurrentIndex(index)

    def _close_tab(self, index: int) -> None:
        if self.request_tabs.count() <= 1:
            return
        widget = self.request_tabs.widget(index)
        self.request_tabs.removeTab(index)
        if widget is not None:
            widget.deleteLater()

    def _rename_tab(self, index: int) -> None:
        if index < 0:
            return
        current = self.request_tabs.tabText(index)
        new_name, ok = QtWidgets.QInputDialog.getText(
            self,
            "Rename Request",
            "New tab name:",
            QtWidgets.QLineEdit.Normal,
            current,
        )
        if ok and new_name.strip():
            self.request_tabs.setTabText(index, new_name.strip())

    def _load_envs(self) -> None:
        try:
            self.envs_cache = self.vm.list_envs()
        except Exception:
            self.envs_cache = []

        for i in range(self.request_tabs.count()):
            widget = self.request_tabs.widget(i)
            if isinstance(widget, RequestTab):
                widget.set_envs(self.envs_cache)
