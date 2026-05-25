"""
Arduino controller file.

This file contains the serial communication with Arduino controller,
including connection management, data transmission and reception of
control signals.
"""

import serial
from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QThread

from src.config import SerialConfig, SerialCommands


class SerialReaderThread(QThread):
    """
    Background thread for non-blocking serial data reading.

    Continuously polls the serial port for incoming data and emits signals when data is 
    received or when a control request is detected. Runs independently of the main UI
    event loop.

    Signals:
        data_received(str): Emitted when a line of data is received from the serial port.
        control_requested(): Emitted when a control request is detected from the serial port.
        error_occurred(str): Emitted when an error occurs during serial reading.
    """
    data_received = pyqtSignal(str)
    control_requested = pyqtSignal()
    error_occurred = pyqtSignal(str)

    def __init__(self, serial_port: serial.Serial):
        super().__init__()
        self.serial_port = serial_port
        self._running = True

    def run(self) -> None:
        while self._running:
            try:
                if self.serial_port and self.serial_port.is_open and self.serial_port.in_waiting > 0:
                    data = self.serial_port.readline().decode("utf-8", errors="ignore").strip()

                    if not data:
                        continue

                    self.data_received.emit(data)

                    if data == SerialCommands.CONTROL_REQUEST:
                        self.control_requested.emit()

            except serial.SerialException as error:
                self.error_occurred.emit(f"Serial read error: {error}")
                self._running = False
                break

            self.msleep(10)

    def stop(self) -> None:
        self._running = False
        self.wait(2000)


class ArduinoController(QObject):
    """
    Manages serial communication with Arduino embedded controller.
    Handles port scanning, connection management, command transmission and background reading 
    of serial data.

    Signals:
        connected(str): Emitted when a connection to a serial port is successfully established.
        disconnected(str): Emitted when a connection to a serial port is closed.
        connection_failed(str): Emitted when a connection to a serial port fails.
        data_sent(bytes): Emitted when data is sent to the serial port. Useful for logging or debugging.
        error_occurred(str): Emitted when an error occurs during serial communication.
        control_requested(): Emitted when a control request is received from the Arduino.
        data_received(str): Emitted when a line of data is received from the serial port.
    """
    connected = pyqtSignal(str)
    disconnected = pyqtSignal(str)
    connection_failed = pyqtSignal(str)
    data_sent = pyqtSignal(bytes)
    error_occurred = pyqtSignal(str)
    control_requested = pyqtSignal()
    data_received = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.serial_port: serial.Serial | None = None
        self.selected_port: str | None = None
        self.reader_thread: SerialReaderThread | None = None

    @property
    def is_connected(self) -> bool:
        return bool(self.serial_port and self.serial_port.is_open)
    
    @property
    def current_port(self) -> str | None:
        return self.selected_port
    
    def send_command(self, command: bytes) -> None:
        """
        Write a command to the Arduino via the serial port.

        Args:
            command: The byte string command to send to the Arduino.
        Emits:
            data_sent(bytes): Emitted with the command that was sent, useful for logging or debugging.
            error_occurred(str): Emitted if an error occurs during command transmission.
        """
        if not self.is_connected:
            self.error_occurred.emit("Serial port is not open.")
            return
        
        try:
            self.serial_port.write(command)
            self.data_sent.emit(command)
        except serial.SerialException as error:
            self.error_occurred.emit(f"Error sending command: {error}")

    def get_available_ports(self) -> list[str]:
        """
        Scan for available COM ports in the configured range.

        Attempts to open each port in the specified range to check if it is available.
        Always includes the currently selected port in the list, even if it is not detected 
        during scanning, to prevent it from disappearing from the UI dropdown.

        Returns:
            List of available COM port names (e.g., ["COM3", "COM4"]).
        """
        available_ports = []
        start_port, end_port = SerialConfig.PORT_SCAN_RANGE

        for port_number in range(start_port, end_port):
            port_name = f"COM{port_number}"
            try:
                test_serial = serial.Serial(
                    port=port_name,
                    baudrate=SerialConfig.BAUD_RATE,
                    timeout=SerialConfig.TIMEOUT
                )
                test_serial.close()
                available_ports.append(port_name)
            except serial.SerialException:
                continue

        # Ensure currently selected port is in the list
        if self.selected_port and self.selected_port not in available_ports:
            available_ports.append(self.selected_port)
            
        return available_ports
    
    def connect(self, port: str) -> None:
        """
        Connect to the specified serial port.

        Creates a serial connection using the configured communication
        parameters and starts the background reader thread after a short delay.

        Args:
            port: The name of the COM port to connect to (e.g., "COM3").
        """
        if self.is_connected:
            self.disconnect()

        try:
            self.serial_port = serial.Serial(
                port=port,
                baudrate=SerialConfig.BAUD_RATE,
                timeout=SerialConfig.TIMEOUT,
            )
            self.selected_port = port
            delay_ms = int(SerialConfig.RECONNECT_DELAY * 1000)
            QTimer.singleShot(delay_ms, lambda: self._finish_connection(port))
        except serial.SerialException as error:
            if self.serial_port and self.serial_port.is_open:
                self.serial_port.close()
            self.serial_port = None
            self.selected_port = None
            self.connection_failed.emit(f"Could not connect to {port}: {error}")
        
    def disconnect(self) -> None:
        """
        Disconnect the serial connection and clean up associated resources.

        Stops the reader thread, closes the serial port, and resets internal state.
        Safe to call even if no connection is active.

        Emits:
            disconnected(str): With the port name that was closed, if one was active.
            error_occurred(str): If the port could not be closed cleanly.
        """
        if self.reader_thread and self.reader_thread.isRunning():
            self.reader_thread.stop()
        self.reader_thread = None
        
        port = self.selected_port

        if self.serial_port:
            try:
                if self.serial_port.is_open:
                    self.serial_port.close()
            except serial.SerialException as error:
                self.error_occurred.emit(f"Error closing serial port: {error}")

        self.serial_port = None
        self.selected_port = None

        if port:
            self.disconnected.emit(port)

    def toggle_connection(self, port: str) -> None:
        """
        Connect to or disconnect from a port based on current state.

        If already connected to the given port, disconnects. Otherwise, initiates a 
        a new connection to the specified port.

        Args:
            port: The name of the COM port to connect to or disconnect from (e.g., 'COM3').
        """
        if self.selected_port == port and self.is_connected:
            self.disconnect()
        else:
            self.connect(port)

    def _finish_connection(self, port: str) -> None:
        if self.is_connected and self.selected_port == port:
            self.connected.emit(port)
            self._start_reader_thread()
        else:
            self.connection_failed.emit(f"Connection to {port} was not completed.")
    
    def cleanup(self) -> None:
        """
        Release all resources held by the controller.
        Delegates to disconnect() to ensure proper cleanup of serial port and reader thread.
        Should be called before the application exits.
        """
        self.disconnect()

    def _start_reader_thread(self) -> None:
        """
        Instantiate and start the serial reader thread.
        Connects thread signals to controller signals before starting.
        Does nothing if the serial port is not open.
        """
        if not self.serial_port or not self.serial_port.is_open:
            return

        self.reader_thread = SerialReaderThread(self.serial_port)
        self.reader_thread.data_received.connect(self.data_received)
        self.reader_thread.control_requested.connect(self.control_requested)
        self.reader_thread.error_occurred.connect(self._handle_reader_error)
        self.reader_thread.start()


    def _handle_reader_error(self, error: str) -> None:
        """
        Handle errors reported by the reader thread.
        Forwards the error signal and initiates disconnection to clean up resources after an
        unexpected error occurs during serial reading.
        """
        self.error_occurred.emit(error)
        self.disconnect()