import pyart
import numpy as np

# Plans to add more options for reading (09-19-2019)
# User may modify to include new reader


def file_to_radar_object(filename, extension):
    """ Input radar filename and use appropriate PyART functions to read file and return radar object.

    Parameters
    ----------
    filename: str
        path and filename of the radar data file
    extension: str
        file extension of radar data file
        i.e. '.nc', '.h5'
                       
    Returns
    -------
    radar: object
        radar object derived from PyART readers
    
    """
    try:
        if extension == ".nc":
            radar = pyart.io.cfradial.read_cfradial(filename, delay_field_loading=True)
        elif extension == ".h5":
            radar = pyart.aux_io.read_gamic(filename, file_field_names=True)
        elif extension == ".v0":
            radar = pyart.io.cfradial.read_cfradial(filename, delay_field_loading=True)
        
    except OSError:
        print('Unable to read in file: ',filename)
        radar = np.nan
        
    return radar
