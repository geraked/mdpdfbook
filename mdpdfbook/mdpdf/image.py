# from  https://stackoverflow.com/questions/8032642/how-to-obtain-image-size-using-standard-python-class-without-using-external-lib


import struct
import imghdr


def get_image_size(fname):
    """Determine the image type of fhandle and return its size.
    from draco"""
    with open(fname, "rb") as fhandle:
        head = fhandle.read(24)
        if len(head) != 24:
            return
        if imghdr.what(fname) == "png":
            check = struct.unpack(">i", head[4:8])[0]
            if check != 0x0D0A1A0A:
                return
            width, height = struct.unpack(">ii", head[16:24])
        elif imghdr.what(fname) == "gif":
            width, height = struct.unpack("<HH", head[6:10])
        elif imghdr.what(fname) == "jpeg":
            try:
                fhandle.seek(0)  # Read 0xff next
                size = 2
                ftype = 0
                while not 0xC0 <= ftype <= 0xCF:
                    fhandle.seek(size, 1)
                    byte = fhandle.read(1)
                    while ord(byte) == 0xFF:
                        byte = fhandle.read(1)
                    ftype = ord(byte)
                    size = struct.unpack(">H", fhandle.read(2))[0] - 2
                # We are at a SOFn block
                fhandle.seek(1, 1)  # Skip `precision' byte.
                height, width = struct.unpack(">HH", fhandle.read(4))
            except Exception:  # IGNORE:W0703
                return
        else:
            return
        return width, height
