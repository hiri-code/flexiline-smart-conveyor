"""
Main window module.

This module contains the main application window, responsible for initializing UI
components, connecting signals and coordinating others modules.
"""
from PySide6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QMenu, QMessageBox
from PySide6.QtGui import QAction, QPixmap, QCloseEvent, QIcon
from PySide6.QtCore import QTimer, Qt
from datetime import datetime

from pathlib import Path

from src.ui.generated.ui_mainwindow import Ui_MainWindow
from src.config import StatusMessages, SerialCommands, DetectionResult, UIConfig
from src.core.arduino_controller import ArduinoController
from src.core.camera_processor import CameraProcessor
from src.core.production_chart import ProductionChart

PATH_ROOT = Path(__file__).resolve().parents[2]

class MainWindow(QMainWindow):
    """
    Main application window for the system.

    Coordinates via Qt signals/slots. Handles no business logic directly, delegates
    to core components and update the UI in response to their signals.
    """
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._load_stylesheet()
        self._initialize_components()
        self._setup_ui()
        self._connect_signals()
        self._initialize_ui_state()

    # >>>>>>>>>>>>>>>>>>>> Initialization <<<<<<<<<<<<<<<<<<<<

    def _load_stylesheet(self) -> None:
        """Load and apply the QSS stylesheet from the resources directory."""
        qss_path = PATH_ROOT / "resources" / "styles" / "design.qss"

        if not qss_path.exists():
            print(f"Stylesheet not found: {qss_path}")
            return
        
        self.setStyleSheet(qss_path.read_text(encoding="utf-8"))

    def _initialize_components(self) -> None:
        """Instantiate core system components."""
        self.arduino = ArduinoController()
        self.camera = CameraProcessor()
        self.production_chart = ProductionChart()

    def _setup_ui(self) -> None:
        """Configure UI elements that require runtime setup."""
        self._setup_status_bar()
        self._setup_chart()
        self._setup_ports_menu()
        self._setup_datetime_timer()
        self._setup_message_timer()
        self._setup_logo()
    
    def _setup_status_bar(self) -> None:
        """Add label to the status bar."""
        self.status_message_label = QLabel(StatusMessages.SYSTEM_READY)
        self.version_status_label = QLabel(StatusMessages.SYSTEM_VERSION)
        self.datetime_status_label = QLabel("--:--")

        self.statusBar().addWidget(self.status_message_label, 1)
        self.statusBar().addPermanentWidget(self.version_status_label)
        self.statusBar().addPermanentWidget(self.datetime_status_label)
    
    def _setup_chart(self) -> None:
        """Embed the production chart widget into the chart container."""
        chart_layout = QVBoxLayout(self.ui.chart_container)
        chart_layout.setContentsMargins(0, 0, 0, 0)
        chart_layout.setSpacing(0)
        chart_layout.addWidget(self.production_chart)

    def _setup_ports_menu(self) -> None:
        """Build the dynamic COM ports submenu under Options."""
        self._ports_submenu = QMenu("Ports", self)
        self.ui.menu_options.insertMenu(self.ui.action_ports, self._ports_submenu)
        self.ui.action_ports.setVisible(False)
        self._ports_submenu.aboutToShow.connect(self._populate_ports_menu)

    def _setup_datetime_timer(self) -> None:
        """Start a 1-second timer to keep the status bar clock updated."""
        self._datetime_timer = QTimer(self)
        self._datetime_timer.timeout.connect(self._update_datetime)
        self._datetime_timer.start(1000)
        self._update_datetime()

    def _setup_message_timer(self) -> None:
        self._message_clear_timer = QTimer(self)
        self._message_clear_timer.setSingleShot(True)
        self._message_clear_timer.timeout.connect(self._clear_temporary_message)
    
    def _setup_logo(self) -> None:
        logo_path = PATH_ROOT / "resources" / "images" / "flexiline_logo_mark.png"

        if not logo_path.exists():
            print(f"Logo not found: {logo_path}")
            return

        pixmap = QPixmap(str(logo_path))
        self.ui.logo_label.setPixmap(
            pixmap.scaled(
                self.ui.logo_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )

    def _initialize_ui_state(self) -> None:
        """Set the initial state of all UI elements."""
        self._set_connection_state(StatusMessages.SERIAL_DISCONNECTED, "offline")
        self._set_system_health(StatusMessages.SYSTEM_READY, "ok")
        self.ui.connection_port_label.setText("Port: --")
        self.ui.camera_status_label.setText(StatusMessages.CAMERA_OFF)
        self.ui.red_counter_value_label.setText("0")
        self.ui.blue_counter_value_label.setText("0")
        self.ui.stop_button.setEnabled(False)
        self.ui.retry_camera_button.setVisible(False)

    
    # >>>>>>>>>>>>>>>>>>>> Signal connection <<<<<<<<<<<<<<<<<<<<

    def _connect_signals(self) -> None:
        """Connect all component signals to their handlers."""
        self._connect_arduino_signals()
        self._connect_camera_signals()
        self._connect_chart_signals()
        self._connect_buttons()

    def _connect_arduino_signals(self) -> None:
        self.arduino.connected.connect(self._on_arduino_connected)
        self.arduino.disconnected.connect(self._on_arduino_disconnected)
        self.arduino.connection_failed.connect(self._on_arduino_connection_failed)
        self.arduino.error_occurred.connect(self._on_arduino_error_occurred)
        self.arduino.control_requested.connect(self.camera.request_detection)
    
    def _connect_camera_signals(self) -> None:
        self.camera.camera_started.connect(self._on_camera_started)
        self.camera.camera_stopped.connect(self._on_camera_stopped)
        self.camera.camera_error.connect(self._on_camera_error)
        self.camera.frame_ready.connect(self._on_camera_frame_ready)
        self.camera.detection_result.connect(self._on_camera_detection_result)

    def _connect_chart_signals(self) -> None:
        self.production_chart.counters_updated.connect(self._on_counters_update)

    def _connect_buttons(self) -> None:
        self.ui.start_button.clicked.connect(self._on_start_clicked)
        self.ui.stop_button.clicked.connect(self._on_stop_clicked)
        self.ui.reset_chart_button.clicked.connect(self._on_reset_chart_clicked)
        self.ui.retry_camera_button.clicked.connect(self._on_retry_camera_clicked)


    # >>>>>>>>>>>>>>>>>>>> Arduino signal handlers <<<<<<<<<<<<<<<<<<<<
    
    def _on_arduino_connected(self, port: str) -> None:
        """Update connection UI when Arduino connects successfully."""
        self._set_connection_state(StatusMessages.SERIAL_CONNECTED, "ok")
        self.ui.connection_port_label.setText(f"Port: {port}")
        self._set_system_health(StatusMessages.SYSTEM_READY, "ok")
        self._show_status_message(StatusMessages.SERIAL_CONNECTED)


    def _on_arduino_disconnected(self, port: str) -> None:
        """Reset connection UI whe Arduino disconnects."""
        self._set_connection_state(StatusMessages.SERIAL_DISCONNECTED, "offline")
        self.ui.connection_port_label.setText("Port: --")
        self.camera.stop()
        self.ui.start_button.setEnabled(True)
        self.ui.stop_button.setEnabled(False)
        self._set_system_health(StatusMessages.SERIAL_DISCONNECTED, "offline")
        self._show_status_message(StatusMessages.SERIAL_DISCONNECTED, temporary=False)

    def _on_arduino_connection_failed(self, error: str) -> None:
        """Show connection failure in UI."""
        self._set_connection_state(StatusMessages.SERIAL_FAILED, "error")
        self._show_status_message(error)

    def _on_arduino_error_occurred(self, error: str) -> None:
        """Show Arduino communication error in UI"""
        self._show_status_message(StatusMessages.SERIAL_ERROR.format(error))

    
    # >>>>>>>>>>>>>>>>>>>> Camera signal handlers <<<<<<<<<<<<<<<<<<<<

    def _on_camera_started(self) -> None:
        """Update camera status label when capture begins."""
        self.ui.camera_status_label.setText(StatusMessages.CAMERA_ON)
        self.ui.retry_camera_button.setVisible(False)
        self._show_status_message(StatusMessages.CAMERA_ON)
    
    def _on_camera_stopped(self) -> None:
        """Update camera status label when capture stops."""
        self.ui.camera_status_label.setText(StatusMessages.CAMERA_OFF)

    def _on_camera_error(self, error: str) -> None:
        """Show camera error and reveal the retry button."""
        message = StatusMessages.CAMERA_ERROR_RETRY.format(error)
        self.ui.camera_status_label.setText(message)
        self.ui.retry_camera_button.setVisible(True)
        self._set_system_health(message, "error")
        self._show_status_message(message, temporary=False)

    def _on_camera_frame_ready(self, image) -> None:
        """Display a processed frame in camera preview label."""
        pixmap = QPixmap.fromImage(image)
        self.ui.camera_label.setPixmap(
            pixmap.scaled(
                self.ui.camera_label.size(),
                aspectMode=Qt.AspectRatioMode.KeepAspectRatio,
                mode=Qt.TransformationMode.SmoothTransformation
            )
        )

    def _on_camera_detection_result(self, result: str) -> None:
        """Forward detection result to the production chart."""
        self.production_chart.add_detection(result)
        self._send_detection_to_arduino(result)

    def _send_detection_to_arduino(self, result: str) -> None:
        if not self.arduino.is_connected:
            self._show_status_message(StatusMessages.SYSTEM_NO_ARDUINO, temporary=False)
            return
        
        if result == DetectionResult.BLUE:
            self.arduino.send_command(SerialCommands.COLOR_BLUE)
            self._show_status_message(StatusMessages.COLOR_BLUE_DETECTED)
        elif result == DetectionResult.RED:
            self.arduino.send_command(SerialCommands.COLOR_RED)
            self._show_status_message(StatusMessages.COLOR_RED_DETECTED)
        else:
            self.arduino.send_command(SerialCommands.COLOR_NONE)
            self._show_status_message(StatusMessages.COLOR_NONE_DETECTED)

    # >>>>>>>>>>>>>>>>>>>> Chart signal handlers <<<<<<<<<<<<<<<<<<<<

    def _on_counters_update(self, red: int, blue: int) -> None:
        """Update counter labels when the chart reports new counts."""
        self.ui.red_counter_value_label.setText(str(red))
        self.ui.blue_counter_value_label.setText(str(blue))


    # >>>>>>>>>>>>>>>>>>>> Button handlers <<<<<<<<<<<<<<<<<<<<

    def _on_start_clicked(self) -> None:
        """Send start command to Arduino and update button states."""
        if not self.arduino.is_connected:
            self._set_system_health(StatusMessages.SYSTEM_NO_ARDUINO, "error")
            self._show_status_message(StatusMessages.SYSTEM_NO_ARDUINO)
            return
        
        self.camera.start()
        self.arduino.send_command(SerialCommands.START)
        self.ui.start_button.setEnabled(False)
        QTimer.singleShot(UIConfig.BUTTON_TOGGLE_DELAY_MS, lambda: self.ui.stop_button.setEnabled(True))
        self._show_status_message(StatusMessages.SYSTEM_STARTED)

    def _on_stop_clicked(self) -> None:
        """Send stop command to Arduino and update button states."""
        if not self.arduino.is_connected:
            return
        
        self.arduino.send_command(SerialCommands.STOP)
        self.camera.stop()
        self.ui.stop_button.setEnabled(False)
        QTimer.singleShot(UIConfig.BUTTON_TOGGLE_DELAY_MS, lambda: self.ui.start_button.setEnabled(True))
        self._set_system_health(StatusMessages.SYSTEM_STOPPED, "warning")
        self._show_status_message(StatusMessages.SYSTEM_STOPPED)

    def _on_reset_chart_clicked(self) -> None:
        """Reset production chart and counters."""
        self.production_chart.reset()
        self._show_status_message(StatusMessages.SYSTEM_CHART_RESET)

    def _on_retry_camera_clicked(self) -> None:
        """Attempt to restart the camera after an error."""
        self.ui.retry_camera_button.setVisible(False)
        self.ui.camera_status_label.setText(StatusMessages.CAMERA_RECONNECTING)
        self._show_status_message(StatusMessages.CAMERA_RECONNECTING, temporary=False)
        self.camera.start()
    

    # >>>>>>>>>>>>>>>>>>>> Port menu function <<<<<<<<<<<<<<<<<<<<
    
    def _populate_ports_menu(self) -> None:
        self._ports_submenu.clear()
        ports = self.arduino.get_available_ports()

        if not ports:
            action = QAction("No ports available", self)
            action.setEnabled(False)
            self._ports_submenu.addAction(action)
            return
        
        for port in ports:
            action = QAction(port, self)
            action.setCheckable(True)
            action.setChecked(port == self.arduino.current_port)
            action.triggered.connect(lambda checked, p=port: self.arduino.toggle_connection(p))
            self._ports_submenu.addAction(action)


    # >>>>>>>>>>>>>>>>>>>> Utilities <<<<<<<<<<<<<<<<<<<<

    def _show_status_message(self, message: str, temporary: bool = True) -> None:
        """Display a message in the status bar."""
        self.status_message_label.setText(message)
        self._message_clear_timer.stop()

        if temporary:
            self._message_clear_timer.start(UIConfig.MESSAGE_DURATION_MS)

    def _clear_temporary_message(self) -> None:
        """Restore the default system message after a temporary message expires."""
        default_message = (StatusMessages.SYSTEM_READY if self.arduino.is_connected else StatusMessages.SERIAL_DISCONNECTED)
        self.status_message_label.setText(default_message)
        
    def _set_connection_state(self, text: str, state: str) -> None:
        self.ui.connection_status_label.setText(text)
        self._apply_state_property(self.ui.connection_status_label, state)


    def _set_system_health(self, text: str, state: str) -> None:
        self.ui.system_health_text_label.setText(text)
        self._apply_state_property(self.ui.system_health_text_label, state)


    def _apply_state_property(self, widget, state: str) -> None:
        widget.setProperty("state", state)
        widget.style().unpolish(widget)
        widget.style().polish(widget)
    
    def _update_datetime(self) -> None:
        """Update the status bar clock with current local time."""
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.datetime_status_label.setText(now)
    


    # >>>>>>>>>>>>>>>>>>>> Close events <<<<<<<<<<<<<<<<<<<<
    
    def closeEvent(self, event: QCloseEvent) -> None:
        """Ask for confirmation and release all resources before closing the app."""
        if not self._confirm_close():
            event.ignore()
            return
        
        self._cleanup_resources()
        event.accept()
        

    def _confirm_close(self) -> bool:
        """Show a confirmation dialog before closing the application."""
        dialog = QMessageBox(self)
        dialog.setWindowTitle(StatusMessages.CLOSE_CONFIRMATION_TITLE)
        dialog.setText(StatusMessages.CLOSE_CONFIRMATION_MESSAGE)
        dialog.setIcon(QMessageBox.Icon.Question)

        yes_button = dialog.addButton(StatusMessages.CLOSE_CONFIRMATION_YES, QMessageBox.ButtonRole.YesRole)
        no_button = dialog.addButton(StatusMessages.CLOSE_CONFIRMATION_NO, QMessageBox.ButtonRole.NoRole)

        dialog.setDefaultButton(no_button)
        dialog.exec()
        return dialog.clickedButton() == yes_button
    
    def _cleanup_resources(self) -> None:
        """Release all resources used by the application."""
        self._datetime_timer.stop()
        self.camera.cleanup()
        self.arduino.cleanup()
        self.production_chart.cleanup()