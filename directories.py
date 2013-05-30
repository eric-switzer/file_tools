import os
import time
import sys


def mkdir_p(path) :
    """Same functionality as shell command mkdir -p."""
    try:
        os.makedirs(path)
    except OSError, exc: # Python >2.5
        if exc.errno == errno.EEXIST:
            pass
        else: raise


def mkparents(path) :
    """Given a file name, makes all the parent directories."""
    last_slash = path.rfind('/')
    if last_slash > 0 : # Protect against last_slash == -1 or 0.
        outdir = path[:last_slash]
        mkdir_p(outdir)


def abbreviate_file_path(fname) :
    """Abbrviates file paths.
    Given any file path return an abbreviated path showing only the deepest
    most directory and the file name (Useful for writing feedback that doesn't
    flood your screen.)
    """
    split_fname = fname.split('/')
    if len(split_fname) > 1 :
        fname_abbr = split_fname[-2] + '/' + split_fname[-1]
    else :
        fname_abbr = fname

    return fname_abbr


def extract_rootdir(pathname):
    r"""superceded by os.path.dirname(filename), but we still use it in
    path_properties because "./" is nice to indicate local paths.
    """
    directory = "/".join(pathname.split("/")[:-1])
    if directory == "":
        directory = "."
    directory += "/"
    return directory


def path_properties(pathname, intend_write=False, intend_read=False,
                    file_index="", prefix="", silent=False, is_file=False,
                    die_overwrite=False):
    r"""Check various properties about the path, print the result
    if `intend_write` then die if the path does not exist or is not writable
    if `intend_read` then die if the path does not exist
    `file_index` is an optional mark to put in front of the file name
    `prefix` is an optional mark to prefix the file property output
    `silent` turns off printing unless there was an intend_r/w error
    `is_file` designates a file; if it does not exist check if the path is
    writable.

    # Usage examples:
    >>> path_properties("this_does_not_exist.txt", is_file=True)
    => this_does_not_exist.txt: does not exist,
        but path: ./ exists, is writable, is not readable.
    (True, False, True, False, '...')

    >>> path_properties("/tmp/nor_does_this.txt", is_file=True)
    => /tmp/nor_does_this.txt: does not exist,
        but path: /tmp/ exists, is writable, is not readable.
    (True, False, True, False, '...')

    # here's one that you should not be able to write to
    >>> path_properties("/var/nor_does_this.txt", is_file=True)
    => /var/nor_does_this.txt: does not exist,
        but path: /var/ exists, is not writable, is not readable.
    (True, False, False, False, '...')

    # here's one that definitely exists
    >>> path_properties(__file__, is_file=True)
    => ...: exists, is writable, is readable.
    (True, True, True, False, '...')

    # test a writeable directory that exists
    >>> path_properties('/tmp/')
    => /tmp/: exists, is writable, is readable.
    (True, True, True, True, '...')
    """
    entry = "%s=> %s %s:" % (prefix, file_index, pathname)

    exists = os.access(pathname, os.F_OK)
    # save the state of the file (exist will later specify if the parent dir
    # exists, but we also care about this specific file)
    file_exists = exists
    readable = os.access(pathname, os.R_OK)
    writable = os.access(pathname, os.W_OK)
    executable = os.access(pathname, os.X_OK)
    if exists:
        modtime = time.ctime(os.path.getmtime(pathname))
    else:
        modtime = None

    # if this is a file that does not exist, check the directory
    if not exists and is_file:
        directory = extract_rootdir(pathname)

        writable = os.access(directory, os.W_OK)
        exists = os.access(directory, os.F_OK)
        if exists:
            modtime = time.ctime(os.path.getmtime(directory))

        readable = False
        entry += " does not exist, but path: %s" % directory

    if exists:
        entry += " exists,"

        if writable:
            entry += " is writable,"
        else:
            entry += " is not writable,"

        if readable:
            entry += " is readable."
        else:
            entry += " is not readable."
    else:
        entry += " does not exist"

    if not silent:
        print entry

    if intend_read and not readable:
        print "ERROR: no file to read: %s" % pathname
        sys.exit()

    if intend_write and not writable:
        print "ERROR: can not write this file"
        sys.exit()

    if intend_write and file_exists:
        if die_overwrite:
            print "OVERWRITE ERROR: " + entry
            sys.exit()
        else:
            print "WARNING: you will overwrite " + entry

    return (exists, readable, writable, executable, modtime)
