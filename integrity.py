import os
import hashlib
import time


def hashfile(filename, hasher=hashlib.md5(), blocksize=65536, max_size=1.e12):
    r"""determine the hash of a file in blocks
    if it exceeds `max_size` just report the modification time
    if the file does not exist, report '-1'
    """
    if os.access(filename, os.F_OK):
        if (os.path.getsize(filename) < max_size):
            afile = open(filename, 'r')
            buf = afile.read(blocksize)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(blocksize)

            afile.close()
            hash_digest = hasher.hexdigest()
        else:
            hash_digest = "large_file"

        modtime = time.ctime(os.path.getmtime(filename))
    else:
        hash_digest = "not_exist"
        modtime = "not_exist"

    return (hash_digest, modtime)
