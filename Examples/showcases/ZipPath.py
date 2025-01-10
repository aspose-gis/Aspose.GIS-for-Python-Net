import io
import tempfile
from pathlib import Path
from zipfile import ZipFile

from aspose.gis import AbstractPath


# Allow work with files from ZIP (read only).
class ZipPath:
    def __init__(self, entry_name, stream):
        self._index = -1
        self._zip = ZipFile(stream, 'r')
        self._abstractPath = None
        self._entry_name = entry_name
        self._streams = []
        self._inner_paths = []
        self._temp_dir = tempfile.TemporaryDirectory()
        self._temp_path = Path(self._temp_dir.name)

    def __enter__(self):

        #with tempfile.TemporaryDirectory() as tempdir:

        self._zip.extractall(self._temp_path)
        self._abstractPath = AbstractPath.from_local_path(str(self._temp_path))

        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        #Exception handling here
        self._temp_dir.cleanup()
        self._zip.close()

    def is_file(self):
        # In our terms, if there is an entry on a provided zip, we return true.
        return self._index > -1

    def delete(self):
        raise NotImplementedError("Delete operation is not supported.")

    def as_abstract_path(self):
        return self._abstractPath

    def open(self, access):
        if access == 'r':
            # we need a clone because a compressed stream does not support 'seek', 'length', and so on.
            stream = io.BytesIO()
            with self._zip.open(self._zip.namelist()[self._index]) as opened:
                stream.write(opened.read())
            stream.seek(0)
            self._streams.append(stream)
            return AbstractPath.from_stream(stream)
        elif access in ['w', 'rw']:
            raise NotImplementedError("Write operation is not supported.")
        else:
            raise ValueError("Invalid access mode.")

    def list_directory(self):
        return [ZipPath(i, self._zip) for i in range(len(self._zip.namelist()))]

    def dispose(self):
        for stream in self._streams:
            stream.close()

        for inner in self._inner_paths:
            inner.dispose()

        self._zip.close()

    def with_location(self, new_location):
        for i, entry in enumerate(self._zip.namelist()):
            if entry.endswith(new_location):
                path = ZipPath(i, self._zip)
                self._inner_paths.append(path)
                return path

        unknown = ZipPath(-1, self._zip)
        self._inner_paths.append(unknown)
        return unknown

    @property
    def location(self):
        return self._zip.namelist()[self._index]

    @property
    def separator(self):
        return '/'
