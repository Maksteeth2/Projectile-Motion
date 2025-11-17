import sys
import math
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout
)
from PyQt6.QtGui import QPainter, QPen, QColor


class ProjectileWidget(QWidget):
    GRAVITY = 9.8
    SCALE = 5.0

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Projectile Motion Simulation")
        self.setFixedSize(800, 600)

        self.vx = 0
        self.vy = 0
        self.x = 0
        self.y = 0
        self.running = False
        self.trajectory = []

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_position)
        self.dt = 0.02  

        # UI
        self.time_label = QLabel("Time: 0.0 s")
        self.height_label = QLabel("Max Height: 0.0 m")
        self.range_label = QLabel("Range: 0.0 m")

        self.speed_input = QLineEdit()
        self.speed_input.setPlaceholderText("Initial speed (m/s)")
        self.angle_input = QLineEdit()
        self.angle_input.setPlaceholderText("Launch angle (°)")

        self.launch_button = QPushButton("Launch")
        self.pause_button = QPushButton("Pause")
        self.reset_button = QPushButton("Reset")

        self.launch_button.clicked.connect(self.launch)
        self.pause_button.clicked.connect(self.pause)
        self.reset_button.clicked.connect(self.reset)

        # Layouts
        layout = QVBoxLayout()
        info_layout = QHBoxLayout()
        info_layout.addWidget(self.time_label)
        info_layout.addWidget(self.height_label)
        info_layout.addWidget(self.range_label)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.speed_input)
        input_layout.addWidget(self.angle_input)
        input_layout.addWidget(self.launch_button)
        input_layout.addWidget(self.pause_button)
        input_layout.addWidget(self.reset_button)

        layout.addLayout(info_layout)
        layout.addStretch()
        layout.addLayout(input_layout)

        self.setLayout(layout)

    def launch(self):
        try:
            speed = float(self.speed_input.text())
            angle_deg = float(self.angle_input.text())
            angle_rad = math.radians(angle_deg)

            self.vx = speed * math.cos(angle_rad)
            self.vy = speed * math.sin(angle_rad)
            self.x = 0
            self.y = 0
            self.max_height = (self.vy ** 2) / (2 * self.GRAVITY)
            self.total_time = (2 * self.vy) / self.GRAVITY
            self.range = self.vx * self.total_time

            self.trajectory.clear()
            self.running = True
            self.timer.start(int(self.dt * 1000))
        except ValueError:
            print("Enter valid numbers for speed and angle.")

    def pause(self):
        self.running = not self.running
        if self.running:
            self.timer.start(int(self.dt * 1000))
        else:
            self.timer.stop()

    def reset(self):
        self.running = False
        self.timer.stop()
        self.x = 0
        self.y = 0
        self.trajectory.clear()
        self.time_label.setText("Time: 0.0 s")
        self.height_label.setText("Max Height: 0.0 m")
        self.range_label.setText("Range: 0.0 m")
        self.update()

    def update_position(self):
        if not self.running:
            return

        prev_x = self.x
        prev_y = self.y

        self.x += self.vx * self.dt
        self.y += self.vy * self.dt - 0.5 * self.GRAVITY * self.dt ** 2
        self.vy -= self.GRAVITY * self.dt

        # Stop when hit the ground
        if self.y < 0:
            self.running = False
            self.timer.stop()
            self.y = 0

        self.trajectory.append((prev_x, prev_y, self.x, self.y))
        self.time_label.setText(f"Time: {self.x / self.vx:.2f} s")
        self.height_label.setText(f"Max Height: {self.max_height:.2f} m")
        self.range_label.setText(f"Range: {self.range:.2f} m")
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(QColor("blue"), 2))

        # Draw trajectory
        for line in self.trajectory:
            x1, y1, x2, y2 = line
            painter.drawLine(
                int(x1 * self.SCALE),
                int(self.height() - y1 * self.SCALE),
                int(x2 * self.SCALE),
                int(self.height() - y2 * self.SCALE)
            )

        # Draw projectile
        painter.setPen(QPen(QColor("red")))
        painter.setBrush(QColor("red"))
        painter.drawEllipse(
            int(self.x * self.SCALE) - 5,
            int(self.height() - self.y * self.SCALE) - 5,
            10,
            10
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProjectileWidget()
    window.show()
    sys.exit(app.exec())
