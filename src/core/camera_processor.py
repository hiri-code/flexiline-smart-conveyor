"""
Camera processor module.

This module contains the camera processing logic, including initialization,
handles the continous capture of video frames, conversion to hsv and emits signals.
"""

from PySide6.QtCore import QObject, Signal, QThread
from PySide6.QtGui import QImage
import cv2
from src.config import CameraConfig, DetectionResult
import numpy as np


class CameraReaderThread(QThread):
    """
    Background thread for non-blocking camera frame processing.

    Captures frames from the camera, process them for color detections and emits
    processed frames as QImage for direct UI rendering. All OpenCV operations run
    in this thread to keep UI responsive.

    Signals:
        frame_ready = (QImage): Emitted for every processed frame with color overlays
            drawn. Ready for display in a QLabel.
        error_occurred(str): Emitted if the camera disconnects or fails to open. Thread
            stops after emitting.
        started_successfully(): Emitted after the camera is initialized successfully.
    """
    frame_ready = Signal(QImage)
    error_occurred = Signal(str)
    started_successfully = Signal()
    detection_result = Signal(str)

    def __init__(self, camera_index: int = CameraConfig.CAMERA_INDEX):
        """
        Initialize the reader thread with camera index and HSV color boundaries.

        Args:
            camera_index (int): OpenCV camera device index. Defaults to CameraConfig.CAMERA_INDEX
        """
        super().__init__()
        self._camera_index = camera_index
        self._running = True
        self._detection_requested = False

        # Build numpy arrays once at init, not on every frame
        self._lower_blue = np.array(CameraConfig.LOWER_BLUE)
        self._upper_blue = np.array(CameraConfig.UPPER_BLUE)
        self._lower_red_1 = np.array(CameraConfig.LOWER_RED_1)
        self._upper_red_1 = np.array(CameraConfig.UPPER_RED_1)
        self._lower_red_2 = np.array(CameraConfig.LOWER_RED_2)
        self._upper_red_2 = np.array(CameraConfig.UPPER_RED_2)

    def request_detection(self) -> None:
        self._detection_requested = True

    def run(self) -> None:
        """
        Capture frames, process them and emit results.
        
        Opens the camera, sets resolution, then enters the capture loop.
        Each frame is converted to HSV, masked, optionally classified, annotated with
        contours and emitted as a QImage.
        """
        cap = cv2.VideoCapture(self._camera_index)

        if not cap.isOpened():
            self.error_occurred.emit("Could not open camera.")
            return
        
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, CameraConfig.FRAME_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CameraConfig.FRAME_HEIGHT)
        self.started_successfully.emit()

        while self._running:
            ret, frame = cap.read()
            if not ret:
                self.error_occurred.emit("Failed to capture frame")
                break
            
            hsv = self._convert_to_hsv(frame)
            blue_mask, red_mask = self._create_masks(hsv)

            if self._detection_requested:
                self._detection_requested = False
                blue_pixels, red_pixels = self._count_pixels(blue_mask, red_mask)
                result = self._classify_color(blue_pixels, red_pixels)
                self.detection_result.emit(result)

            annotated = self._draw_overlay(frame, blue_mask, red_mask)
            q_image = self._to_qimage(annotated)
            self.frame_ready.emit(q_image)

            self.msleep(10)

        cap.release()

    def stop(self) -> None:
        
        self._running = False
        self.wait(2000)

    def _convert_to_hsv(self, frame: np.ndarray) -> np.ndarray:
        return cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)        

    def _create_masks(self, hsv: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        blue_mask = cv2.inRange(hsv, self._lower_blue, self._upper_blue)        
        red_mask = cv2.bitwise_or(
            cv2.inRange(hsv, self._lower_red_1, self._upper_red_1),
            cv2.inRange(hsv, self._lower_red_2, self._upper_red_2)
        )
        return blue_mask, red_mask

    def _count_pixels(self, blue_mask: np.ndarray, red_mask: np.ndarray) -> tuple[int, int]:
        return cv2.countNonZero(blue_mask), cv2.countNonZero(red_mask)
    
    def _classify_color(self, blue_pixels: int, red_pixels: int) -> str:
        if blue_pixels > CameraConfig.MIN_COLOR_PIXELS:
            return DetectionResult.BLUE
        if red_pixels > CameraConfig.MIN_COLOR_PIXELS:
            return DetectionResult.RED
        return DetectionResult.NONE
    
    def _draw_overlay(self, frame: np.ndarray, blue_mask: np.ndarray, red_mask: np.ndarray) -> np.ndarray:
        annotated = frame.copy()
        
        blue_contours, _ = cv2.findContours(
            blue_mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        red_contours, _ = cv2.findContours(
            red_mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        cv2.drawContours(annotated, blue_contours, -1, (255, 0, 0), 2)
        cv2.drawContours(annotated, red_contours, -1, (0, 0, 255), 2)

        return annotated
    
    def _to_qimage(self, frame: np.ndarray) -> QImage:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        return QImage(rgb.data, w, h, ch * w, QImage.Format.Format_RGB888).copy()


class CameraProcessor(QObject):
    """
    Public interface for camera capture and color detection.

    Wraps CameraReaderThread and exposes a clean API for starting, stopping and requesting
    color detection.

    Signals:
        camera_started: Emitted when the camera is confirmed open.
        camera_stopped: Emitted when the camera stops, either normally or due to an error.
        camera_error(str): Emitted when the camera encounters an error.
        detection_result(str): Forwarded from CameraReaderThread. Carries the color 
            classification result.
        frame_ready(QImage): Forwarded from CameraReaderThread. Each frame is processed and 
            ready for display.
    """
    camera_started = Signal()
    camera_stopped = Signal()
    camera_error = Signal(str)
    detection_result = Signal(str)
    frame_ready = Signal(QImage)
    
    def __init__(self):
        super().__init__()
        self._reader_thread: CameraReaderThread | None = None

    def start(self) -> None:
        """
        Start the camera capture and processing thread.
        
        Does nothing if the thread is already running.

        Emits:
            camera_started: Once the camera is confirmed open.
            camera_error: If the camera cannot be opened.
        """
        if self._reader_thread and self._reader_thread.isRunning():
            return
        
        self._reader_thread = CameraReaderThread()
        self._reader_thread.frame_ready.connect(self.frame_ready)
        self._reader_thread.detection_result.connect(self.detection_result)
        self._reader_thread.started_successfully.connect(self.camera_started)
        self._reader_thread.error_occurred.connect(self._handle_camera_error)
        self._reader_thread.start()

    def stop(self):
        """
        Stop the camera capture thread and reset state.

        Emits:
            camera_stopped: After the thread is stopped.
        """
        if self._reader_thread and self._reader_thread.isRunning():
            self._reader_thread.stop()
        self._reader_thread = None
        self.camera_stopped.emit()

    def request_detection(self) -> None:
        if self._reader_thread and self._reader_thread.isRunning():
            self._reader_thread.request_detection()
        else:
            self.camera_error.emit("Camera is not running.")

    def cleanup(self) -> None:
        self.stop()

    def _handle_camera_error(self, error: str) -> None:
        self.camera_error.emit(error)
        self.stop()