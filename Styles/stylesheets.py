class StyleSheets():
    def __init__(self):
        #self.main_styles = self.get_monochrome_style()
        self.main_styles = self.get_monochrome_img_style()

        self.modern_styles = self.get_modern_style()

        self.neopolitan_styles = self.get_neopolitan_style()

        #self.old_school_styles = self.get_old_school_style()

        self.hand_drawn_styles = self.get_hand_drawn()

        self.baseball_styles = self.get_baseball()
        
        self.paper_styles = self.get_paper()

        #self.chrome_styles = self.get_chrome()

        self.retro_styles = self.get_retro()

        self.vapor_styles = self.get_vapor()
    
    def get_vapor(self):
        return ''' 
        /* Global */
        * {
            font-size: 16px;
            font-family: "Courier New", monospace;
            color: #ffffff;
        }

        /* QFileDialog */
        QFileDialog {
            background-color: #1a0033; /* deep purple backdrop */
            color: #ffff00; /* neon yellow labels */
            font-size: 16px;
        }

        /* File list in QFileDialog */
        QFileDialog QListView,
        QFileDialog QTreeView {
            background-color: #ffffff; /* white background */
            color: #000000; /* black text for contrast */
            font-size: 16px;
            selection-background-color: #00ffff; /* neon cyan highlight */
            selection-color: #000000; /* black text on highlight */
        }

        /* QFileDialog headers */
        QFileDialog QHeaderView::section {
            background-color: #ff00cc; /* neon pink header */
            color: #000000; /* black text */
            font-weight: bold;
            font-size: 16px;
            border: 1px solid #00ffff;
            padding: 4px;
        }

        /* QFileDialog QLineEdit (filename box) */
        QFileDialog QLineEdit {
            background-color: #000000;
            color: #00ffff; /* cyan text */
            border: 2px solid #ff00cc;
            border-radius: 4px;
            padding: 4px;
        }

        /* QFileDialog QComboBox (file type dropdown) */
        QFileDialog QComboBox {
            background-color: #000000;
            color: #ffff00; /* neon yellow text */
            border: 2px solid #00ffff;
            border-radius: 4px;
            padding: 2px;
            min-height: 20px;
        }

        /* QDialog */
        QDialog {
            background: qlineargradient(
                spread:pad, x1:0, y1:0, x2:1, y2:1,
                stop:0 #1a1aff, stop:0.5 #ff00cc, stop:1 #6600ff
            ); /* neon purple/blue gradient */
            border: 2px solid #ff00cc;
            color: #ffff00; /* neon yellow text on blue/purple */
        }

        /* QGroupBox */
        QGroupBox {
            background-color: #ff00cc; /* neon pink */
            border: 2px solid #00ffff; /* cyan border */
            border-radius: 6px;
            margin-top: 20px;
            padding: 6px;
            color: #000000; /* black text inside pink */
        }

        /* QGroupBox::title */
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 2px 6px;
            color: #000000; /* black text for readability on pink */
            font-weight: bold;
            font-size: 18px;
        }

        /* QLabel */
        QLabel {
            color: #ffff00; /* neon yellow for visibility */
            background: transparent;
        }

        /* QLineEdit */
        QLineEdit {
            background-color: #000000;
            color: #00ffff; /* cyan text on black */
            border: 2px solid #ff00cc; /* neon pink border */
            border-radius: 4px;
            padding: 4px;
        }

        /* QLineEdit:focus */
        QLineEdit:focus {
            border: 2px solid #00ffff; /* neon cyan */
            background-color: #1a1a1a;
            color: #ffff00; /* yellow text for stronger contrast */
        }

        /* QTreeWidget */
        QTreeWidget {
            background-color: #330066; /* deep purple */
            border: 2px solid #ff00cc; /* neon pink border */
            color: #ffff00; /* neon yellow text for contrast on deep purple */
            font-size: 16px;
            show-decoration-selected: 1;
        }

        /* QTreeWidget items */
        QTreeWidget::item {
            font-size: 16px;
            color: #ffff00; /* neon yellow for readability on deep purple */
        }

        QTreeWidget::item:selected {
            background-color: #00ffff; /* neon cyan highlight */
            color: #000000; /* black text on selection */
        }

        QTreeWidget::item:hover {
            background-color: #ff00cc; /* neon pink hover */
            color: #000000; /* black text */
        }

        /* QTreeWidget column headers */
        QHeaderView::section {
            background-color: #ff00cc; /* neon pink headers */
            color: #000000; /* black text for readability */
            font-weight: bold;
            font-size: 16px;
            border: 1px solid #00ffff; /* neon cyan border */
            padding: 4px;
        }

        /* QCheckBox */
        QCheckBox {
            spacing: 8px;
            color: #ffff00; /* neon yellow for contrast */
            font-size: 16px;
        }

        /* QCheckBox::indicator */
        QCheckBox::indicator {
            width: 18px;
            height: 18px;
            border: 2px solid #00ffff;
            background-color: #000000;
        }

        /* QCheckBox::indicator:checked */
        QCheckBox::indicator:checked {
            background-color: #ffff00; /* neon yellow */
            border: 2px solid #ff00cc;
        }

        /* QCheckBox::indicator:unchecked */
        QCheckBox::indicator:unchecked {
            background-color: #000000;
        }

        /* QRadioButton */
        QRadioButton {
            spacing: 8px;
            color: #ffff00; /* neon yellow text */
            font-size: 16px;
        }

        /* QRadioButton::indicator */
        QRadioButton::indicator {
            width: 18px;
            height: 18px;
            border-radius: 9px;
            border: 2px solid #00ffff;
            background-color: #000000;
        }

        /* QRadioButton::indicator:checked */
        QRadioButton::indicator:checked {
            background-color: #ffff00;
            border: 2px solid #ff00cc;
        }

        /* QRadioButton::indicator:unchecked */
        QRadioButton::indicator:unchecked {
            background-color: #000000;
            border: 2px solid #00ffff;
        }

        /* QPushButton */
        QPushButton {
            background-color: #ff00cc; /* neon pink */
            border: 2px solid #00ffff;
            border-radius: 6px;
            padding: 6px 12px;
            color: #000000; /* black text for contrast */
            font-weight: bold;
        }

        /* QPushButton:hover */
        QPushButton:hover {
            background-color: #00ffff; /* neon cyan */
            color: #000000; /* black text */
            border: 2px solid #ffff00;
        }

        /* QComboBox (general) */
        QComboBox {
            background-color: #000000; /* black base */
            color: #ffff00; /* neon yellow text */
            border: 2px solid #00ffff; /* neon cyan border */
            border-radius: 4px;
            padding: 4px;
            min-height: 22px;
            font-size: 16px;
        }

        /* QComboBox on focus */
        QComboBox:focus {
            border: 2px solid #ff00cc; /* neon pink on focus */
            background-color: #1a1a1a; /* dark gray for contrast */
            color: #00ffff; /* neon cyan text */
        }

        /* QComboBox dropdown list */
        QComboBox QAbstractItemView {
            background-color: #000000; /* black list */
            color: #ffff00; /* neon yellow items */
            selection-background-color: #00ffff; /* neon cyan highlight */
            selection-color: #000000; /* black text on selection */
            font-size: 16px;
            border: 2px solid #ff00cc; /* neon pink border */
            border-radius: 4px;
        }

        /* QDateEdit (inherits from QComboBox) */
        QDateEdit {
            background-color: #000000; /* black background */
            color: #ffff00; /* neon yellow text */
            border: 2px solid #00ffff; /* neon cyan border */
            border-radius: 4px;
            padding: 4px;
            font-size: 16px;
        }

        /* QDateEdit on focus */
        QDateEdit:focus {
            border: 2px solid #ff00cc; /* neon pink */
            background-color: #1a1a1a; /* dark gray */
            color: #00ffff; /* neon cyan text */
        }

        /* QDateEdit calendar popup */
        QDateEdit::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 20px;
            border-left: 1px solid #00ffff; /* separates dropdown arrow */
        }

        QCalendarWidget QWidget {
            background-color: #000000; /* black calendar background */
            color: #ffff00; /* neon yellow text */
            border: 2px solid #ff00cc;
        }

        QCalendarWidget QAbstractItemView {
            background-color: #000000; 
            color: #ffff00; 
            selection-background-color: #00ffff; 
            selection-color: #000000;
        }
        '''
    
    def get_retro(self):
        return '''
            /* Global */
            * {
                font-size: 16px;
                font-family: "Press Start 2P", monospace; /* retro pixel font if available */
                color: #ffffff;
            }

            /* QComboBox (general appearance) */
            QDateEdit {
                background-color: #ffb480; /* peach/orange like QGroupBox */
                color: #006400; /* dark green for contrast */
                border: 2px solid #ff6d1f; /* brick orange border */
                border-radius: 4px;
                padding: 4px;
                font-size: 16px;
            }

            /* QComboBox on focus */
            QDateEdit:focus {
                border: 2px solid #006400; /* dark pipe green */
                background-color: #f7f7c6; /* light yellow like QLineEdit:focus */
                color: #000000; /* black text for readability on yellow */
            }

            /* QComboBox dropdown list */
            QDateEdit QAbstractItemView {
                background-color: #ffffff; /* white list background */
                color: #000000; /* black text for readability */
                selection-background-color: #006400; /* dark green selection */
                selection-color: #ffffff; /* white text on selection */
                font-size: 16px;
                border: 2px solid #ff6d1f;
                border-radius: 4px;
            }


            /* QComboBox (general appearance) */
            QComboBox {
                background-color: #ffb480; /* peach/orange like QGroupBox */
                color: #006400; /* dark green for contrast */
                border: 2px solid #ff6d1f; /* brick orange border */
                border-radius: 4px;
                padding: 4px;
                font-size: 16px;
            }

            /* QComboBox on focus */
            QComboBox:focus {
                border: 2px solid #006400; /* dark pipe green */
                background-color: #f7f7c6; /* light yellow like QLineEdit:focus */
                color: #000000; /* black text for readability on yellow */
            }

            /* QComboBox dropdown list */
            QComboBox QAbstractItemView {
                background-color: #ffffff; /* white list background */
                color: #000000; /* black text for readability */
                selection-background-color: #006400; /* dark green selection */
                selection-color: #ffffff; /* white text on selection */
                font-size: 16px;
                border: 2px solid #ff6d1f;
                border-radius: 4px;
            }


            /* QDialog */
            QDialog {
                background-color: #5c94fc; /* sky blue background */
            }

            /* QGroupBox */
            QGroupBox {
                background-color: #ffb480; /* peach/orange (brick block) */
                border: 2px solid #ff6d1f; /* darker orange border */
                border-radius: 6px;
                margin-top: 20px;
                padding: 6px;
            }

            /* QGroupBox::title */
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 2px 6px;
                color: #006400; /* dark pipe green for contrast */
                font-weight: bold;
                font-size: 18px;
            }

            /* QLabel */
            QLabel {
                color: #006400; /* darker text for visibility on blue */
                background: transparent;
                font-size: 18px; /* larger font */
            }

            /* QLineEdit */
            QLineEdit {
                background-color: #ffffff;
                color: #000000;
                border: 2px solid #ff6d1f; /* brick orange border */
                border-radius: 4px;
                padding: 4px;
            }

            /* QLineEdit:focus */
            QLineEdit:focus {
                border: 2px solid #006400; /* darker green pipe */
                background-color: #f7f7c6; /* light yellow, like question blocks */
            }

            /* QTreeWidget */
            QTreeWidget {
                background-color: #a8e4ff; /* light sky blue */
                border: 2px solid #5c94fc;
                show-decoration-selected: 1;
                color: #222222; /* darker text for contrast */
                font-size: 18px; /* larger font */
            }

            /* QTreeWidget column headers */
            QHeaderView::section {
                background-color: #d4d0c8;
                color: #A48B7C;
                font-weight: bold;
                font-size: 14pt; /* increased from 10pt */
                border: 1px solid #a0a0a0;
                padding: 4px;
            }

            /* QTreeWidget::item:selected */
            QTreeWidget::item:selected {
                background-color: #006400; /* darker pipe green */
                color: #ffffff;
            }

            /* QTreeWidget::item:hover */
            QTreeWidget::item:hover {
                background-color: #ffb480; /* brick peach */
                color: #000000;
            }

            /* QTreeWidget column headers */
            QHeaderView::section {
                background-color: #b23a00; /* dark brick red */
                color: #fff200; /* coin gold text */
                font-size: 18px;
                font-weight: bold;
                border: 1px solid #ff6d1f;
                padding: 4px;
            }

            /* QCheckBox */
            QCheckBox {
                spacing: 8px;
                color: #222222; /* readable on blue */
                font-size: 18px; /* larger font */
            }

            /* QCheckBox::indicator */
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #ff6d1f;
                background-color: #ffffff;
            }

            /* QCheckBox::indicator:checked */
            QCheckBox::indicator:checked {
                background-color: #006400; /* darker pipe green */
                border: 2px solid #004d00;
            }

            /* QCheckBox::indicator:unchecked */
            QCheckBox::indicator:unchecked {
                background-color: #ffffff;
            }

            /* QRadioButton */
            QRadioButton {
                spacing: 8px;
                color: #222222; /* readable on blue */
                font-size: 18px;
            }

            /* QRadioButton::indicator */
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
                border-radius: 9px; /* circle */
                border: 2px solid #ff6d1f; /* brick orange border */
                background-color: #ffffff; /* unselected background */
            }

            /* Checked state */
            QRadioButton::indicator:checked {
                background-color: #006400; /* dark pipe green */
                border: 2px solid #004d00; /* darker green outline */
            }

            /* Unchecked state */
            QRadioButton::indicator:unchecked {
                background-color: #ffffff;
            }

            /* Hover state */
            QRadioButton::indicator:hover {
                border: 2px solid #d4af37; /* gold glow */
            }


            /* QPushButton */
            QPushButton {
                background-color: #ff6d1f; /* brick red/orange */
                border: 2px solid #b23a00;
                border-radius: 6px;
                padding: 6px 12px;
                color: #ffffff;
                font-weight: bold;
            }

            /* QPushButton:hover */
            QPushButton:hover {
                background-color: #fff200; /* coin gold */
                color: #000000;
                border: 2px solid #d4af37;
            }

            /* QFileDialog */
            QFileDialog {
                background-color: #f0f0f0; /* light gray */
                color: #000000; /* black text */
            }

            /* File list in QFileDialog */
            QFileDialog QListView,
            QFileDialog QTreeView {
                background-color: #ffffff; /* white background */
                color: #000000; /* black text */
                font-size: 16px;
                selection-background-color: #006400; /* dark green highlight */
                selection-color: #ffffff; /* white text on selection */
            }

            /* File dialog headers */
            QFileDialog QHeaderView::section {
                background-color: #b23a00; /* brick red */
                color: #fff200; /* coin gold */
                font-weight: bold;
                font-size: 16px;
                border: 1px solid #ff6d1f;
                padding: 4px;
            }

        '''
    
    def get_chrome(self):
        return '''
            /* QDialog */
            QDialog {
                background-color: #f1f3f4;
                border: none;
            }

            /* QGroupBox */
            QGroupBox {
                border: 1px solid #dadce0;
                border-radius: 6px;
                margin-top: 20px;
                background-color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 6px;
                color: #202124;
                font-weight: 500;
                font-size: 10pt;
            }

            /* QLabel */
            QLabel {
                color: #3c4043;
                background-color: transparent;
                font-family: "Roboto", "Segoe UI", sans-serif;
                font-size: 10pt;
            }

            /* QLineEdit */
            QLineEdit {
                background-color: #ffffff;
                border: 1px solid #dadce0;
                border-radius: 4px;
                padding: 4px 6px;
                font-family: "Roboto", "Segoe UI", sans-serif;
                font-size: 10pt;
            }
            QLineEdit:focus {
                border: 2px solid #1a73e8;
            }

            /* QTreeWidget */
            QTreeWidget {
                background-color: #ffffff;
                border: 1px solid #dadce0;
                font-family: "Roboto", "Segoe UI", sans-serif;
                font-size: 10pt;
            }

            /* QTreeWidget::item:selected */
            QTreeWidget::item:selected {
                background-color: #e8f0fe;
                color: #1a73e8;
            }

            /* QTreeWidget::item:hover */
            QTreeWidget::item:hover {
                background-color: #f1f3f4;
                color: #202124;
            }

            /* QCheckBox */
            QCheckBox {
                spacing: 6px;
                font-family: "Roboto", "Segoe UI", sans-serif;
                font-size: 10pt;
                color: #202124;
            }

            /* QCheckBox::indicator */
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 2px solid #5f6368;
                border-radius: 2px;
                background-color: #ffffff;
            }

            /* QCheckBox::indicator:checked */
            QCheckBox::indicator:checked {
                background-color: #1a73e8;
                border: 2px solid #1a73e8;
            }

            /* QCheckBox::indicator:unchecked */
            QCheckBox::indicator:unchecked {
                background-color: #ffffff;
                border: 2px solid #5f6368;
            }

            /* QPushButton */
            QPushButton {
                background-color: #f8f9fa;
                border: 1px solid #dadce0;
                border-radius: 4px;
                padding: 6px 12px;
                font-family: "Roboto", "Segoe UI", sans-serif;
                font-size: 10pt;
                color: #202124;
            }

            /* QPushButton::hover */
            QPushButton:hover {
                background-color: #e8eaed;
                border: 1px solid #c1c1c1;
            }

            /* QPushButton:pressed */
            QPushButton:pressed {
                background-color: #d2e3fc;
                border: 1px solid #1a73e8;
                color: #1a73e8;
            }
            '''
    
    def get_paper(self):
        return ''' 
            /* QDialog */
            QDialog {
                background-color: #ece9d8;
                border: 1px solid #a0a0a0;
            }

            /* QFileDialog */
            QFileDialog {
                background-color: #ece9d8; /* same as QDialog background */
                color: #000000; /* black text to match general style */
                font-family: Tahoma;
                font-size: 14pt;
                border: 1px solid #a0a0a0;
            }

            /* File list in QFileDialog */
            QFileDialog QListView,
            QFileDialog QTreeView {
                background-color: #ffffff; /* white background */
                color: #000000; /* black text for readability */
                font-family: Tahoma;
                font-size: 14pt;
                selection-background-color: #0a64ad; /* blue highlight for selection */
                selection-color: #ffffff; /* white text on selection */
                border: 1px solid #a0a0a0;
            }

            /* QFileDialog headers */
            QFileDialog QHeaderView::section {
                background-color: #d4d0c8; /* same as header style elsewhere */
                color: #000000; /* black text for readability */
                font-weight: bold;
                font-size: 14pt;
                border: 1px solid #a0a0a0;
                padding: 4px;
            }

            /* QFileDialog QLineEdit (filename box) */
            QFileDialog QLineEdit {
                background-color: #ffffff; /* match general line edits */
                color: #000000;
                border: 1px solid #7a7a7a;
                border-radius: 4px;
                padding: 4px;
                font-family: Tahoma;
                font-size: 14pt;
            }

            /* QFileDialog QComboBox (file type dropdown) */
            QFileDialog QComboBox {
                background-color: #ffffff; /* match line edits */
                color: #000000;
                border: 1px solid #7a7a7a;
                border-radius: 4px;
                padding: 4px;
                font-family: Tahoma;
                font-size: 14pt;
                min-height: 22px;
            }

            /* QComboBox dropdown list inside QFileDialog */
            QFileDialog QComboBox QAbstractItemView {
                background-color: #ffffff;
                color: #000000;
                selection-background-color: #0a64ad;
                selection-color: #ffffff;
                border: 1px solid #7a7a7a;
                font-family: Tahoma;
                font-size: 14pt;
            }

            /* QGroupBox */
            QGroupBox {
                border: 2px groove #d4d0c8;
                border-radius: 5px;
                margin-top: 20px;
                background-color: #f0f0f0;
                font-family: Tahoma;
                font-size: 14pt; /* increased from 10pt */
                color: #000000;
            }

            /* QGroupBox titles */
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
                color: #A48B7C; /* warm light brown / gray mix */
                font-weight: bold;
                font-size: 14pt;
            }

            /* QLabel */
            QLabel {
                color: #000000;
                background-color: transparent;
                font-family: Tahoma;
                font-size: 14pt; /* increased from 10pt */
            }

            /* QLineEdit */
            QLineEdit {
                background-color: #ffffff;
                border: 1px solid #7a7a7a;
                padding: 2px;
                font-family: Tahoma;
                font-size: 14pt; /* increased from 10pt */
            }

            /* QHeaderView::section (tree headers) */
            QHeaderView::section {
                background-color: #d4d0c8;
                color: #A48B7C; /* warm light brown / gray mix */
                font-weight: bold;
                font-size: 14pt;
                border: 1px solid #a0a0a0;
                padding: 4px;
            }

            /* QTreeWidget */
            QTreeWidget {
                background-color: #ffffff;
                border: 1px solid #a0a0a0;
                font-family: Tahoma;
                font-size: 14pt; /* increased from 10pt */
            }

            /* QTreeWidget column headers */
            QHeaderView::section {
                background-color: #d4d0c8;
                color: #A48B7C;
                font-weight: bold;
                font-size: 14pt; /* increased from 10pt */
                border: 1px solid #a0a0a0;
                padding: 4px;
            }

            /* QTreeWidget items */
            QTreeWidget::item:selected {
                background-color: #0a64ad;
                color: #ffffff;
            }
            
            QTreeWidget::item:hover {
                background-color: #cce8ff;
                color: #000000;
            }

            /* QCheckBox text */
            QCheckBox {
                spacing: 8px;
                font-family: Tahoma;
                font-size: 14pt;
                color: #A48B7C; /* warm light brown / gray mix */
            }

            /* QCheckBox indicators */
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #7a7a7a;
                background-color: #ffffff;
            }

            /* QCheckBox checked state */
            QCheckBox::indicator:checked {
                background-color: #A48B7C; /* fill with warm brown-gray */
                border: 2px solid #7a7a7a;
            }

            /* QCheckBox unchecked state */
            QCheckBox::indicator:unchecked {
                background-color: #ffffff;
                border: 2px solid #7a7a7a;
            }

            /* QRadioButton */
            QRadioButton {
                spacing: 8px;
                font-family: Tahoma;
                font-size: 14pt; /* increased from 10pt */
                color: #000000;
            }
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
                border-radius: 9px;
                border: 2px solid #7a7a7a;
                background-color: #ffffff;
            }
            QRadioButton::indicator:checked {
                background-color: #0a64ad; /* blue fill for checked */
                border: 2px solid #000080;
            }
            QRadioButton::indicator:unchecked {
                background-color: #ffffff;
                border: 2px solid #7a7a7a;
            }

            /* QPushButton */
            QPushButton {
                background-color: #d4d0c8;
                border: 2px outset #ffffff;
                padding: 4px 8px;
                font-family: Tahoma;
                font-size: 14pt; /* increased from 10pt */
            }
            QPushButton:hover {
                background-color: #e4e4e4;
                border: 2px outset #ffffff;
            }
            QPushButton:pressed {
                background-color: #c0c0c0;
                border: 2px inset #808080;
            }

        '''

    def get_monochrome_style(self):
        return''' 
        * {
            font-family: "Segoe UI", sans-serif;
            font-size: 20px;
            color: #1a1a1a;
            background-color: #eeeeee;
        }

        QDialog {
            border: 2px solid #444444;
        }

        QGroupBox {
            border: 2px solid #444444;
            border-radius: 10px;
            margin-top: 10px;
            padding: 10px;
            background-color: #f0f0f0;
        }

        QLabel {
            font-size: 20px;
            font-weight: bold;
            color: #000000;
        }

        
        QLineEdit {
            background-color: #ffffff;
            border: 1px solid #666666;
            border-radius: 4px;
            padding: 6px;
            color: #1a1a1a;
            font-size: 16px;
        }

        QCheckBox {
            font-size: 18px;
        }

        
        QPushButton {
            background-color: rgba(50, 50, 50, 0.9);
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
        }

        
        QPushButton:hover {
            background-color: rgba(30, 30, 30, 0.5);
        }

        
        QPushButton:pressed {
            background-color: rgba(90, 90, 90, 1.0);
        }'''

   
        return ''' 
            QWidget {
                background-color: #1e1e1e;
                color: #e0e0e0;
                font-family: "Segoe UI", sans-serif;
            }

            QPushButton {
                background-color: #2e2e2e;
                color: #e0e0e0;
                border: 1px solid #444;
                padding: 6px;
            }

            QLineEdit {
                background-color: #2e2e2e;
                color: #e0e0e0;
                border: 1px solid #666;
                padding: 4px;
            }

            QTextEdit {
                background-color: #2e2e2e;
                color: #e0e0e0;
                border: 1px solid #666;
                padding: 6px;
            }

            QComboBox {
                background-color: #2e2e2e;
                color: #e0e0e0;
                border: 1px solid #444;
                padding: 4px;
            }
        '''
    
    def get_monochrome_img_style(self):
        return''' 
        * {
            font-family: "Segoe UI", sans-serif;
            font-size: 20px;
            color: #1a1a1a;
            background-color: #eeeeee;
        }

        QDialog {
            border: 2px solid #444444;
        }

        QGroupBox {
            border: 2px solid #444444;
            border-radius: 10px;
            margin-top: 10px;
            padding: 10px;
            background-color: #f0f0f0;
        }

        QLabel {
            font-size: 20px;
            font-weight: bold;
            color: #000000;
        }

        
        QLineEdit {
            background-color: #ffffff;
            border: 1px solid #666666;
            border-radius: 4px;
            padding: 6px;
            color: #1a1a1a;
            font-size: 16px;
        }

        QTreeWidget {
            font-size: 20px;
        }

        QTreeWidget::item:selected {
            background-color: #b7b7b7;   /* Highlight color */
            color: black;                /* Text color */
        }

        QTreeWidget::item:hover {
            background-color: #434343;   /* Optional hover effect */
            color: #f3f3f3;
        }

        QCheckBox {
            font-size: 18px;
        }

        QCheckBox::indicator {
        width: 16px;
        height: 16px;
        border: 2px solid white;
        border-radius: 4px;
        background-color: black;
        }

        QCheckBox::indicator:checked {
            background-color: white;
            border: 2px solid black;
        }

        QCheckBox::indicator:unchecked {
            background-color: darlgray;
            border: 2px solid white;
        }

        QPushButton {
            background-color: rgba(50, 50, 50, 0.9);
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
        }

        
        QPushButton:hover {
            background-color: rgba(30, 30, 30, 0.5);
        }

        
        QPushButton:pressed {
            background-color: rgba(90, 90, 90, 1.0);
        }'''

    def get_modern_style(self):
        return '''
            * {
                font-family: "Segoe UI", sans-serif;
                font-size: 20px;
                color: #f2f2f2;
                background-color: #333333;
            }

            QDialog {
                border: 2px solid #0033cc;
                background-color: #333333;
            }

            QGroupBox {
                border: 2px solid #0033cc;
                border-radius: 10px;
                margin-top: 10px;
                padding: 10px;
                background-color: #333333;
            }

            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #f2f2f2;
                border-radius: 10px;
            }

            QLineEdit {
                background-color: #333333;
                border: 1px solid #6600cc;
                border-radius: 4px;
                padding: 6px;
                color: #f2f2f2;
                font-size: 18px;
            }

            QTreeWidget {
                font-size: 20px;
                background-color: #333333;
                color: #f2f2f2;
                border-radius: 10px;
                border: 2px solid #0033cc;
            }

            QTreeWidget::item {
                font-size: 20px;
                background-color: #666666;
                color: #f2f2f2;
                border: 1px solid #6600cc;
                border-radius: 2px;
            }

            QTreeWidget::item:selected {
                background-color: #0033cc;
                
            }

            QTreeWidget::item:hover {
                background-color: #333333;
                color: #f2f2f2;
                border-radius: 6px;
            }

            QCheckBox {
                font-size: 18px;
                color: #f2f2f2;
            }

            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 2px solid #ffffff;
                border-radius: 4px;
                background-color:#333333;
            }

            QCheckBox::indicator:checked {
                background-color: #ffffff;
                border: 2px solid #333333;
            }

            QCheckBox::indicator:unchecked {
                background-color: #6600cc;
                border: 2px solid #ffffff;
            }

            QPushButton {
                background-color: rgba(51, 51, 51, 0.6); /* Soft black */
                color: #f2f2f2;
                border: 2px solid #6600cc;
                border-radius: 6px;
                padding: 8px 16px;
                text-align: center;
            }

            QPushButton:hover {
                background-color: #666666;
                
            }

            QPushButton:pressed {
                background-color: #6600cc;
            }
        '''

    def get_neopolitan_style(self):
      return """
        * {
            font-size: 16px;
        }

        /* QDialog */
        QDialog {
            background-color: #fff8f0; /* vanilla cream */
            border: 1px solid #d8cfc4;
            border-radius: 8px;
        }
        

        /* QGroupBox */
        QGroupBox {
            background-color: #fbe3e8; /* strawberry blush */
            border: 1px solid #e0bfc4;
            border-radius: 6px;
            margin-top: 20px;
            padding: 6px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 6px;
            color: #6b4c3b; /* chocolate accent */
            font-weight: bold;
            font-size: 12pt;
        }

        /* QLabel */
        QLabel {
            color: #5a4a42;
            background-color: transparent;
            font-family: "Segoe UI", sans-serif;
            font-size: 14pt;
        }

        /* QLineEdit */
        QLineEdit {
            background-color: #fffaf6;
            border: 1px solid #d8cfc4;
            border-radius: 6px;
            padding: 4px 6px;
            font-family: "Segoe UI", sans-serif;
            font-size: 14pt;
        }
        QLineEdit:focus {
            border: 2px solid #f4b6c2; /* strawberry highlight */
        }

        /* QTreeWidget */
        QTreeWidget {
            background-color: #fffaf6;
            border: 1px solid #d8cfc4;
            font-family: "Segoe UI", sans-serif;
            font-size: 12pt;
        }

        /* QTreeWidget::item:selected */
        QTreeWidget::item:selected {
            background-color: #f4b6c2; /* strawberry */
            color: #6b4c3b;
        }

        /* QTreeWidget::item:hover */
        QTreeWidget::item:hover {
            background-color: #fceeea;
            color: #6b4c3b;
        }

        /* QCheckBox */
        QCheckBox {
            spacing: 6px;
            font-family: "Segoe UI", sans-serif;
            font-size: 12pt;
            color: #5a4a42;
        }

        /* QCheckBox::indicator */
        QCheckBox::indicator {
            width: 16px;
            height: 16px;
            border-radius: 4px;
            border: 1px solid #c8b8a8;
            background-color: #fffaf6;
        }

        /* QCheckBox::indicator:checked */
        QCheckBox::indicator:checked {
            background-color: #a9746e;
            border: 1px solid #6b4c3b;
        }

        /* QCheckBox::indicator:unchecked */
        QCheckBox::indicator:unchecked {
            background-color: #fffaf6;
            border: 1px solid #c8b8a8;
        }

        /* QPushButton:hover */
        QPushButton:hover {
            background-color: #a9746e; /* cinnamon warmth */
            border: 1px solid #6b4c3b;
            color: #fffaf6;
        }

        /* QGroupBox::title */
        QGroupBox::title {
            color: #a9746e; /* cinnamon accent */
        }

        /* QHeaderView::section (Tree Widget column headers) */
        QHeaderView::section {
            background-color: #fbe3e8; /* strawberry blush, same as QGroupBox */
            color: #6b4c3b; /* chocolate accent */
            font-weight: bold;
            font-size: 12pt;
            border: 1px solid #e0bfc4;
            padding: 4px;
        }

        /* QRadioButton */
        QRadioButton {
            spacing: 6px;
            font-family: "Segoe UI", sans-serif;
            font-size: 12pt;
            color: #5a4a42; /* dark chocolate text */
        }

        /* QRadioButton indicator */
        QRadioButton::indicator {
            width: 16px;
            height: 16px;
            border-radius: 8px;
            border: 1px solid #c8b8a8; /* light brown border */
            background-color: #fffaf6; /* vanilla cream background */
        }

        /* QRadioButton indicator checked */
        QRadioButton::indicator:checked {
            background-color: #a9746e; /* cinnamon accent fill */
            border: 1px solid #6b4c3b; /* chocolate border */
        }

        /* QRadioButton indicator unchecked */
        QRadioButton::indicator:unchecked {
            background-color: #fffaf6; /* vanilla cream */
            border: 1px solid #c8b8a8;
        }

        /* QFileDialog */
        QFileDialog {
            background-color: #fff8f0; /* vanilla cream, same as QDialog */
            color: #5a4a42; /* chocolate accent text */
            font-family: "Segoe UI", sans-serif;
            font-size: 14pt;
            border: 1px solid #d8cfc4;
        }

        /* File list in QFileDialog */
        QFileDialog QListView,
        QFileDialog QTreeView {
            background-color: #fffaf6; /* vanilla cream list background */
            color: #5a4a42; /* chocolate accent text */
            font-family: "Segoe UI", sans-serif;
            font-size: 12pt;
            selection-background-color: #f4b6c2; /* strawberry highlight */
            selection-color: #6b4c3b; /* chocolate text on selection */
            border: 1px solid #d8cfc4;
        }

        /* QFileDialog headers */
        QFileDialog QHeaderView::section {
            background-color: #fbe3e8; /* strawberry blush header */
            color: #6b4c3b; /* chocolate accent */
            font-weight: bold;
            font-size: 12pt;
            border: 1px solid #e0bfc4;
            padding: 4px;
        }

        /* QFileDialog QLineEdit (filename box) */
        QFileDialog QLineEdit {
            background-color: #fffaf6; /* vanilla cream */
            color: #5a4a42; /* chocolate text */
            border: 1px solid #d8cfc4;
            border-radius: 6px;
            padding: 4px 6px;
            font-family: "Segoe UI", sans-serif;
            font-size: 14pt;
        }

        /* QFileDialog QComboBox (file type dropdown) */
        QFileDialog QComboBox {
            background-color: #fffaf6;
            color: #5a4a42;
            border: 1px solid #d8cfc4;
            border-radius: 6px;
            padding: 4px;
            font-family: "Segoe UI", sans-serif;
            font-size: 14pt;
            min-height: 22px;
        }

        /* QComboBox dropdown list inside QFileDialog */
        QFileDialog QComboBox QAbstractItemView {
            background-color: #fffaf6;
            color: #5a4a42;
            selection-background-color: #f4b6c2;
            selection-color: #6b4c3b;
            border: 1px solid #d8cfc4;
            font-family: "Segoe UI", sans-serif;
            font-size: 12pt;
        }

      """
    
    def get_old_school_style(self):
        return '''
            * {
            font-size: 16px;
            }

            QWidget {
                background-color: #f5f5f5;
                font-family: 'Segoe UI';
                font-size: 10pt;
            }

            QLabel {
                color: #333;
            }

            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #388e3c;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }

            QLineEdit {
                border: 1px solid #aaa;
                border-radius: 4px;
                padding: 4px;
                background-color: white;
                selection-background-color: #0078d7;
            }

            QComboBox {
                padding: 4px;
                border: 1px solid #888;
                border-radius: 4px;
            }
            QComboBox::drop-down {
                border-left: 1px solid #888;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                selection-background-color: #d0eaff;
            }

            QCheckBox {
                spacing: 5px;
            }
            QCheckBox::indicator:checked {
                background-color: #0078d7;
            }
            QCheckBox::indicator:unchecked {
                background-color: #ccc;
            }

            QRadioButton::indicator:checked {
                background-color: #0078d7;
            }
            QRadioButton::indicator:unchecked {
                background-color: #ccc;
            }

            QTabWidget::pane {
                border: 1px solid #aaa;
            }
            QTabBar::tab {
                background: #ccc;
                padding: 6px;
            }
            QTabBar::tab:selected {
                background: #eee;
            }

            QSlider::groove:horizontal {
                height: 6px;
                background: #ddd;
            }
            QSlider::handle:horizontal {
                background: #0078d7;
                width: 14px;
            }

            QProgressBar {
                border: 1px solid #aaa;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                width: 20px;
            }

            QScrollBar:vertical {
                background: #f0f0f0;
                width: 12px;
            }
            QScrollBar::handle:vertical {
                background: #999;
                min-height: 20px;
            }

            QListWidget {
                background: white;
                border: 1px solid #ccc;
            }
            QListWidget::item:selected {
                background-color: #d0eaff;
            }

            QTreeView::branch:has-children:!has-siblings:closed,
            QTreeView::branch:closed:has-children:has-siblings {
                image: url(:/icons/branch_closed.png);
            }
            QTreeView::branch:open:has-children:!has-siblings,
            QTreeView::branch:open:has-children:has-siblings  {
                image: url(:/icons/branch_open.png);
            }

            QToolTip {
                background-color: #ffffdc;
                color: #000;
                border: 1px solid gray;
            }

            QMenuBar {
                background-color: #efefef;
            }
            QMenuBar::item:selected {
                background-color: #dcdcdc;
            }

            QMenu {
                background-color: #ffffff;
            }
            QMenu::item:selected {
                background-color: #0078d7;
                color: white;
            }

            QSpinBox {
                border: 1px solid #aaa;
                padding: 2px 4px;
                border-radius: 4px;
            }

            QDateEdit {
                border: 1px solid #aaa;
                border-radius: 4px;
                padding: 4px;
            }

            QToolBar {
                background: #eee;
                border-bottom: 1px solid #ccc;
            }
            QToolButton {
                background: transparent;
            }
            QToolButton:hover {
                background: #d0eaff;
            }

            QTextEdit {
                border: 1px solid #aaa;
                background-color: white;
                selection-background-color: #0078d7;
            }

            QFrame {
                border: 1px solid #ccc;
                border-radius: 6px;
            }

            QGroupBox {
                border: 1px solid #aaa;
                border-radius: 4px;
                margin-top: 6px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }

            QCalendarWidget QToolButton {
                background-color: #0078d7;
                color: white;
                border: none;
            }

            QMessageBox QPushButton {
                min-width: 80px;
                padding: 6px;
            }

            QDialog {
                background-color: #f0f0f0;
                border: 1px solid #aaa;
            }
            '''
    
    def get_hand_drawn(self):
        return """
        /* Global */
        * {
            font-size: 16px;
        }

        /* Base QWidget */
        QWidget {
            background-color: #fdf6e3; /* cream base */
            color: #3c2f2f; /* chocolate text */
            font-family: "Courier New", monospace;
            border: 1px dashed #a89f91; /* light brown border */
            border-radius: 2px;
        }

        /* QDialog */
        QDialog {
            background-color: #fdf6e3;
            border: 1px solid #a89f91;
            border-radius: 8px;
        }

        /* QGroupBox */
        QGroupBox {
            background-color: #e6d3b3; /* light cinnamon blush */
            border: 1px solid #8b7d6b; /* brown border */
            border-radius: 6px;
            margin-top: 20px;
            padding: 6px;
            font-family: "Courier New", monospace;
            font-size: 16px;
            color: #3c2f2f;
        }

        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 6px;
            color: #997300; /* deeper cinnamon accent */
            font-weight: bold;
            font-size: 16px;
        }

        /* QLabel */
        QLabel {
            color: #3c2f2f;
            background-color: transparent;
            font-family: "Courier New", monospace;
            font-size: 16px;
        }

        /* QLineEdit */
        QLineEdit {
            background-color: #fffaf0;
            color: #3c2f2f;
            border: 1px dashed #a89f91;
            border-radius: 6px;
            padding: 4px;
            font-family: "Courier New", monospace;
            font-size: 16px;
        }

        QLineEdit:focus {
            border: 2px solid #997300;
        }

        /* QTextEdit */
        QTextEdit {
            background-color: #fffaf0;
            color: #3c2f2f;
            border: 1px dashed #a89f91;
            padding: 6px;
            font-family: "Courier New", monospace;
            font-size: 16px;
        }

        /* QComboBox */
        QComboBox {
            background-color: #e6d3b3;
            color: #3c2f2f;
            border: 1px dashed #8b7d6b;
            border-radius: 6px;
            padding: 4px;
            font-family: "Courier New", monospace;
            font-size: 16px;
            min-height: 22px;
        }

        QComboBox:focus {
            border: 2px solid #997300;
            background-color: #fffaf0;
        }

        /* QComboBox dropdown list */
        QComboBox QAbstractItemView {
            background-color: #fffaf0;
            color: #3c2f2f;
            selection-background-color: #e6d3b3;
            selection-color: #3c2f2f;
            border: 1px dashed #a89f91;
            font-family: "Courier New", monospace;
            font-size: 16px;
        }

        /* QDateEdit */
        QDateEdit {
            background-color: #fffaf0;
            color: #3c2f2f;
            border: 1px dashed #a89f91;
            border-radius: 6px;
            padding: 4px;
            font-family: "Courier New", monospace;
            font-size: 16px;
        }

        QDateEdit:focus {
            border: 2px solid #997300;
        }

        /* QTreeWidget */
        QTreeWidget {
            background-color: #fffaf0;
            border: 1px dashed #a89f91;
            font-family: "Courier New", monospace;
            font-size: 16px;
        }

        /* QTreeWidget column headers */
        QHeaderView::section {
            background-color: #e6d3b3;
            color: #3c2f2f;
            font-weight: bold;
            font-size: 16px;
            border: 1px solid #8b7d6b;
            padding: 4px;
        }

        /* QTreeWidget items */
        QTreeWidget::item:selected {
            background-color: #997300;
            color: #fffaf0;
        }

        QTreeWidget::item:hover {
            background-color: #fbe3e8;
            color: #3c2f2f;
        }

        /* QCheckBox */
        QCheckBox {
            spacing: 6px;
            font-family: "Courier New", monospace;
            font-size: 16px;
            color: #3c2f2f;
        }

        QCheckBox::indicator {
            width: 16px;
            height: 16px;
            border-radius: 4px;
            border: 1px solid #a89f91;
            background-color: #fffaf0;
        }

        QCheckBox::indicator:checked {
            background-color: #997300;
            border: 1px solid #3c2f2f;
        }

        QCheckBox::indicator:unchecked {
            background-color: #fffaf0;
            border: 1px solid #a89f91;
        }

        /* QRadioButton */
        QRadioButton {
            spacing: 6px;
            font-family: "Courier New", monospace;
            font-size: 16px;
            color: #3c2f2f;
        }

        QRadioButton::indicator {
            width: 16px;
            height: 16px;
            border-radius: 8px;
            border: 1px solid #a89f91;
            background-color: #fffaf0;
        }

        QRadioButton::indicator:checked {
            background-color: #997300;
            border: 1px solid #3c2f2f;
        }

        QRadioButton::indicator:unchecked {
            background-color: #fffaf0;
            border: 1px solid #a89f91;
        }

        /* QPushButton */
        QPushButton {
            background-color: #e6d3b3;
            color: #3c2f2f;
            border: 2px dashed #8b7d6b;
            padding: 6px;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #997300;
            border: 2px dashed #3c2f2f;
            color: #fffaf0;
        }

        /* QFileDialog */
        QFileDialog {
            background-color: #fdf6e3;
            color: #3c2f2f;
            font-family: "Courier New", monospace;
            font-size: 16px;
            border: 1px solid #a89f91;
        }

        QFileDialog QListView,
        QFileDialog QTreeView {
            background-color: #fffaf0;
            color: #3c2f2f;
            font-family: "Courier New", monospace;
            font-size: 16px;
            selection-background-color: #e6d3b3;
            selection-color: #3c2f2f;
            border: 1px dashed #a89f91;
        }

        QFileDialog QHeaderView::section {
            background-color: #e6d3b3;
            color: #3c2f2f;
            font-weight: bold;
            font-size: 16px;
            border: 1px solid #8b7d6b;
            padding: 4px;
        }

        QFileDialog QLineEdit {
            background-color: #fffaf0;
            color: #3c2f2f;
            border: 1px dashed #a89f91;
            border-radius: 6px;
            padding: 4px 6px;
            font-family: "Courier New", monospace;
            font-size: 16px;
        }

        QFileDialog QComboBox {
            background-color: #e6d3b3;
            color: #3c2f2f;
            border: 1px dashed #8b7d6b;
            border-radius: 6px;
            padding: 4px;
            font-family: "Courier New", monospace;
            font-size: 16px;
            min-height: 22px;
        }

        QFileDialog QComboBox QAbstractItemView {
            background-color: #fffaf0;
            color: #3c2f2f;
            selection-background-color: #e6d3b3;
            selection-color: #3c2f2f;
            border: 1px dashed #a89f91;
            font-family: "Courier New", monospace;
            font-size: 16px;
        }
    """

    def get_baseball(self):
        return '''
            /* Global */
            * {
                font-family: "Segoe UI", sans-serif;
                font-size: 16px;
                color: #2e2e2e; /* dark charcoal text for readability */
            }

            /* Base QWidget */
            QWidget {
                background-color: #a3c77f; /* baseball field grass */
                color: #2e2e2e;
                border-radius: 2px;
            }

            /* QDialog */
            QDialog {
                background-color: #f4e2c1; /* sandy stadium paths */
                border: 2px solid #7d5a3c; /* brown dugout wood */
                border-radius: 8px;
            }

            /* QGroupBox */
            QGroupBox {
                background-color: #e0d8c1; /* bleacher seating */
                border: 2px solid #7d5a3c; /* wood trim */
                border-radius: 6px;
                margin-top: 20px;
                padding: 6px;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 6px;
                color: #7d5a3c; /* wood-tone title */
                font-weight: bold;
                font-size: 16pt;
            }

            /* QLabel */
            QLabel {
                color: #2e2e2e;
                background-color: transparent;
                font-size: 14pt;
            }

            /* QLineEdit */
            QLineEdit {
                background-color: #fff1d6; /* chalky infield lines */
                color: #2e2e2e;
                border: 1px solid #7d5a3c;
                border-radius: 4px;
                padding: 4px 6px;
            }

            /* QTextEdit */
            QTextEdit {
                background-color: #fff1d6;
                color: #2e2e2e;
                border: 1px solid #7d5a3c;
                padding: 6px;
            }

            /* QPushButton */
            QPushButton {
                background-color: #7d5a3c; /* brown wood plank */
                color: #f4e2c1; /* sandy text */
                border: 2px solid #5c4032;
                border-radius: 6px;
                padding: 6px 12px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #996633; /* brighter wood */
                color: #fff1d6;
            }

            /* QComboBox */
            QComboBox {
                background-color: #e0d8c1;
                color: #2e2e2e;
                border: 1px solid #7d5a3c;
                border-radius: 4px;
                padding: 4px;
            }

            QComboBox:focus {
                border: 2px solid #996633;
                background-color: #fff1d6;
            }

            /* QComboBox dropdown list */
            QComboBox QAbstractItemView {
                background-color: #fff1d6;
                color: #2e2e2e;
                selection-background-color: #7d5a3c;
                selection-color: #fff1d6;
            }

            /* QDateEdit */
            QDateEdit {
                background-color: #fff1d6;
                color: #2e2e2e;
                border: 1px solid #7d5a3c;
                border-radius: 4px;
                padding: 4px;
            }

            /* QTreeWidget */
            QTreeWidget {
                background-color: #a3c77f; /* grass */
                color: #2e2e2e;
                border: 1px solid #7d5a3c;
                font-size: 14pt;
            }

            QTreeWidget::item:selected {
                background-color: #996633; /* dirt-colored selection */
                color: #fff1d6;
            }

            QTreeWidget::item:hover {
                background-color: #c8e3a0; /* light grass highlight */
            }

            /* QTreeWidget column headers */
            QHeaderView::section {
                background-color: #7d5a3c; /* wood tone */
                color: #fff1d6;
                font-weight: bold;
                font-size: 14pt;
                border: 1px solid #5c4032;
                padding: 4px;
            }

            /* QCheckBox */
            QCheckBox {
                spacing: 6px;
                font-size: 14pt;
                color: #2e2e2e;
            }

            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 1px solid #7d5a3c;
                background-color: #fff1d6;
            }

            QCheckBox::indicator:checked {
                background-color: #996633;
                border: 1px solid #5c4032;
            }

            QCheckBox::indicator:unchecked {
                background-color: #fff1d6;
                border: 1px solid #7d5a3c;
            }

            /* QRadioButton */
            QRadioButton {
                spacing: 6px;
                font-size: 14pt;
                color: #2e2e2e;
            }

            QRadioButton::indicator {
                width: 16px;
                height: 16px;
                border-radius: 8px;
                border: 1px solid #7d5a3c;
                background-color: #fff1d6;
            }

            QRadioButton::indicator:checked {
                background-color: #996633;
                border: 1px solid #5c4032;
            }

            /* QFileDialog */
            QFileDialog {
                background-color: #f4e2c1;
                color: #2e2e2e;
                border: 1px solid #7d5a3c;
            }

            QFileDialog QListView,
            QFileDialog QTreeView {
                background-color: #fffaf0;
                color: #2e2e2e;
                selection-background-color: #7d5a3c;
                selection-color: #fff1d6;
            }

            QFileDialog QHeaderView::section {
                background-color: #7d5a3c;
                color: #fff1d6;
                border: 1px solid #5c4032;
                font-weight: bold;
                font-size: 14pt;
            }

            QFileDialog QLineEdit {
                background-color: #fffaf0;
                color: #2e2e2e;
                border: 1px solid #7d5a3c;
                border-radius: 4px;
                padding: 4px;
            }

            QFileDialog QComboBox {
                background-color: #e0d8c1;
                color: #2e2e2e;
                border: 1px solid #7d5a3c;
                border-radius: 4px;
                padding: 4px;
            }

            '''