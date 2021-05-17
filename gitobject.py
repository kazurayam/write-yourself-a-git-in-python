import hashlib
import re
import zlib

from utils_ref import ref_resolve

class GitObject(object):
    repo = None

    def __init__(self, repo, data=None):
        self.repo = repo
        if data != None:
            self.deserialize(data)

    def deserialize(self):
        """This function must be implemented by subclasses.
It must read the object's contents from self.data, a byte string, and do whatever it takes to convert it into a meaningful representation.
What exactly that means depends on each subclass."""
        raise Exception("Unimplemented!")

    def serialize(self, data):
        raise Exception("Unimplemented")
