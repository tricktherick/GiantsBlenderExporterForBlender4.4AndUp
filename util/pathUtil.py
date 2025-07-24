import os


class Error(Exception):
    """Base class for exceptions in this module."""
    
    pass

class InputError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


def resolvePath(fullPath, referenceDirectory = None, targetDirectory = None):
    """
    
    """
    # print("fullPath: {}, refDir: {}, tarDir: {}".format(fullPath,referenceDirectory,targetDirectory))
    if referenceDirectory:
        absPath = os.path.normpath(os.path.join(referenceDirectory, fullPath))
        if os.path.isfile(absPath):
            fullPath = fullPath.replace("/", os.sep)
            fullPath = fullPath.replace("\\",os.sep)
            fileName = fullPath.split(os.sep)[-1]
            filePath = fullPath.rsplit(os.sep,1)[0]
            return _resolveFilePath(fileName, filePath, referenceDirectory, targetDirectory)
            
        elif os.path.isdir(absPath):
            fullPath = fullPath.replace("/", os.sep)
            fullPath = fullPath.replace("\\",os.sep)
            filePath = fullPath
            return _resolvePath(filePath, referenceDirectory, targetDirectory)
        else:
            raise InputError("Invalid Function Parameters: {}: {}".format(resolvePath.__code__.co_varnames[0],absPath),"No Valid File: {}".format(absPath))
    else:
        if os.path.isfile(fullPath):
            fullPath = fullPath.replace("/", os.sep)
            fullPath = fullPath.replace("\\",os.sep)
            fileName = fullPath.split(os.sep)[-1]
            filePath = fullPath.rsplit(os.sep,1)[0]
            return _resolveFilePath(fileName, filePath, referenceDirectory, targetDirectory)
            
        elif os.path.isdir(fullPath):
            fullPath = fullPath.replace("/", os.sep)
            fullPath = fullPath.replace("\\",os.sep)
            filePath = fullPath
            return _resolvePath(filePath, referenceDirectory, targetDirectory)
        else:
            raise InputError("Invalid Function Parameters: {}: {}".format(resolvePath.__code__.co_varnames[0],fullPath),"No Valid File: {}".format(fullPath))
    
def _resolvePath(filePath, referenceDirectory = None, targetDirectory = None):
    """
    This function manipulates paths
    
    :param filePath: path of the file directory (relative or absolute) without filename
    :param referenceDirectory: the directory the file currently relative to, if None, filePath is assumed to be absolute, if given filePath is assumed to be relative
    :param targetDirectory: the directory the file is supposed to be relative to
    
    :raises InputError: if paths are given don't exist
    :raises ValueError: if attempted to create relative path between different volumes
    """
    
    if referenceDirectory == None:
        absPath = os.path.abspath(filePath)
        if os.path.isabs(absPath):
            if os.path.isdir(absPath):
                #path and file are good and absolute
                #process
                fullAbsPath = absPath
            else:
                #non valid path
                raise InputError("Invalid Function Parameters: {}: {}".format(_resolvePath.__code__.co_varnames[0],filePath),"No Valid Path: {}".format(absPath))
        else:
            #weird behavior
            raise InputError("Invalid Function Parameters: {}: {}".format(_resolvePath.__code__.co_varnames[0],filePath),"Path is not Absolute: {}".format(absPath))
    else:   #relative Path
        if os.path.isdir(referenceDirectory):
            # absPath = os.path.abspath(referenceDirectory + os.sep + filePath)
            absPath = os.path.normpath(os.path.join(referenceDirectory, filePath))
            if os.path.isdir(absPath):
                #process
                fullAbsPath = absPath
            else:
                #non valid path
                raise InputError("Invalid Function Parameters: {}: {}".format(_resolvePath.__code__.co_varnames[0],filePath),"No Valid Path: {}".format(absPath))
        else:
            raise InputError("Invalid Function Parameters: {}: {}".format(_resolvePath.__code__.co_varnames[1],referenceDirectory),"No Valid Path: {}".format(referenceDirectory))          
            #problem, no abspath and no reference for relpath
    
        
    if targetDirectory == None: #return absolute Path
        resolvedPath = fullAbsPath
        #adjust seperator
        
    else:   #return relative path
        targetDirectory = os.path.abspath(targetDirectory)
        if os.path.isdir(targetDirectory):
            try:
                resolvedPath = os.path.relpath(fullAbsPath, targetDirectory)
            except ValueError as e:
                # different volumes
                # print(e)
                # print("Ignore target directory and return absolute path")
                resolvedPath = fullAbsPath
        else:
            #non valid path
            raise InputError("Invalid Function Parameters: {}: {}".format(_resolvePath.__code__.co_varnames[2],filePath),"No Valid Path: {}".format(targetDirectory))      
     
    resolvedPath = resolvedPath.replace("/", os.sep)
    resolvedPath = resolvedPath.replace("\\",os.sep)
    return resolvedPath            


def _resolveFilePath(fileName, filePath, referenceDirectory = None, targetDirectory = None):
    """ 
    This function manipulates paths 
    
    :param fileName: name of the file
    :param filePath: path of the file directory (relative or absolute) without filename
    :param referenceDirectory: the directory the file currently relative to, if None, filePath is assumed to be absolute, if given filePath is assumed to be relative
    :param targetDirectory: the directory the file is supposed to be relative to
    
    :raises InputError: if paths are given don't exist
    :raises ValueError: if attempted to create relative path between different volumes
    """
    
    if referenceDirectory == None:  #absolute Path
        absPath = os.path.abspath(filePath)
        if os.path.isabs(absPath):
            if os.path.isdir(absPath):
                if os.path.isfile(absPath + os.sep + fileName):
                    #path and file are good and absolute
                    #process
                    fullAbsPath = absPath + os.sep + fileName
                    
                else:
                    #non valid file
                    raise InputError("Invalid Function Parameters: {}: {}, {}: {}".format(_resolveFilePath.__code__.co_varnames[0],fileName,_resolveFilePath.__code__.co_varnames[1],filePath),"No Valid File: {}".format(absPath + os.sep + fileName))
            else:
                #non valid path
                raise InputError("Invalid Function Parameters: {}: {}".format(_resolveFilePath.__code__.co_varnames[1],filePath),"No Valid Path: {}".format(absPath))
        else:
            #weird behavior
            raise InputError("Invalid Function Parameters: {}: {}".format(_resolveFilePath.__code__.co_varnames[1],filePath),"Path is not Absolute: {}".format(absPath))
            
    else:   #relative Path
        if os.path.isdir(referenceDirectory):
            absPath = os.path.normpath(os.path.join(referenceDirectory, filePath))
            # absPath = os.path.abspath(referenceDirectory + os.sep + filePath)
            if os.path.isdir(absPath):
                if os.path.isfile(absPath + os.sep + fileName):
                    #path and file are good and absolute
                    #process
                    fullAbsPath = absPath + os.sep + fileName
                else:
                    #non valid file
                    raise InputError("Invalid Function Parameters: {}: {}, {}: {}".format(_resolveFilePath.__code__.co_varnames[0],fileName,_resolveFilePath.__code__.co_varnames[1],filePath),"No Valid File: {}".format(absPath + os.sep + fileName))
            else:
                #non valid path
                raise InputError("Invalid Function Parameters: {}: {}".format(_resolveFilePath.__code__.co_varnames[1],filePath),"No Valid Path: {}".format(absPath))
        else:
            raise InputError("Invalid Function Parameters: {}: {}".format(_resolveFilePath.__code__.co_varnames[2],referenceDirectory),"No Valid Path: {}".format(referenceDirectory))          
            #problem, no abspath and no reference for relpath
    
        
    if targetDirectory == None: #return absolute Path
        resolvedPath = fullAbsPath
        #adjust seperator
        
    else:   #return relative path
        targetDirectory = os.path.abspath(targetDirectory)
        if os.path.isdir(targetDirectory):
            try:
                resolvedPath = os.path.relpath(fullAbsPath, targetDirectory)
            except ValueError as e:
                # different volumes
                # print(e)
                # print("Ignore target directory and return absolute path")
                resolvedPath = fullAbsPath
        else:
            #non valid path
            raise InputError("Invalid Function Parameters: {}: {}".format(_resolveFilePath.__code__.co_varnames[3],filePath),"No Valid Path: {}".format(targetDirectory))      
     
    resolvedPath = resolvedPath.replace("/", os.sep)
    resolvedPath = resolvedPath.replace("\\",os.sep)
    return resolvedPath
        
        
if __name__ == "__main__":
    print("pathUtil")

    try:
        print("returned: {}".format(resolvePath("../shaders/vehicleShader.xml",None,None)))
    except Exception as e:
        print(e)
    
    