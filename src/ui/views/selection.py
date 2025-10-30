from PySide6.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem

class Selection(QWidget):
    def __init__(self, widget):
        super().__init__()
        self.selected_item = widget.currentItem()

    def get_selected_item(self):
        #print("selected item", self.selected_item)
        return

