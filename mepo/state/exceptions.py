class StateDoesNotExistError(Exception):
    """Raised when the mepo state does not exist"""
    pass

class StateAlreadyInitializedError(Exception):
    """Raised when the mepo state has already been initialized"""
    pass

class ConfigFileNotFoundError(FileNotFoundError):
    """Raised when the config file is not found"""
    pass

class SuffixNotRecognizedError(RuntimeError):
    """Raised when the config suffix is not recognized"""
    pass
