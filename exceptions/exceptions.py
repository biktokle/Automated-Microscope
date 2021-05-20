

class FileNotFoundException(Exception):

    def __init__(self, no_such_dir):
        super().__init__(f'Image directory does not exist: {no_such_dir}')


class DirectoryNotSetUpException(Exception):

    def __init__(self, message):
        super().__init__(f'Image directory was not set up: {message}')


class AmbiguousFilesException(Exception):

    def __init__(self):
        super().__init__('More than one image in directory, ambiguous')
