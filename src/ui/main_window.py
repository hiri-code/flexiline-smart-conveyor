from PySide6.QtWidgets import QMainWindow, QLabel
from pathlib import Path

from src.ui.generated.ui_mainwindow import Ui_MainWindow

PATH_ROOT = Path(__file__).resolve().parents[2]

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._load_stylesheet()
        self._initialize_ui_state()
        self._setup_status_bar()

    def _load_stylesheet(self) -> None:
        qss_path = PATH_ROOT / "resources" / "styles" / "design.qss"

        if not qss_path.exists():
            print(f"Stylesheet not found: {qss_path}")
            return
        
        self.setStyleSheet(qss_path.read_text(encoding="utf-8"))

    def _initialize_ui_state(self) -> None:
        self.ui.connection_status_label.setText("Disconnected")
        self.ui.connection_port_label.setText("Port: --")
        self.ui.camera_status_label.setText("Camera off")
        self.ui.system_message_label.setText("System ready")
        self.ui.red_counter_value_label.setText("0")
        self.ui.blue_counter_value_label.setText("0")
        self.ui.stop_button.setEnabled(False)
        self.ui.retry_camera_button.setVisible(False)

    def _setup_status_bar(self) -> None:
        self.status_message_label = QLabel("System ready")
        self.version_status_label = QLabel("v1.0.0")
        self.datetime_status_label = QLabel("--:--")
        self.statusBar().addWidget(self.status_message_label, 1)
        self.statusBar().addPermanentWidget(self.version_status_label)
        self.statusBar().addPermanentWidget(self.datetime_status_label)