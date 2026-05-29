from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget
from matplotlib.figure import Figure

from src.config import ChartConfig, DetectionResult

class ProductionChart(FigureCanvas):
    """
    PyQt5 widget that displays a real time line chart of red and blue detections.

    Signals:
        counters_updated(int, int): Emitted when the red and blue counts are updated.
        chart_updated(): Emitted when the chart is updated with new data.
    """
    counters_updated = pyqtSignal(int, int)
    chart_updated = pyqtSignal()

    def __init__(
            self,
            parent: QWidget | None = None,
            chart_title: str = ChartConfig.CHART_TITLE,
            ax_x: str = ChartConfig.X_LABEL,
            ax_y: str = ChartConfig.Y_LABEL,  
            legend_blue: str = ChartConfig.LEGEND_BLUE,
            legend_red: str = ChartConfig.LEGEND_RED
        ):
        """
        Initialize the production chart widget with configurable labels and legend.

        Args:
            parent(QWidget | None): Parent widget. Defaults to None.
            chart_title(str): Title of the chart. Defaults to ChartConfig.CHART_TITLE
            ax_x(str): X-axis label. Defaults to ChartConfig.X_LABEL
            ax_y(str): Y-axis label. Defaults to ChartConfig.Y_LABEL
            legend_blue(str): Legend label for blue line. Defaults to ChartConfig.LEGEND_BLUE
            legend_red(str): Legend label for red line. Defaults to ChartConfig.LEGEND_RED
        """
        self._fig = Figure()
        super().__init__(self._fig)
        self.setParent(parent)

        self._ax = self._fig.add_subplot(111)
        self._ax.set_title(chart_title)
        self._ax.set_xlabel(ax_x)
        self._ax.set_ylabel(ax_y)

        self._blue_count: int = 0
        self._red_count: int = 0
        self._time_step = 0

        self._time_data: list[int] = []
        self._red_history: list[int] = []
        self._blue_history: list[int] = []

        self._blue_line, = self._ax.plot([], [], label=legend_blue)
        self._red_line, = self._ax.plot([], [], label=legend_red)
        self._ax.legend()

        self._update_plot()

    
    def add_detection(self, result: str) -> None:
        """
        Add a new detection to the chart.

        Args:
            result(str): The detection result, expected to be 'red', 'blue', or 'none'.
        """
        if result == DetectionResult.RED:
            self._red_count += 1
        elif result == DetectionResult.BLUE:
            self._blue_count += 1
        else:
            return
        
        self._time_step += 1
        self._time_data.append(self._time_step)
        self._blue_history.append(self._blue_count)
        self._red_history.append(self._red_count)
        self._trim_history()
        self._update_plot()

        self.counters_updated.emit(self._red_count, self._blue_count)
        self.chart_updated.emit()

    def reset(self) -> None:
        """Reset the chart and counts to initial state.""" 
        self._blue_count = 0
        self._red_count = 0
        self._time_step = 0
        self._time_data.clear()
        self._red_history.clear()
        self._blue_history.clear()

        self._update_plot()

        self.counters_updated.emit(self._red_count, self._blue_count)
        self.chart_updated.emit()

    def get_counts(self) -> tuple[int, int]:
        """
        Return current red and blue detection counts.

        Returns:
            tuple[int, int]: A tuple containing the red count and blue count, respectively.
        """
        return self._red_count, self._blue_count

    def cleanup(self) -> None:
        """Release Matplotlib figure resources."""
        self._fig.clear()

    def _update_plot(self) -> None:
        self._blue_line.set_data(self._time_data, self._blue_history)
        self._red_line.set_data(self._time_data, self._red_history)

        self._ax.relim()
        self._ax.autoscale_view()

        self.draw_idle()

    def _trim_history(self) -> None:
        """Keep only the most recent chart data points."""
        
        # Prevents the chart from becoming too cluttered and improves performance
        # by limiting the number of plotted points
        max_points = ChartConfig.MAX_HISTORY_POINTS

        if len(self._time_data) <= max_points:
            return
        
        self._time_data = self._time_data[-max_points:]
        self._red_history = self._red_history[-max_points:]
        self._blue_history = self._blue_history[-max_points:]