# This Python file uses the following encoding: utf-8
import sys
from pathlib import Path

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWebEngineQuick import QtWebEngineQuick
from modules.UserManagers import UserManagers
from modules.PdfManangers import PdfManangers


if __name__ == "__main__":

    QtWebEngineQuick.initialize()
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    qml_file = Path(__file__).resolve().parent / "main.qml"

    user = UserManagers()
    context = engine.rootContext()
    context.setContextProperty("user", user)

    pdf = PdfManangers()
    context.setContextProperty("pdf", pdf)

    engine.load(qml_file)
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
