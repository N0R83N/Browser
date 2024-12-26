# Redesigned Browser Implementation with Advanced Customization Tools, Shortcuts, and Session Persistence

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QToolBar, QAction,
                             QColorDialog, QPushButton, QTabWidget, QMenu, QDialog, QFormLayout, QLineEdit, QLabel)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5.QtCore import QUrl

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nijat Browser")
        self.setGeometry(100, 100, 1200, 800)

        # Mərkəzi widget yarat
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Əsas tərtibat
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Naviqasiya düymələri və URL çubuğu üçün alətlər paneli
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Google-də axtarış edin və ya URL daxil edin")
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        # Naviqasiya düymələri əlavə olunur
        back_button = QAction("Geri", self)
        back_button.triggered.connect(self.navigate_back)
        self.toolbar.addAction(back_button)

        forward_button = QAction("İrəli", self)
        forward_button.triggered.connect(self.navigate_forward)
        self.toolbar.addAction(forward_button)

        reload_button = QAction("Yenilə", self)
        reload_button.triggered.connect(self.reload_page)
        self.toolbar.addAction(reload_button)

        home_button = QAction("Əsas", self)
        home_button.triggered.connect(self.navigate_home)
        self.toolbar.addAction(home_button)

        self.toolbar.addWidget(self.url_bar)

        # Fərdiləşdirmə üçün parametrlər düyməsi əlavə olunur
        settings_button = QAction("Parametrlər", self)
        settings_button.triggered.connect(self.open_settings)
        self.toolbar.addAction(settings_button)

        # Yeni tab əlavə etmək üçün düymə
        new_tab_button = QAction("Yeni Tab", self)
        new_tab_button.triggered.connect(self.create_new_tab)
        self.toolbar.addAction(new_tab_button)

        # Tarix menyusu əlavə olunur
        history_menu = QMenu("Tarixçə", self)
        self.history_action = QAction("Tarixçəni Göstər", self)
        self.history_action.triggered.connect(self.show_history)
        history_menu.addAction(self.history_action)
        self.menuBar().addMenu(history_menu)

        # Qısayollar menyusu
        shortcuts_menu = QMenu("Qısayollar", self)
        self.shortcut_action = QAction("Qısayolları İdarə et", self)
        self.shortcut_action.triggered.connect(self.manage_shortcuts)
        shortcuts_menu.addAction(self.shortcut_action)
        self.menuBar().addMenu(shortcuts_menu)

        # Çoxsaylı tablar üçün tab widgetı
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        layout.addWidget(self.tabs)

        # İlk tab əlavə olunur
        self.add_new_tab(QUrl("https://www.google.com"), "Əsas")

        # Tarixçə saxlanması
        self.history = []

        # Qısayolların saxlanması
        self.shortcuts = {"Google": "https://www.google.com", "YouTube": "https://www.youtube.com"}

        # Qısayollar üçün alətlər paneli yaradılır
        self.shortcut_toolbar = QToolBar("Qısayollar", self)
        self.addToolBar(self.shortcut_toolbar)
        self.update_shortcuts()

    def add_new_tab(self, qurl, label):
        browser = QWebEngineView()
        profile = QWebEngineProfile.defaultProfile()
        profile.setPersistentCookiesPolicy(QWebEngineProfile.AllowPersistentCookies)
        profile.setCachePath("cache")
        profile.setPersistentStoragePath("storage")

        browser.setUrl(qurl)
        index = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(index)
        browser.urlChanged.connect(lambda url, browser=browser: self.update_tab_title(browser, url))
        browser.urlChanged.connect(self.record_history)

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def update_tab_title(self, browser, qurl):
        index = self.tabs.indexOf(browser)
        if index != -1:
            self.tabs.setTabText(index, qurl.toString()[:15] + "...")

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://www.google.com/search?q=" + url
        self.tabs.currentWidget().setUrl(QUrl(url))

    def navigate_back(self):
        if self.tabs.currentWidget().history().canGoBack():
            self.tabs.currentWidget().back()

    def navigate_forward(self):
        if self.tabs.currentWidget().history().canGoForward():
            self.tabs.currentWidget().forward()

    def reload_page(self):
        self.tabs.currentWidget().reload()

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("https://www.google.com"))

    def open_settings(self):
        # Rəng seçimi dialoqu açılır
        color = QColorDialog.getColor()
        if color.isValid():
            self.setStyleSheet(f"background-color: {color.name()};")

    def create_new_tab(self):
        self.add_new_tab(QUrl("https://www.google.com"), "Yeni Tab")

    def record_history(self, url):
        self.history.append(url.toString())

    def show_history(self):
        history_window = QMainWindow(self)
        history_window.setWindowTitle("Gözləmə Tarixçəsi")
        history_window.setGeometry(150, 150, 600, 400)

        history_widget = QWidget()
        history_layout = QVBoxLayout()
        history_widget.setLayout(history_layout)

        for url in self.history:
            button = QPushButton(url)
            button.clicked.connect(lambda checked, u=url: self.add_new_tab(QUrl(u), "Tarixçə"))
            history_layout.addWidget(button)

        history_window.setCentralWidget(history_widget)
        history_window.show()

    def update_shortcuts(self):
        # Mövcud qısayolları təmizləyin
        self.shortcut_toolbar.clear()

        for name, url in self.shortcuts.items():
            shortcut_button = QPushButton(name)
            shortcut_button.clicked.connect(lambda checked, u=url: self.add_new_tab(QUrl(u), name))
            self.shortcut_toolbar.addWidget(shortcut_button)

    def manage_shortcuts(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Qısayolları İdarə et")
        dialog.setGeometry(200, 200, 400, 300)

        layout = QFormLayout()

        name_input = QLineEdit()
        url_input = QLineEdit()
        add_button = QPushButton("Qısayol Əlavə et")

        layout.addRow(QLabel("Ad:"), name_input)
        layout.addRow(QLabel("URL:"), url_input)
        layout.addWidget(add_button)

        def add_shortcut():
            name = name_input.text().strip()
            url = url_input.text().strip()
            if name and url:
                self.shortcuts[name] = url
                self.update_shortcuts()
                dialog.close()

        add_button.clicked.connect(add_shortcut)

        dialog.setLayout(layout)
        dialog.exec_()

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        browser = Browser()
        browser.show()
        sys.exit(app.exec_())
    except ModuleNotFoundError as e:
        print("Xəta: PyQt5 quraşdırılmayıb. Zəhmət olmasa 'pip install PyQt5' istifadə edərək quraşdırın.")
