import sys
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QAction, QToolBar
from PyQt5.QtWebEngineWidgets import QWebEngineView

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("LIA Digital QT")
        self.setGeometry(300, 100, 1200, 800)

        # Add tab widget for tabs
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)

        # Load the initial URL in the first tab
        self.add_new_tab("https://digital.lia.co.id")

        # Create zoom in/out actions
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        zoom_in_action = QAction('Zoom In', self)
        zoom_in_action.triggered.connect(self.zoom_in)
        toolbar.addAction(zoom_in_action)

        zoom_out_action = QAction('Zoom Out', self)
        zoom_out_action.triggered.connect(self.zoom_out)
        toolbar.addAction(zoom_out_action)

        new_tab_action = QAction('New Tab', self)
        new_tab_action.triggered.connect(lambda: self.add_new_tab())
        toolbar.addAction(new_tab_action)

        # Add navigation actions: Home, Back, Forward
        home_action = QAction('Home', self)
        home_action.triggered.connect(lambda: self.tabs.currentWidget().setUrl(QUrl("https://digital.lia.co.id")))
        toolbar.addAction(home_action)

        back_action = QAction('Back', self)
        back_action.triggered.connect(lambda: self.tabs.currentWidget().back())
        toolbar.addAction(back_action)

        forward_action = QAction('Forward', self)
        forward_action.triggered.connect(lambda: self.tabs.currentWidget().forward())
        toolbar.addAction(forward_action)

    def add_new_tab(self, url=None):
        """Add a new tab with the specified URL."""
        if url is None:
            url = "https://digital.lia.co.id"
        browser = QWebEngineView()
        browser.setUrl(QUrl(url))
        browser.titleChanged.connect(lambda title: self.tabs.setTabText(self.tabs.indexOf(browser), title))
        self.tabs.addTab(browser, "New Tab")
        self.tabs.setCurrentWidget(browser)

    def close_tab(self, index):
        """Close the tab at the given index."""
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def zoom_in(self):
        """Zoom in on the current tab."""
        current_tab = self.tabs.currentWidget()
        current_tab.setZoomFactor(current_tab.zoomFactor() + 0.1)

    def zoom_out(self):
        """Zoom out on the current tab."""
        current_tab = self.tabs.currentWidget()
        current_tab.setZoomFactor(current_tab.zoomFactor() - 0.1)
        
def closeEvent(self, event):
    """Handle the window close event."""
    # Clear cache for all profiles
    self.profile.clearAllVisitedLinks()
    self.profile.clearHttpCache()
    
    # Iterate through all tabs and clear their individual caches
    for i in range(self.tabs.count()):
        webview = self.tabs.widget(i)
        page = webview.page()
        profile = page.profile()
        profile.clearAllVisitedLinks()
        profile.clearHttpCache()
    
    # Accept the close event
    event.accept()    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())