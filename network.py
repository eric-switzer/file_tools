import tempfile
import urllib2

def load_shelve_over_http(url):
    r"""load a shelve specified by a url into a dictionary as output
    shleve does not accept file handles, so write using tempfile
    there is probably a more elegant way to do this
    """
    req = urllib2.urlopen(url)
    temp_file = tempfile.NamedTemporaryFile()

    chunksize = 16 * 1024
    while True:
        chunk = req.read(chunksize)
        if not chunk: break
        temp_file.write(chunk)
    temp_file.flush()

    shelvedict = shelve.open(temp_file.name, "r")
    retdict = {}
    retdict.update(shelvedict)
    shelvedict.close()
    temp_file.close()

    return retdict
