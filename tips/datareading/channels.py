

def get_index(stringlist, substr):
    "Returns index of element in list when contains a substring"
    try:
        return next(i for i, e in enumerate(stringlist) if substr in e)
    except StopIteration:
        return -2 #If not found in the list, return -2 so the final value is -1 in the GUI

def extract_channel_numbers(savedchannels):
    """Extract row index for data channels depending on position on the .set file
    This works fine for new versions of labview programs, but the old ones do not follow the same order
    Also the channel names are a bit messy ("Current1" and "Current 2", for instance - no space and space)
    """
    channel_list = savedchannels.split("\n")
    # ['X (um)', 'Y (um)', 'Z (um)', 'V1 (V)', 'V2 (V)', 'Current1 (A)', 'Current 2 (A)', 'Current 3 (A)',
    # 'FeedbackType ', 'Line Number', 'Lockin Amplitude', 'Lockin  Phase', 'dt(s)', '']
    channel_strs = ["X", "Y", "Z", "Current1", "Current 2", "V1", "V2", "Line Number", "dt"]

    datachannels = []
    for i in range(len(channel_strs)):
        datachannels.append(get_index(channel_list, channel_strs[i]) + 1)

    return datachannels


#TODO: think a better way to do this - it will depend a lot on how the data is saved
def get_channel_indexes(datasettings, savedchannels):
    "Extract row indexes for data channels in .tsv file"

    #Define default indexes, we assume X, Y, Z are the first three rows
    channel_X = 1
    channel_Y = 2
    channel_Z = 3
    channel_C1 = -1
    channel_C2 = -1
    channel_V1 = -1
    channel_V2 = -1
    channel_LN = -1
    channel_DT = -1
    datachannels = [channel_X, channel_Y, channel_Z, channel_C1, channel_C2, channel_V1, channel_V2, channel_LN, channel_DT]
    if datasettings["oldlabview"]:
        # Old labview files are quite messy to detect the row index from the data file
        # Info in .set files do not usually follow the same order than in the .tsv 
        channel_C1 = datachannels[3] = 4
        channel_V1 = datachannels[5] = 5
        channel_LN = datachannels[7] = 7
    else:
        datachannels = extract_channel_numbers(savedchannels)

    #TODO: for galvanostatic might be different
    #TODO: for some cases, C1 = 4, V1 = 8, LN = 11 if not saved as 10channel and old labview?


    return datachannels
