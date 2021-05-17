class GitTreeLeaf(object):
    def __init__(self, mode, path, sha):
        self.mode = mode
        self.path = path
        self.sha = sha


def tree_parse_one(raw, start=0):
    # Find the space terminator of the mode
    x = raw.find(b' ', start)
    assert(x - start == 5 or x - start == 6)

    # Read the mode
    mode = raw[start:x]

    # Find the NULL terminator of the path
    y = raw.find(b'\x00', x)
    # add read the path
    path = raw[x+1 : y]

    # Read the SHA and convert to an hex string
    sha = hex(
        int.from_bytes(raw[y+1 : y+21], "big")
        )[2:] # hex() adds 0x in front,
    # we don't want that.

    return y+21, GitTreeLeaf(mode, path, sha)


def tree_parse(raw):
    pos = 0
    max = len(raw)
    ret = list()
    while pos < max:
        pos, data = tree_parse_one(raw, pos)
        ret.append(data)
    return ret


def tree_serialize(obj):
    # @FIXME Add serializer!
    ret = b''
    for i in obj.items:
        ret += i.mode
        ret += b' '
        ret += i.path
        ret += b'\x00'
        sha = int(i.sha, 16)
        # @FIXME Does
        ret += sha.to_bytes(20, byteorder="big")
    return ret
