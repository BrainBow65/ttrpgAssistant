# Copyright (C) 2024 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

"""
This example shows how to customize Qt Quick Controls by implementing a simple filesystem explorer.
"""

# Compile both resource files app.qrc and icons.qrc and include them here if you wish
# to load them from the resource system. Currently, all resources are loaded locally
# import FileSystemModule.rc_icons
# import FileSystemModule.rc_app

from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QCommandLineParser, qVersion

import sys

# Copyright (C) 2024 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

from PySide6.QtWidgets import QFileSystemModel
from PySide6.QtQuick import QQuickTextDocument
from PySide6.QtQml import QmlElement, QmlSingleton
from PySide6.QtCore import (Qt, QDir, QAbstractListModel, Slot, QFile, QTextStream,
                            QMimeDatabase, QFileInfo, QStandardPaths, QModelIndex,
                            Signal, Property)

@QmlElement
@QmlSingleton
class FileSystemModel(QFileSystemModel):

    rootIndexChanged = Signal()

    def getDefaultRootDir():
        return QStandardPaths.writableLocation(QStandardPaths.StandardLocation.HomeLocation)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.mRootIndex = QModelIndex()
        self.mDb = QMimeDatabase()
        self.setFilter(QDir.Filter.AllEntries | QDir.Filter.Hidden | QDir.Filter.NoDotAndDotDot)
        self.setInitialDirectory()

    # check for the correct mime type and then read the file.
    # returns the text file's content or an error message on failure
    @Slot(str, result=str)
    def readFile(self, path):
        if path == "":
            return ""

        file = QFile(path)

        mime = self.mDb.mimeTypeForFile(QFileInfo(file))
        if ('text' in mime.comment().lower()
                or any('text' in s.lower() for s in mime.parentMimeTypes())):
            if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
                stream = QTextStream(file).readAll()
                file.close()
                return stream
            else:
                return self.tr("Error opening the file!")
        return self.tr("File type not supported!")

    @Slot(QQuickTextDocument, int, result=int)
    def currentLineNumber(self, textDocument, cursorPosition):
        td = textDocument.textDocument()
        tb = td.findBlock(cursorPosition)
        return tb.blockNumber()

    def setInitialDirectory(self, path=getDefaultRootDir()):
        dir = QDir(path)
        if dir.makeAbsolute():
            self.setRootPath(dir.path())
        else:
            self.setRootPath(self.getDefaultRootDir())
        self.setRootIndex(self.index(dir.path()))

    # we only need one column in this example
    def columnCount(self, parent):
        return 1

    @Property(QModelIndex, notify=rootIndexChanged)
    def rootIndex(self):
        return self.mRootIndex

    def setRootIndex(self, index):
        if (index == self.mRootIndex):
            return
        self.mRootIndex = index
        self.rootIndexChanged.emit()


@QmlElement
class LineNumberModel(QAbstractListModel):

    lineCountChanged = Signal()

    def __init__(self, parent=None):
        self.mLineCount = 0
        super().__init__(parent=parent)

    @Property(int, notify=lineCountChanged)
    def lineCount(self):
        return self.mLineCount

    @lineCount.setter
    def lineCount(self, n):
        if n < 0:
            print("lineCount must be greater then zero")
            return
        if self.mLineCount == n:
            return

        if self.mLineCount < n:
            self.beginInsertRows(QModelIndex(), self.mLineCount, n - 1)
            self.mLineCount = n
            self.endInsertRows()
        else:
            self.beginRemoveRows(QModelIndex(), n, self.mLineCount - 1)
            self.mLineCount = n
            self.endRemoveRows()

    def rowCount(self, parent):
        return self.mLineCount

    def data(self, index, role):
        if not self.checkIndex(index) or role != Qt.ItemDataRole.DisplayRole:
            return
        return index.row()

if __name__ == '__main__':
    app = QGuiApplication(sys.argv)
    app.setOrganizationName("QtProject")
    app.setApplicationName("File System Explorer")
    app.setApplicationVersion(qVersion())
    app.setWindowIcon(QIcon("FileSystemModule/icons/app_icon.svg"))

    parser = QCommandLineParser()
    parser.setApplicationDescription("Qt Filesystemexplorer Example")
    parser.addHelpOption()
    parser.addVersionOption()
    parser.addPositionalArgument("", "Initial directory", "[path]")
    parser.process(app)
    args = parser.positionalArguments()

    engine = QQmlApplicationEngine()
    # Include the path of this file to search for the 'qmldir' module
    engine.addImportPath(sys.path[0])

    engine.loadFromModule("FileSystemModule", "Main")

    if not engine.rootObjects():
        sys.exit(-1)

    if (len(args) == 1):
        fsm = engine.singletonInstance("FileSystemModule", "FileSystemModel")
        fsm.setInitialDirectory(args[0])

    sys.exit(app.exec())