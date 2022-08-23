from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia
from compiler import Compiler, CompilerLoad
from config import OPTIONS_DICT
import sys, os, utils, config

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(750, 500)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())

        # Playlist
        self.compiler = None

        self.playlist = QtMultimedia.QMediaPlaylist()
        self.playlist.setPlaybackMode(QtMultimedia.QMediaPlaylist.Loop)
        self.musicPlayer = QtMultimedia.QMediaPlayer()
        self.musicPlayer.setPlaylist(self.playlist)
        self.musicPlayer.setVolume(50)
        self.musicPlayer.positionChanged.connect(self.position_change)
        self.musicPlayer.durationChanged.connect(lambda max: self.song_seek_slider.setMaximum(max))

        # Shortcuts
        ## Playlist Shortcuts
        self.add_shortcut = QtWidgets.QShortcut("A", MainWindow)
        self.add_shortcut.activated.connect(self.add_similar)
        self.keep_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("S"), MainWindow)
        self.keep_shortcut.activated.connect(self.keep)
        self.remove_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("D"), MainWindow)
        self.remove_shortcut.activated.connect(self.delete)

        # Seek Shortcuts
        self.one_shortcut = QtWidgets.QShortcut("1", MainWindow)
        self.one_shortcut.activated.connect(lambda: self.skip(1))
        self.two_shortcut = QtWidgets.QShortcut("2", MainWindow)
        self.two_shortcut.activated.connect(lambda: self.skip(2))
        self.three_shortcut = QtWidgets.QShortcut("3", MainWindow)
        self.three_shortcut.activated.connect(lambda: self.skip(3))
        self.four_shortcut = QtWidgets.QShortcut("4", MainWindow)
        self.four_shortcut.activated.connect(lambda: self.skip(4))
        self.five_shortcut = QtWidgets.QShortcut("5", MainWindow)
        self.five_shortcut.activated.connect(lambda: self.skip(5))
        self.six_shortcut = QtWidgets.QShortcut("6", MainWindow)
        self.six_shortcut.activated.connect(lambda: self.skip(6))
        self.seven_shortcut = QtWidgets.QShortcut("7", MainWindow)
        self.seven_shortcut.activated.connect(lambda: self.skip(7))
        self.eight_shortcut = QtWidgets.QShortcut("8", MainWindow)
        self.eight_shortcut.activated.connect(lambda: self.skip(8))
        self.nine_shortcut = QtWidgets.QShortcut("9", MainWindow)
        self.nine_shortcut.activated.connect(lambda: self.skip(9))
        self.ten_shortcut = QtWidgets.QShortcut("0", MainWindow)
        self.ten_shortcut.activated.connect(lambda: self.skip(0))

        ## Volume Shortcuts
        self.vol_up_shortcut = QtWidgets.QShortcut("right", MainWindow)
        self.vol_up_shortcut.activated.connect(lambda: self.volume(self.musicPlayer.volume() + 10))
        self.vol_down_shortcut = QtWidgets.QShortcut("left", MainWindow)
        self.vol_down_shortcut.activated.connect(lambda: self.volume(self.musicPlayer.volume() - 10))

        ## Save Shortcut
        self.save_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+S"), MainWindow)
        self.save_shortcut.activated.connect(self.save_session)

        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.album_art = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.album_art.sizePolicy().hasHeightForWidth())
        self.album_art.setSizePolicy(sizePolicy)
        self.album_art.setMinimumSize(QtCore.QSize(150, 150))
        self.album_art.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.album_art.setObjectName("album_art")
        self.album_art.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.verticalLayout_2.addWidget(self.album_art, 0, QtCore.Qt.AlignHCenter)
        self.title_label = QtWidgets.QLabel(self.centralwidget)
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setObjectName("title_label")
        self.verticalLayout_2.addWidget(self.title_label)
        self.album_label = QtWidgets.QLabel(self.centralwidget)
        self.album_label.setAlignment(QtCore.Qt.AlignCenter)
        self.album_label.setObjectName("album_label")
        self.verticalLayout_2.addWidget(self.album_label)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.add_similar_button = QtWidgets.QPushButton(self.centralwidget)
        self.add_similar_button.setObjectName("add_similar_button")
        self.horizontalLayout_4.addWidget(self.add_similar_button)
        self.keep_button = QtWidgets.QPushButton(self.centralwidget)
        self.keep_button.setObjectName("keep_button")
        self.horizontalLayout_4.addWidget(self.keep_button)
        self.remove_button = QtWidgets.QPushButton(self.centralwidget)
        self.remove_button.setObjectName("remove_button")
        self.horizontalLayout_4.addWidget(self.remove_button)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.duration_label = QtWidgets.QLabel(self.centralwidget)
        self.duration_label.setAlignment(QtCore.Qt.AlignCenter)
        self.duration_label.setObjectName("duration_label")
        self.verticalLayout_2.addWidget(self.duration_label)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.song_seek_slider = QtWidgets.QSlider(self.centralwidget)
        self.song_seek_slider.setOrientation(QtCore.Qt.Horizontal)
        self.song_seek_slider.setObjectName("song_seek_slider")
        self.song_seek_slider.setMinimum(0)
        self.song_seek_slider.setMaximum(100)
        self.song_seek_slider.sliderMoved.connect(lambda pos: self.musicPlayer.setPosition(pos))
        self.verticalLayout.addWidget(self.song_seek_slider)
        self.song_time_label = QtWidgets.QLabel(self.centralwidget)
        self.song_time_label.setAlignment(QtCore.Qt.AlignCenter)
        self.song_time_label.setObjectName("song_time_label")
        self.verticalLayout.addWidget(self.song_time_label)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.todo_list = QtWidgets.QListWidget(self.centralwidget)
        self.todo_list.setObjectName("todo_list")
        self.verticalLayout_3.addWidget(self.todo_list)
        self.todo_length_label = QtWidgets.QLabel(self.centralwidget)
        self.todo_length_label.setAlignment(QtCore.Qt.AlignCenter)
        self.todo_length_label.setObjectName("todo_length_label")
        self.verticalLayout_3.addWidget(self.todo_length_label)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.completed_list = QtWidgets.QListWidget(self.centralwidget)
        self.completed_list.setObjectName("completed_list")
        self.verticalLayout_4.addWidget(self.completed_list)
        self.completed_length_label = QtWidgets.QLabel(self.centralwidget)
        self.completed_length_label.setAlignment(QtCore.Qt.AlignCenter)
        self.completed_length_label.setObjectName("completed_length_label")
        self.verticalLayout_4.addWidget(self.completed_length_label)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 750, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuNew = QtWidgets.QMenu(self.menuFile)
        self.menuNew.setObjectName("menuNew")
        self.menuExport = QtWidgets.QMenu(self.menuFile)
        self.menuExport.setObjectName("menuExport")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionfrom_m3u8 = QtWidgets.QAction(MainWindow)
        self.actionfrom_m3u8.setObjectName("actionfrom_m3u8")
        self.actionfrom_m3u8.triggered.connect(self.import_m3u8)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionOpen.triggered.connect(self.open_session)
        self.actionas_m3u8 = QtWidgets.QAction(MainWindow)
        self.actionas_m3u8.setObjectName("actionas_m3u8")
        self.actionas_m3u8.triggered.connect(self.export)
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave.triggered.connect(self.save_session)
        self.menuNew.addAction(self.actionfrom_m3u8)
        self.menuExport.addAction(self.actionas_m3u8)
        self.menuFile.addAction(self.menuNew.menuAction())
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.menuExport.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())

        self.menuEdit = QtWidgets.QMenu(MainWindow)
        self.menuEdit.setObjectName("menuEdit")
        self.actionFilter = QtWidgets.QAction(MainWindow)
        self.actionFilter.setObjectName("menuFilter")
        self.actionFilter.triggered.connect(self.add_filter)
        self.actionRenamePlaylist = QtWidgets.QAction(MainWindow)
        self.actionRenamePlaylist.setObjectName("menuRenamePlaylist")
        self.actionRenamePlaylist.triggered.connect(self.rename_playlist)
        self.menuEdit.addAction(self.actionFilter)
        self.menuEdit.addAction(self.actionRenamePlaylist)
        self.menubar.addAction(self.menuEdit.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.album_art, self.add_similar_button)
        MainWindow.setTabOrder(self.add_similar_button, self.keep_button)
        MainWindow.setTabOrder(self.keep_button, self.remove_button)
        MainWindow.setTabOrder(self.remove_button, self.song_seek_slider)
        MainWindow.setTabOrder(self.song_seek_slider, self.completed_list)
        MainWindow.setTabOrder(self.completed_list, self.todo_list)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Autocompiler 2.0 - Now featuring more compiling!"))
        self.title_label.setText(_translate("MainWindow", "Title"))
        self.album_label.setText(_translate("MainWindow", "Album"))
        self.add_similar_button.setText(_translate("MainWindow", "Add Similar"))
        self.add_similar_button.clicked.connect(self.add_similar)
        self.keep_button.setText(_translate("MainWindow", "Keep"))
        self.keep_button.clicked.connect(self.keep)
        self.remove_button.setText(_translate("MainWindow", "Remove"))
        self.remove_button.clicked.connect(self.delete)
        self.song_time_label.setText(_translate("MainWindow", "Please load a playlist..."))
        self.duration_label.setText(_translate("MainWindow", "Length"))
        self.todo_length_label.setText(_translate("MainWindow", "Items: 0"))
        self.completed_length_label.setText(_translate("MainWindow", "Items: 0"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuNew.setTitle(_translate("MainWindow", "New..."))
        self.menuExport.setTitle(_translate("MainWindow", "Export..."))
        self.actionfrom_m3u8.setText(_translate("MainWindow", "from .m3u8"))
        self.actionOpen.setText(_translate("MainWindow", "Load session..."))
        self.actionas_m3u8.setText(_translate("MainWindow", "as .m3u8"))
        self.actionSave.setText(_translate("MainWindow", "Save..."))
        self.actionFilter.setText(_translate("MainWindow", "Add Filter..."))
        self.actionRenamePlaylist.setText(_translate("MainWindow", "Rename Playlist..."))
    
    def load_m3u8(self, location):
        if not os.path.isfile(location) or not location.endswith(".m3u8"): return
        self.compiler = Compiler(location, title = os.path.splitext(os.path.basename(location))[0])
        self.update_todo()
        self.update_completed()
        self.update()

    def update(self):
        self.update_song()
        self.update_info()

    def update_todo(self):
        if self.compiler == None or not self.compiler.hasNext():
            return
        self.todo_list.clear()
        for song in self.compiler.queue_title_cache:
            self.todo_list.addItem(song)
    
    def update_completed(self):
        if self.compiler == None or not self.compiler.hasNext():
            return
        self.completed_list.clear()
        for song in self.compiler.accepted:
            self.completed_list.addItem(utils.title(song))

    def update_song(self):
        if self.compiler == None or not self.compiler.hasNext():
            self.playlist.clear()
            return
        self.playlist.clear()
        self.playlist.addMedia(QtMultimedia.QMediaContent(QtCore.QUrl(self.compiler.next())))
        self.musicPlayer.play()
    
    def update_info(self):
        if self.compiler == None or not self.compiler.hasNext():
            self.title_label.setText("")
            self.album_label.setText("")
            self.song_time_label.setText("Load a new playlist or export this one...")
            return
        self.title_label.setText(utils.title(self.compiler.next()))
        self.album_label.setText(utils.album(self.compiler.next()))
        self.song_time_label.setText(str(len(self.compiler.queue)) + " songs in queue...")
        utils.get_album_art(self.compiler.next())
        self.album_art.setStyleSheet("border-image : url(cover.jpg);")
        self.todo_length_label.setText(str(len(self.compiler.queue)))
        self.completed_length_label.setText(str(len(self.compiler.accepted)))
        MainWindow.setWindowTitle("Currently editing - " + self.compiler.get_title())
    
    def delete(self):
        if self.compiler == None or not self.compiler.hasNext():
            return
        self.todo_list.takeItem(0)
        self.compiler.delete()
        self.update()
    
    def add_similar(self):
        if self.compiler == None or not self.compiler.hasNext():
            return
        self.completed_list.addItem(self.todo_list.takeItem(0))
        self.compiler.add_similar()
        self.update()
        self.update_todo()
    
    def keep(self):
        if self.compiler == None or not self.compiler.hasNext():
            return
        self.completed_list.addItem(self.todo_list.takeItem(0))
        self.compiler.keep()
        self.update()

    def skip(self, num):
        self.musicPlayer.setPosition((self.musicPlayer.duration() / 10) * num)
    
    def volume(self, vol):
        self.musicPlayer.setVolume(vol)
    
    def import_m3u8(self):
        filein = QtWidgets.QFileDialog.getOpenFileName(None,
        "Choose a playlist...",
        OPTIONS_DICT["import_m3u8_path"],
        "Playlist (*.m3u8)")
        if filein[0] == '' and filein[1] == '': return
        config.edit_config("import_m3u8_path", os.path.dirname(filein[0]))
        self.load_m3u8(filein[0])

    def export(self):
        if self.compiler == None:
            return
        fileout = QtWidgets.QFileDialog.getSaveFileName(None,
        "Choose a location...",
        OPTIONS_DICT["export_m3u8_path"],
        "Playlist (*.m3u8)")
        if fileout is None: return
        config.edit_config("export_m3u8_path", os.path.dirname(fileout[0]))
        self.compiler.tracks_to_m3u(fileout[0])
    
    def save_session(self):
        if self.compiler == None: return
        fileout = QtWidgets.QFileDialog.getSaveFileName(None,
        "Choose a location...",
        OPTIONS_DICT["save_session_path"],
        "Autoplaylist (*.apm)")
        if fileout[0] == '': return
        config.edit_config("save_session_path", os.path.dirname(fileout[0]))
        self.compiler.save(fileout[0])

    def open_session(self):
        filein = QtWidgets.QFileDialog.getOpenFileName(None,
        "Choose a playlist...",
        OPTIONS_DICT["open_session_path"],
        "Autoplaylist (*.apm)")
        if filein[0] == '' and filein[1] == '': return
        config.edit_config("open_session_path", os.path.dirname(filein[0]))
        self.compiler = CompilerLoad(filein[0]).load()
        self.update_todo()
        self.update_completed()
        self.update()

    def position_change(self, pos):
        dur = self.musicPlayer.duration()
        self.song_seek_slider.setValue(pos)
        self.duration_label.setText('%d:%02d'%(int(pos/60000),int((pos/1000)%60)) + '/%d:%02d'%(int(dur/60000),int((dur/1000)%60)))

    def add_filter(self):
        text, ok = QtWidgets.QInputDialog.getText(MainWindow, 'Filter', 'Enter filters seperated by a ";"')
        if ok and self.compiler != None:
            self.compiler.set_filter(text)
    
    def rename_playlist(self):
        text, ok = QtWidgets.QInputDialog.getText(MainWindow, 'Rename Playlist', 'Enter the new name of the playlist')
        if ok and self.compiler != None:
            self.compiler.title = text
        self.update_info()

if __name__ == "__main__":
   app = QtWidgets.QApplication(sys.argv)
   MainWindow = QtWidgets.QMainWindow()
   ui = Ui_MainWindow()
   ui.setupUi(MainWindow)

   MainWindow.show()
   sys.exit(app.exec_())