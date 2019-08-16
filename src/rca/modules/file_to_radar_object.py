import pyart


def file_to_radar_object(filename, extension):
    " Input radar filename and use appropriate PyART functions to read file and return radar object.  "
    if extension == ".nc":
        radar = pyart.io.cfradial.read_cfradial(filename, delay_field_loading=True)
    elif extension == ".h5":
        radar = pyart.aux_io.read_gamic(filename, file_field_names=True)

    return radar
