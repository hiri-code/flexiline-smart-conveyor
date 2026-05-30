# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QStatusBar, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1330, 965)
        MainWindow.setStyleSheet(u"")
        self.actionPorts = QAction(MainWindow)
        self.actionPorts.setObjectName(u"actionPorts")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(12)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(12, 12, 12, 8)
        self.header_frame = QFrame(self.centralwidget)
        self.header_frame.setObjectName(u"header_frame")
        self.header_frame.setMinimumSize(QSize(0, 90))
        self.header_frame.setMaximumSize(QSize(16777215, 110))
        self.header_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.header_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.header_frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.header_left_spacer_widget = QWidget(self.header_frame)
        self.header_left_spacer_widget.setObjectName(u"header_left_spacer_widget")
        self.header_left_spacer_widget.setMinimumSize(QSize(160, 0))

        self.horizontalLayout.addWidget(self.header_left_spacer_widget)

        self.header_title_widget = QWidget(self.header_frame)
        self.header_title_widget.setObjectName(u"header_title_widget")
        self.horizontalLayout_2 = QHBoxLayout(self.header_title_widget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(10, 0, 0, 0)
        self.logo_label = QLabel(self.header_title_widget)
        self.logo_label.setObjectName(u"logo_label")
        self.logo_label.setMinimumSize(QSize(100, 70))
        self.logo_label.setMaximumSize(QSize(100, 90))
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.logo_label)

        self.title_text_widget = QWidget(self.header_title_widget)
        self.title_text_widget.setObjectName(u"title_text_widget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title_text_widget.sizePolicy().hasHeightForWidth())
        self.title_text_widget.setSizePolicy(sizePolicy)
        self.title_text_widget.setMinimumSize(QSize(260, 40))
        self.verticalLayout_2 = QVBoxLayout(self.title_text_widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.app_title_label = QLabel(self.title_text_widget)
        self.app_title_label.setObjectName(u"app_title_label")
        sizePolicy.setHeightForWidth(self.app_title_label.sizePolicy().hasHeightForWidth())
        self.app_title_label.setSizePolicy(sizePolicy)
        self.app_title_label.setMinimumSize(QSize(0, 0))
        self.app_title_label.setFrameShape(QFrame.Shape.NoFrame)
        self.app_title_label.setAlignment(Qt.AlignmentFlag.AlignBottom|Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft)

        self.verticalLayout_2.addWidget(self.app_title_label)

        self.app_subtitle_label = QLabel(self.title_text_widget)
        self.app_subtitle_label.setObjectName(u"app_subtitle_label")
        self.app_subtitle_label.setMaximumSize(QSize(16777215, 15))
        self.app_subtitle_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)

        self.verticalLayout_2.addWidget(self.app_subtitle_label)


        self.horizontalLayout_2.addWidget(self.title_text_widget)


        self.horizontalLayout.addWidget(self.header_title_widget)

        self.connection_status_frame = QFrame(self.header_frame)
        self.connection_status_frame.setObjectName(u"connection_status_frame")
        self.connection_status_frame.setMinimumSize(QSize(210, 70))
        self.connection_status_frame.setMaximumSize(QSize(260, 80))
        self.connection_status_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.connection_status_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.connection_status_frame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.connection_status_label = QLabel(self.connection_status_frame)
        self.connection_status_label.setObjectName(u"connection_status_label")
        self.connection_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_3.addWidget(self.connection_status_label)

        self.connection_port_label = QLabel(self.connection_status_frame)
        self.connection_port_label.setObjectName(u"connection_port_label")
        self.connection_port_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_3.addWidget(self.connection_port_label)

        self.connection_port_label.raise_()
        self.connection_status_label.raise_()

        self.horizontalLayout.addWidget(self.connection_status_frame)


        self.verticalLayout.addWidget(self.header_frame)

        self.main_content_widget = QWidget(self.centralwidget)
        self.main_content_widget.setObjectName(u"main_content_widget")
        self.main_content_widget.setAutoFillBackground(False)
        self.gridLayout = QGridLayout(self.main_content_widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.chart_card = QFrame(self.main_content_widget)
        self.chart_card.setObjectName(u"chart_card")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.chart_card.sizePolicy().hasHeightForWidth())
        self.chart_card.setSizePolicy(sizePolicy1)
        self.chart_card.setFrameShape(QFrame.Shape.StyledPanel)
        self.chart_card.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.chart_card)
        self.verticalLayout_5.setSpacing(8)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(10, 10, 10, 10)
        self.chart_title_label = QLabel(self.chart_card)
        self.chart_title_label.setObjectName(u"chart_title_label")
        sizePolicy.setHeightForWidth(self.chart_title_label.sizePolicy().hasHeightForWidth())
        self.chart_title_label.setSizePolicy(sizePolicy)
        self.chart_title_label.setMinimumSize(QSize(0, 35))
        self.chart_title_label.setMaximumSize(QSize(16777215, 45))
        self.chart_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_5.addWidget(self.chart_title_label)

        self.chart_container = QWidget(self.chart_card)
        self.chart_container.setObjectName(u"chart_container")
        sizePolicy1.setHeightForWidth(self.chart_container.sizePolicy().hasHeightForWidth())
        self.chart_container.setSizePolicy(sizePolicy1)
        self.chart_container.setMinimumSize(QSize(650, 320))

        self.verticalLayout_5.addWidget(self.chart_container)


        self.gridLayout.addWidget(self.chart_card, 0, 1, 1, 1)

        self.camera_card = QFrame(self.main_content_widget)
        self.camera_card.setObjectName(u"camera_card")
        self.camera_card.setMinimumSize(QSize(640, 480))
        self.camera_card.setFrameShape(QFrame.Shape.StyledPanel)
        self.camera_card.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.camera_card)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.camera_title_label = QLabel(self.camera_card)
        self.camera_title_label.setObjectName(u"camera_title_label")
        self.camera_title_label.setMinimumSize(QSize(0, 35))
        self.camera_title_label.setMaximumSize(QSize(16777215, 45))
        self.camera_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_4.addWidget(self.camera_title_label)

        self.camera_preview_container = QWidget(self.camera_card)
        self.camera_preview_container.setObjectName(u"camera_preview_container")
        sizePolicy.setHeightForWidth(self.camera_preview_container.sizePolicy().hasHeightForWidth())
        self.camera_preview_container.setSizePolicy(sizePolicy)
        self.camera_preview_container.setMinimumSize(QSize(520, 390))
        self.horizontalLayout_4 = QHBoxLayout(self.camera_preview_container)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.camera_label = QLabel(self.camera_preview_container)
        self.camera_label.setObjectName(u"camera_label")
        sizePolicy.setHeightForWidth(self.camera_label.sizePolicy().hasHeightForWidth())
        self.camera_label.setSizePolicy(sizePolicy)
        self.camera_label.setMinimumSize(QSize(320, 240))
        self.camera_label.setMaximumSize(QSize(16777215, 16777215))
        self.camera_label.setFrameShape(QFrame.Shape.NoFrame)
        self.camera_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_4.addWidget(self.camera_label)


        self.verticalLayout_4.addWidget(self.camera_preview_container)

        self.camera_status_label = QLabel(self.camera_card)
        self.camera_status_label.setObjectName(u"camera_status_label")
        self.camera_status_label.setMinimumSize(QSize(0, 40))
        self.camera_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_4.addWidget(self.camera_status_label)

        self.retry_button_container = QWidget(self.camera_card)
        self.retry_button_container.setObjectName(u"retry_button_container")
        self.horizontalLayout_3 = QHBoxLayout(self.retry_button_container)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.retry_camera_button = QPushButton(self.retry_button_container)
        self.retry_camera_button.setObjectName(u"retry_camera_button")
        self.retry_camera_button.setMinimumSize(QSize(0, 38))
        self.retry_camera_button.setMaximumSize(QSize(220, 16777215))

        self.horizontalLayout_3.addWidget(self.retry_camera_button)


        self.verticalLayout_4.addWidget(self.retry_button_container)

        self.camera_status_label.raise_()
        self.retry_button_container.raise_()
        self.camera_preview_container.raise_()
        self.camera_title_label.raise_()

        self.gridLayout.addWidget(self.camera_card, 0, 0, 1, 1)

        self.gridLayout.setColumnStretch(0, 4)
        self.gridLayout.setColumnStretch(1, 7)

        self.verticalLayout.addWidget(self.main_content_widget)

        self.bottom_content_widget = QWidget(self.centralwidget)
        self.bottom_content_widget.setObjectName(u"bottom_content_widget")
        self.gridLayout_2 = QGridLayout(self.bottom_content_widget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.controls_card = QFrame(self.bottom_content_widget)
        self.controls_card.setObjectName(u"controls_card")
        sizePolicy.setHeightForWidth(self.controls_card.sizePolicy().hasHeightForWidth())
        self.controls_card.setSizePolicy(sizePolicy)
        self.controls_card.setMinimumSize(QSize(0, 180))
        self.controls_card.setMaximumSize(QSize(680, 16777215))
        self.controls_card.setFrameShape(QFrame.Shape.StyledPanel)
        self.controls_card.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.controls_card)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.controls_title_label = QLabel(self.controls_card)
        self.controls_title_label.setObjectName(u"controls_title_label")
        self.controls_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_6.addWidget(self.controls_title_label)

        self.control_buttons_container = QWidget(self.controls_card)
        self.control_buttons_container.setObjectName(u"control_buttons_container")
        self.control_buttons_container.setMinimumSize(QSize(0, 70))
        self.horizontalLayout_5 = QHBoxLayout(self.control_buttons_container)
        self.horizontalLayout_5.setSpacing(16)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.start_button = QPushButton(self.control_buttons_container)
        self.start_button.setObjectName(u"start_button")
        self.start_button.setMinimumSize(QSize(150, 55))

        self.horizontalLayout_5.addWidget(self.start_button)

        self.stop_button = QPushButton(self.control_buttons_container)
        self.stop_button.setObjectName(u"stop_button")
        self.stop_button.setMinimumSize(QSize(150, 55))

        self.horizontalLayout_5.addWidget(self.stop_button)

        self.reset_chart_button = QPushButton(self.control_buttons_container)
        self.reset_chart_button.setObjectName(u"reset_chart_button")
        self.reset_chart_button.setMinimumSize(QSize(150, 55))

        self.horizontalLayout_5.addWidget(self.reset_chart_button)


        self.verticalLayout_6.addWidget(self.control_buttons_container)

        self.system_message_label = QLabel(self.controls_card)
        self.system_message_label.setObjectName(u"system_message_label")
        self.system_message_label.setMinimumSize(QSize(0, 34))
        self.system_message_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_6.addWidget(self.system_message_label)


        self.gridLayout_2.addWidget(self.controls_card, 0, 0, 1, 1)

        self.counters_card = QFrame(self.bottom_content_widget)
        self.counters_card.setObjectName(u"counters_card")
        self.counters_card.setMinimumSize(QSize(0, 180))
        self.counters_card.setFrameShape(QFrame.Shape.StyledPanel)
        self.counters_card.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.counters_card)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.counters_title_label = QLabel(self.counters_card)
        self.counters_title_label.setObjectName(u"counters_title_label")
        self.counters_title_label.setMinimumSize(QSize(0, 32))
        self.counters_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_7.addWidget(self.counters_title_label)

        self.counters_container = QWidget(self.counters_card)
        self.counters_container.setObjectName(u"counters_container")
        self.horizontalLayout_6 = QHBoxLayout(self.counters_container)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.red_counter_frame = QFrame(self.counters_container)
        self.red_counter_frame.setObjectName(u"red_counter_frame")
        self.red_counter_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.red_counter_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.red_counter_frame)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.red_counter_title_label = QLabel(self.red_counter_frame)
        self.red_counter_title_label.setObjectName(u"red_counter_title_label")
        self.red_counter_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_8.addWidget(self.red_counter_title_label)

        self.red_counter_value_label = QLabel(self.red_counter_frame)
        self.red_counter_value_label.setObjectName(u"red_counter_value_label")
        self.red_counter_value_label.setMinimumSize(QSize(0, 60))
        self.red_counter_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_8.addWidget(self.red_counter_value_label)


        self.horizontalLayout_6.addWidget(self.red_counter_frame)

        self.blue_counter_frame = QFrame(self.counters_container)
        self.blue_counter_frame.setObjectName(u"blue_counter_frame")
        self.blue_counter_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.blue_counter_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.blue_counter_frame)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.blue_counter_title_label = QLabel(self.blue_counter_frame)
        self.blue_counter_title_label.setObjectName(u"blue_counter_title_label")
        self.blue_counter_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_9.addWidget(self.blue_counter_title_label)

        self.blue_counter_value_label = QLabel(self.blue_counter_frame)
        self.blue_counter_value_label.setObjectName(u"blue_counter_value_label")
        self.blue_counter_value_label.setMinimumSize(QSize(0, 60))
        self.blue_counter_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_9.addWidget(self.blue_counter_value_label)


        self.horizontalLayout_6.addWidget(self.blue_counter_frame)


        self.verticalLayout_7.addWidget(self.counters_container)


        self.gridLayout_2.addWidget(self.counters_card, 0, 1, 1, 1)

        self.system_status_card = QFrame(self.bottom_content_widget)
        self.system_status_card.setObjectName(u"system_status_card")
        self.system_status_card.setMinimumSize(QSize(0, 180))
        self.system_status_card.setFrameShape(QFrame.Shape.StyledPanel)
        self.system_status_card.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.system_status_card)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.system_status_title_label = QLabel(self.system_status_card)
        self.system_status_title_label.setObjectName(u"system_status_title_label")
        self.system_status_title_label.setMinimumSize(QSize(0, 32))
        self.system_status_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_10.addWidget(self.system_status_title_label)

        self.system_health_container = QWidget(self.system_status_card)
        self.system_health_container.setObjectName(u"system_health_container")
        self.system_health_container.setMinimumSize(QSize(0, 100))
        self.horizontalLayout_7 = QHBoxLayout(self.system_health_container)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.system_health_icon_label = QLabel(self.system_health_container)
        self.system_health_icon_label.setObjectName(u"system_health_icon_label")
        self.system_health_icon_label.setMinimumSize(QSize(120, 0))
        self.system_health_icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_7.addWidget(self.system_health_icon_label)

        self.system_health_text_label = QLabel(self.system_health_container)
        self.system_health_text_label.setObjectName(u"system_health_text_label")

        self.horizontalLayout_7.addWidget(self.system_health_text_label)


        self.verticalLayout_10.addWidget(self.system_health_container)


        self.gridLayout_2.addWidget(self.system_status_card, 0, 2, 1, 1)

        self.gridLayout_2.setColumnStretch(0, 4)
        self.gridLayout_2.setColumnStretch(1, 2)
        self.gridLayout_2.setColumnStretch(2, 2)

        self.verticalLayout.addWidget(self.bottom_content_widget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1330, 33))
        self.menu_options = QMenu(self.menubar)
        self.menu_options.setObjectName(u"menu_options")
        self.menu_help = QMenu(self.menubar)
        self.menu_help.setObjectName(u"menu_help")
        MainWindow.setMenuBar(self.menubar)
        self.status_bar = QStatusBar(MainWindow)
        self.status_bar.setObjectName(u"status_bar")
        MainWindow.setStatusBar(self.status_bar)

        self.menubar.addAction(self.menu_options.menuAction())
        self.menubar.addAction(self.menu_help.menuAction())
        self.menu_options.addAction(self.actionPorts)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"FlexiLine", None))
        self.actionPorts.setText(QCoreApplication.translate("MainWindow", u"Ports", None))
        self.logo_label.setText(QCoreApplication.translate("MainWindow", u"LOGO", None))
        self.app_title_label.setText(QCoreApplication.translate("MainWindow", u"FLEXILINE", None))
        self.app_subtitle_label.setText(QCoreApplication.translate("MainWindow", u"SMART CONVEYOR SYSTEM", None))
        self.connection_status_label.setText(QCoreApplication.translate("MainWindow", u"Disconnected", None))
        self.connection_port_label.setText(QCoreApplication.translate("MainWindow", u"Port: --", None))
        self.chart_title_label.setText(QCoreApplication.translate("MainWindow", u"Production Chart", None))
        self.camera_title_label.setText(QCoreApplication.translate("MainWindow", u"Computer Vision", None))
        self.camera_label.setText(QCoreApplication.translate("MainWindow", u"Camera preview", None))
        self.camera_status_label.setText(QCoreApplication.translate("MainWindow", u"Camera off", None))
        self.retry_camera_button.setText(QCoreApplication.translate("MainWindow", u"Retry camera", None))
        self.controls_title_label.setText(QCoreApplication.translate("MainWindow", u"System Control", None))
        self.start_button.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.stop_button.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.reset_chart_button.setText(QCoreApplication.translate("MainWindow", u"Reset chart", None))
        self.system_message_label.setText(QCoreApplication.translate("MainWindow", u"System ready to start", None))
        self.counters_title_label.setText(QCoreApplication.translate("MainWindow", u"Counters", None))
        self.red_counter_title_label.setText(QCoreApplication.translate("MainWindow", u"Red count", None))
        self.red_counter_value_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.blue_counter_title_label.setText(QCoreApplication.translate("MainWindow", u"Blue count", None))
        self.blue_counter_value_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.system_status_title_label.setText(QCoreApplication.translate("MainWindow", u"System Status", None))
        self.system_health_icon_label.setText(QCoreApplication.translate("MainWindow", u"ICON", None))
        self.system_health_text_label.setText(QCoreApplication.translate("MainWindow", u"System operating normally", None))
        self.menu_options.setTitle(QCoreApplication.translate("MainWindow", u"Options", None))
        self.menu_help.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

