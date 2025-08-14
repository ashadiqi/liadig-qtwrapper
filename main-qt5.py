import sys
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QAction, QToolBar, QLineEdit, QWidget, QHBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtGui import QIcon

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("LIA Digital QT")
        self.setGeometry(300, 100, 1200, 800)

        # Tab widget 
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)

        # URL for the first tab
        self.add_new_tab("https://digital.lia.co.id")

        # Toolbar and actions
        toolbar = QToolBar()
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.addToolBar(toolbar)

        zoom_in_action = QAction(QIcon.fromTheme("zoom-in"), 'Zoom In', self)
        zoom_in_action.triggered.connect(self.zoom_in)
        toolbar.addAction(zoom_in_action)

        zoom_out_action = QAction(QIcon.fromTheme("zoom-out"), 'Zoom Out', self)
        zoom_out_action.triggered.connect(self.zoom_out)
        toolbar.addAction(zoom_out_action)

        new_tab_action = QAction(QIcon.fromTheme("tab-new"), 'New Tab', self)
        new_tab_action.triggered.connect(lambda: self.add_new_tab())
        toolbar.addAction(new_tab_action)

        home_action = QAction(QIcon.fromTheme("go-home"), 'Home', self)
        home_action.triggered.connect(lambda: self.tabs.currentWidget().setUrl(QUrl("https://digital.lia.co.id")))
        toolbar.addAction(home_action)

        back_action = QAction(QIcon.fromTheme("go-previous"), 'Back', self)
        back_action.triggered.connect(lambda: self.tabs.currentWidget().back())
        toolbar.addAction(back_action)

        forward_action = QAction(QIcon.fromTheme("go-next"), 'Forward', self)
        forward_action.triggered.connect(lambda: self.tabs.currentWidget().forward())
        toolbar.addAction(forward_action)

        # Widget for the search function
        search_widget = QWidget()
        search_layout = QHBoxLayout()
        search_widget.setLayout(search_layout)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Find in page...")
        self.search_input.returnPressed.connect(self.find_next)
        search_layout.addWidget(self.search_input)

        toolbar.addWidget(search_widget)

        find_next_action = QAction(QIcon.fromTheme("go-down"), 'Find Next', self)
        find_next_action.triggered.connect(self.find_next)
        toolbar.addAction(find_next_action)

        find_prev_action = QAction(QIcon.fromTheme("go-up"), 'Find Previous', self)
        find_prev_action.triggered.connect(self.find_prev)
        toolbar.addAction(find_prev_action)
    
    def add_new_tab(self, url=None):
        if url is None:
            url = "https://digital.lia.co.id"
        browser = QWebEngineView()
        browser.setUrl(QUrl(url))
        browser.titleChanged.connect(lambda title: self.tabs.setTabText(self.tabs.indexOf(browser), title))
        self.tabs.addTab(browser, "New Tab")
        self.tabs.setCurrentWidget(browser)

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def zoom_in(self):
        current_tab = self.tabs.currentWidget()
        current_tab.setZoomFactor(current_tab.zoomFactor() + 0.1)

    def zoom_out(self):
        current_tab = self.tabs.currentWidget()
        current_tab.setZoomFactor(current_tab.zoomFactor() - 0.1)
    
    def find_next(self):
        current_tab = self.tabs.currentWidget()
        if isinstance(current_tab, QWebEngineView):
            flags = QWebEnginePage.FindFlags(0)
            current_tab.findText(self.search_input.text(), flags)

    def find_prev(self):
        current_tab = self.tabs.currentWidget()
        if isinstance(current_tab, QWebEngineView):
            flags = QWebEnginePage.FindFlags(QWebEnginePage.FindBackward)
            current_tab.findText(self.search_input.text(), flags)

    def closeEvent(self, event):
        # Clear cache
        for i in range(self.tabs.count()):
            webview = self.tabs.widget(i)
            page = webview.page()
            profile = page.profile()
            profile.clearAllVisitedLinks()
            profile.clearHttpCache()
        
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())