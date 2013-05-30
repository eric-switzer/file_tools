import os

def print_multicolumn(*args, **kwargs):
    """given a series of arrays of the same size as arguments, write these as
    columns to a file (kwarg "outfile"), each with format string (kwarg format)
    """
    outfile = "multicolumns.dat"
    format = "%10.15g"

    if "outfile" in kwargs:
        outfile = kwargs["outfile"]

    if "format" in kwargs:
        format = kwargs["format"]

    # if there is a root directory that does not yet exist
    rootdir = "/".join(outfile.split("/")[0:-1])
    if len(rootdir) > 0 and rootdir != ".":
        if not os.path.isdir(rootdir):
            print "print_multicolumn: making dir " + rootdir
            os.mkdir(rootdir)

    numarg = len(args)
    fmt_string = (format + " ") * numarg + "\n"
    print "writing %d columns to file %s" % (numarg, outfile)

    outfd = open(outfile, "w")
    for column_data in zip(*args):
        outfd.write(fmt_string % column_data)

    outfd.close()


