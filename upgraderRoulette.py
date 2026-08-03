from random import randint

from PyQt6.QtCore import QVariantAnimation, QEasingCurve, QRect, Qt, QLineF, pyqtSignal
from PyQt6.QtGui import QPainter, QMovie, QBrush, QColor, QPen, QLinearGradient, QConicalGradient, QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout

from AllConstants import WINDOWSIZE


class UpgraderRouletteWidget(QWidget):
    animation_ended = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.widgetSize= int(WINDOWSIZE[0] * 0.3)
        self.setFixedSize(self.widgetSize, self.widgetSize)

        self.arrow_angle = 180
        self.choosed_chance = 0

        self.status = 'idle'
        self.is_success = False

        self.animation = QVariantAnimation(self)
        self.animation.setDuration(6000)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.animation.valueChanged.connect(self.handle_animation_change)

        self.animation.finished.connect(self.handle_animation_finished)

        self.chance_animation = QVariantAnimation(self)
        self.chance_animation.setDuration(800)  # Полкилометра плавности (400мс), можно сделать быстрее (например, 250)
        # Отличный тип кривой для эффекта упругого или мягкого наплыва:
        self.chance_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.chance_animation.valueChanged.connect(self.handle_chance_animation_change)

    def handle_animation_change(self, value):
        self.arrow_angle = value
        self.update()

        # Слот для обработки плавного изменения процентов на каждом кадре

    def handle_chance_animation_change(self, value):
        self.choosed_chance = value
        self.right_after_spin = False
        self.update()  # Перерисовываем пирог (drawPie) с новым углом

        # МЕТОД ДЛЯ ВЫЗОВА ПРИ НАЖАТИИ НА КНОПКИ ШАНСА (вызывайте его из chance_changed)

    def animate_chance_change(self, new_chance):
        """Плавный переход сектора к новому значению шанса"""
        self.status = 'idle'
        if self.chance_animation.state() == QVariantAnimation.State.Running:
            self.chance_animation.stop()

        # Стартуем с текущего фактического значения процентов
        self.chance_animation.setStartValue(float(self.choosed_chance))
        # Конечная точка — проценты с нажатой кнопки
        self.chance_animation.setEndValue(float(new_chance))

        self.chance_animation.start()

    def start_animation(self, neededangle, is_success=False):
        if self.animation.state() == QVariantAnimation.State.Running:
            return

        self.status = 'spinning' # Рулетка начала вращение
        self.is_success = is_success  # Запоминаем исход для финала
        self.update()

        if randint(0,1) == 1:
            target_angle = -1800 - neededangle
        else:
            target_angle = -1800 + neededangle

        self.animation.setStartValue(float(180))
        self.animation.setEndValue(float(target_angle))
        self.animation.start()

    def handle_animation_finished(self):
        self.status = 'finished'
        self.update()
        self.animation_ended.emit()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        deleniaRect = QRect(70, 70, self.widgetSize - 140, self.widgetSize - 140)
        mainRect = QRect(20, 20, self.widgetSize - 40, self.widgetSize - 40)
        secondRect = QRect(50, 50, self.widgetSize - 100, self.widgetSize - 100)

        painter.setBrush(QBrush(QColor("#404040")))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(mainRect)

        center = mainRect.center()
        gradient = QConicalGradient(center.x(), center.y(), -90)
        gradient.setColorAt(1.0, QColor("#00EE55"))
        gradient.setColorAt(0.75, QColor("#00E5AA"))
        gradient.setColorAt(0.5, QColor("#00B4D8"))
        gradient.setColorAt(0.25, QColor("#00E5AA"))
        gradient.setColorAt(0, QColor("#00EE55"))


        painter.setBrush(QBrush(gradient))
        angle = 360.0 / 100.0 * self.choosed_chance
        painter.drawPie(mainRect, int((-90 + angle / 2.0) * 16), int(-angle * 16))

        center = mainRect.center()
        arrow_length = self.widgetSize // 2 - 8
        arrow_line = QLineF.fromPolar(arrow_length, self.arrow_angle - 90)
        arrow_line.translate(center.x(), center.y())

        arrow_pen = QPen(QColor("#e74c3c"), 4)
        arrow_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(arrow_pen)
        painter.drawLine(arrow_line)

        painter.setBrush(QBrush(QColor("#212121")))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(secondRect)

        painter.setBrush(QBrush(QColor("#404040")))
        for ang in range(0, 360, 10):
            painter.drawPie(secondRect, ang * 16, 16)

        painter.drawEllipse(deleniaRect)

        font = QFont("Segoe UI", 26, QFont.Weight.Bold)
        painter.setFont(font)
        if self.status == "finished":
            # Если анимация завершена — пишем результат
            if self.is_success:
                painter.setPen(QPen(QColor("#00EE55")))  # Зеленый
                text_to_draw = "УСПЕХ"
            else:
                painter.setPen(QPen(QColor("#e74c3c")))  # Красный
                text_to_draw = "НЕУДАЧА"
        else:
            # Во всех остальных случаях ("idle", "spinning") — пишем проценты
            painter.setPen(QPen(QColor("#00EE00")))
            text_to_draw = f"{self.choosed_chance:.2f}%"

            # Рисуем итоговый текст строго по центру
        painter.drawText(secondRect, Qt.AlignmentFlag.AlignCenter, text_to_draw)

