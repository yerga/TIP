from tips.datareading.data_utils import readFile

def initiate_settings_dict():
    "Define default settings in case they are missing from the file"
    datasettings = {"labviewprogram": "", "cycles": 1, "xwidth": 0, "ywidth": 0, "hopdistance": 0, "scanrate": 0, "oldlabview": False, 
        "sampletime": 0, "samplespdp": 0, "islsv": False}
    return datasettings

def extract_param_and_value(item):
    """Extract name of parameter and its value from .set file
    An example of the input can be: 'Y Width : 24.00000000000000'
    It splits the string from the : symbol and returns name and value
    """
    param, value = "", ""
    item = item.split(" : ")
    if len(item) > 1:
        param, value = item
    return param, value

def get_exp_settings(filename):
    "Extract useful information from the .set file"
    setfilename = filename.replace("tsv", "set") # This assumes the .tsv and .set files are in the same folder
    try:
        setlines = readFile(setfilename, encoding="utf8")
    except UnicodeDecodeError:
        setlines = readFile(setfilename, encoding="latin1")

    # Remove all the \n characters from each line
    for i in range(len(setlines)):
        setlines[i] = setlines[i].replace("\n", "")
    
    #Initiate settins dictionary with default values
    datasettings = initiate_settings_dict()

    #print(setlines)
    # Get name of the labVIEW program used to collect the data
    datasettings["labvprogram"] = setlines[0]

    # Locate line indexes where different sections from the .set file start
    lsindex = setlines.index("Local Settings")
    gsindex = setlines.index("Global Settings")
    dfindex = setlines.index("Save Data Format: ")

    # Slice full settings file by sections 
    localsettings = setlines[lsindex+2:gsindex-1]
    globalsettings = setlines[gsindex+2:dfindex-1]
    savedchannels = setlines[dfindex+2:]
    datasettings["nchannels"] = len(savedchannels)

    # Extract useful parameters and its values from the .set file
    #TODO: think a better way to extract these values
    for item in localsettings:
        param, value = extract_param_and_value(item)
        #print(param, value)
        if "X Width" in param:
            datasettings["xwidth"] = "{:.1f}".format(float(value))
        elif "Y Width" in param:
            datasettings["ywidth"] = "{:.1f}".format(float(value))
        elif "HoppingDistance" in param or "Hopping Distance" in param:
            datasettings["hopdistance"] = "{:.2f}".format(float(value))
        elif "CV Rate" in param or "V Vel" in param:
            datasettings["scanrate"] = "{:.3f}".format(float(value))
        elif "No. Cycles" in param or "Number of Cycles" in param:
            datasettings["ncycles"] = "{:d}".format(int(float(value)))
        elif "V1" in param:
            v1 = "{:.3f}".format(float(value))
        elif "V2" in param:
            v2 = "{:.3f}".format(float(value))

    for item in globalsettings:
        param, value = extract_param_and_value(item)
        if "Sample Time (us)" in param:
            datasettings["sampletime"] = "{:d}".format(int(float(value)))
        elif "Samples per Data Point" in param:
            datasettings["samplespdp"] = "{:d}".format(int(float(value)))
        
    # Detect if the labview program is from an old or newer version
    # Looks like "Use 10 Channel" option is only available in old versions
    #TODO: check if this is consistent for different labview programs
    datasettings["oldlabview"] = bool([i for i, e in enumerate(globalsettings) if "Use 10 Channel" in e])

    # Making the text nicer to show it in the GUI
    for i in range(len(localsettings)):
        localsettings[i] = "<b>"+localsettings[i].replace(":", ":</b>").replace("000000000000", "")
        if ":" not in localsettings[i]:
            localsettings[i] = localsettings[i]+"</b>"

    for i in range(len(globalsettings)):
        globalsettings[i] = "<b>"+globalsettings[i].replace(":", ":</b>").replace("000000000000", "")
        if ":" not in globalsettings[i]:
            globalsettings[i] = globalsettings[i]+"</b>"

    localsettings = '<br/>'.join(localsettings)
    globalsettings = '<br/>'.join(globalsettings)
    savedchannels = '\n'.join(savedchannels)
    allsettings = [localsettings, globalsettings, savedchannels] #This is used to show the full text of the .set file into the GUI

    return allsettings, datasettings
