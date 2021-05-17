from gitblob import GitBlob
from gitcommit import GitCommit
from gitrepository import GitRepository, repo_file, repo_dir
from gittag import GitTag
from gittree import GitTree
from utils_ref import ref_resolve
import hashlib
import re
import os
import zlib

def object_read(repo, sha):
    """Read object object_id from Git repository repo. Return a
GitObject whose exact type depends on the Object."""

    path = repo_file(repo, "objects", sha[0:2], sha[2:])

    with open(path, "rb") as f:
        raw = zlib.decompress(f.read())

        # Read object type
        x = raw.find(b' ')
        fmt = raw[0:x]

        # Read and validate object size
        y = raw.find(b'\x00', x)
        size = int(raw[x:y].decode("ascii"))
        if size != len(raw)-y-1:
            raise Exception("Malformed object {0}: bad length".format(sha))

        # Pick constructor
        if fmt == b'commit':
            c = GitCommit
        elif fmt == b'tree':
            c = GitTree
        elif fmt == b'tag':
            c = GitTag
        elif fmt == b'blob':
            c = GitBlob
        else:
            raise Exception("Unknown type {0} for object {1}".format(fmt.decode("ascii"), sha))

    # Call constructor and return object
    return c(repo, raw[y+1:])



def object_write(obj, actually_write=True):
    # Serialize object data
    data = obj.serialize()
    # Add header
    result = obj.fmt + b' ' + str(len(data)).encode() + b'\x00' + data
    # Compute hash
    sha = hashlib.sha1(result).hexdigest()

    if actually_write:
        # Compute pathlib
        path = repo_file(obj.repo, "objects", sha[0:2], sha[2:], mkdir=actually_write)
        with open(path, 'wb') as f:
            # Compress and write
            f.write(zlib.compress(result))
    return sha



def object_resolve(repo, name):
    """Resolve name to an object hash in repo.

This function is aware of;

- the HEAD literal
- short and long hash
- tags
- branches
- remote branches
"""
    candidates = list()
    hashRE = re.compile(r"^[0-9A-Fa-f]{4,40}$")

    # Empty string? Abort.
    if not name.strip():
        return None

    # Head is non-ambiguous
    if name == "HEAD":
        return [ ref_resolve(repo, "HEAD") ]

    if hashRE.match(name):
        if len(name) == 40:
            # this is a complete hash
            return [ name.lower() ]

        # This is a small hash
        # 4 seems to be the minimal length
        # for git to consider something a short hash.
        name = name.lower()
        prefix = name[0:2]
        path = repo_dir(repo, "objects", prefix, mkdir=False)
        if path:
            rem = name[2:]
            for f in os.listdir(path):
                if f.startswith(rem):
                    candidates.append(prefix + f)
    return candidates




def object_find(repo, name, fmt=None, follow=True):
    sha = object_resolve(repo, name)

    if not sha:
        raise Exception("No such reference {0}.".format(name))

    if len(sha) > 1:
        raise Exception("Ambiguous reference {0}: candidates are:\n - {1}".format(name, "\n - ".join(sha)))

    sha = sha[0]

    if not fmt:
        return sha

    while True:
        obj = object_read(repo, sha)

        if obj.fmt == fmt:
            return sha

        if not follow:
            return None

        # Follow tags
        if obj.fmt == b'tag':
            sha = obj.kvlm[b'object'].decode("ascii")
        elif obj.fmt == b'commit' and fmt == b'tree':
            sha = obj.kvlm[b'tree'].decode("ascii")
        else:
            return None
