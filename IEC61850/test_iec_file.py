
import ctypes
try:
    import lib61850
except:
    import lib61850_linux as lib61850
from libiec61850client import iec61850client


def _getFileHandler(parameter, buffer, bytesRead):
    filename = ctypes.cast(parameter, ctypes.c_char_p).value.decode(
        "utf-8")  # convert parameter back to python string
    print("received %i bytes for file: %s" % (bytesRead, filename))
    if bytesRead > 0:
        with open(filename, "ab") as fp:
            bytesbuffer = ctypes.string_at(buffer, bytesRead)
            fp.write(bytesbuffer)  # append bytes to file
    return True


def ClientFile61850_dir():
    for i in range(0, max_client):
        if error[i]['error'].value == lib61850.IED_ERROR_OK:
            error_file = lib61850.IedClientError()
            rootDirectory = lib61850.IedConnection_getFileDirectory(
                con[i]['con'], error_file, "/")
            if error_file.value != lib61850.IED_ERROR_OK:
                print("Error retrieving file directory")
                exit(1)

            directoryEntry = lib61850.LinkedList_getNext(rootDirectory)

            while directoryEntry:

                entry = ctypes.cast(lib61850.LinkedList_getData(
                    directoryEntry), lib61850.FileDirectoryEntry)

                file_name = lib61850.FileDirectoryEntry_getFileName(
                    entry).decode("UTF-8")
                file_size = lib61850.FileDirectoryEntry_getFileSize(entry)
                file_modified = lib61850.FileDirectoryEntry_getLastModified(
                    entry)
                print("name: %s size: %d modified: %s" %
                      (file_name, file_size, file_modified))

                directoryEntry = lib61850.LinkedList_getNext(directoryEntry)
            lib61850.LinkedList_destroy(directoryEntry)
        else:
            print("connection issue")


def ClientFile61850_get(file_name):
    handler = lib61850.IedClientGetFileHandler(_getFileHandler)
    localfilename = file_name.replace('\\', '')
    open(localfilename, "w").close()  # create an empty file
    error_getfile = lib61850.IedClientError()
    file_name_array = bytes(localfilename.encode('utf-8'))
    print(file_name_array)
    for i in range(max_client):
        lib61850.IedConnection_getFile(
            con[i]['con'], error_getfile, file_name, handler, ctypes.c_char_p(file_name_array))
        if error_getfile.value != lib61850.IED_ERROR_OK:
            print("Failed to get file!")
            

