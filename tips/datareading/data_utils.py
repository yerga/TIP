
def readFile(filename, encoding=""):
    "Open a text file and return all the content as a list of lines"
    openedFile = open(filename, "r", encoding=encoding)
    linesread = openedFile.readlines()
    openedFile.close()
    return linesread