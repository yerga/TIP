import traceback
from PyQt5.QtWidgets import QFileDialog, QErrorMessage
from tips.logging_utils import get_logger
wecalLogger = get_logger("tips")

def showErrorDialog(error):
    error_dialog = QErrorMessage()
    error_dialog.showMessage("Error: " + str(error))
    error_dialog.exec_()

def getFileName(parent, path="", title="Select .tsv file", filefilter="TSV files (*.tsv)"):
    "Run a FileDialog to select a File, return the full filename"
    try:
        filename, ffilter = QFileDialog.getOpenFileName(parent, title, path, filefilter, "")
        wecalLogger.debug("Selected file: " + filename)
        return filename
    except Exception:
        error = traceback.format_exc()
        wecalLogger.error(error)
        showErrorDialog(error)
