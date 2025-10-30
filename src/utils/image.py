from PySide6.QtGui import QPixmap, QIcon

class Image():
  def __init__(self, file_path):
    self.file_path = file_path

class Icon():
  def __init__(self, file_path):
    #super().__init__(file_path)
    self.file_path = file_path

  def create_icon(self):
    if self.file_path:
      pix_map = QPixmap(self.file_path)
      # Check if pixmap was successfully loaded (not null)
      if not pix_map.isNull():
        icon = QIcon(pix_map)
        return icon
    return None
  
  def create_px_mp(self):
    if self.file_path:
      px_map = QIcon(self.file_path)
      if px_map:
        return px_map
    return None
  
  
'''class PixMap():
  def __init__(self, file_path):
    #super().__init__(file_path)
    self.file_path = file_path
  
  def create_px_mp(self):
    if self.file_path:
      px_map = QIcon(self.file_path)
      if px_map:
        return px_map
    return None'''


  



