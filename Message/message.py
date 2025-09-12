from PySide6.QtWidgets import QMessageBox, QDialog
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QFontMetrics



'''def show_message(self, text):

  box = QMessageBox(self)
  box.setWindowTitle('Update Message')
  box.setText(text)
  box.setStandardButtons(QMessageBox.Ok)
  return box'''

class Message(QDialog):
  def __init__(self, styles, parent=None):
    self.parent = parent
    self.box = QMessageBox(parent=self.parent)
    self.styles = styles
    self.box.setWindowTitle('Update Message')
    self.box.setStandardButtons(QMessageBox.Ok)
    #self.box.setStyleSheet(self.styles.modern_styles)

  def set_box_text(self, text):
    self.box.setText(text)

  def show_message(self, text):
    self.set_box_text(text)
    self._resize_to_fit_text(text)

    # show not functional - non-modal
    #self.box.show()

    # message exec - modal
    self.box.exec()
  
  def _resize_to_fit_text(self, text):
        # Use font metrics to calculate text size
        font_metrics = QFontMetrics(self.box.font())
        text_width = font_metrics.horizontalAdvance(text)
        text_height = font_metrics.height()

        # Add padding and set minimum size
        padding = 100  # Adjust as needed
        min_width = max(250, text_width + padding)
        min_height = 150  # You can also adjust based on line count

        self.box.setMinimumSize(min_width, min_height)

   
    
    
    