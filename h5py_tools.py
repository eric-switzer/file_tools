import numpy as np
import h5py

def _traverse_data_dict(data_dict, h5pyobj, path=()):
    for data_key in data_dict:
        current_path = path+(data_key,)
        if isinstance(data_dict[data_key], np.ndarray):
            #print "npytree -> hdf5", current_path, data_dict[data_key].shape
            h5pyobj[data_key] = data_dict[data_key]
        elif not isinstance(data_dict[data_key], dict):
            pass
        else:
            sub_h5pyobj = h5pyobj.create_group(data_key)
            _traverse_data_dict(data_dict[data_key],
                                             sub_h5pyobj, current_path)


def _print_data_dict(data_dict, depth=""):
    for data_key in data_dict:
        current_depth = depth + " "
        try:
            data_here = data_dict[data_key].value
            if isinstance(data_here, np.ndarray):
                datashape = repr(data_here.shape)
                print "%s->%s %s" % (current_depth, data_key, datashape)
            else:
                print "leaf %s has non numpy data" % data_key
        except AttributeError:
            if isinstance(data_key, (str, unicode)):
                print "%s-%s:" % (current_depth, data_key)
                _print_data_dict(data_dict[data_key], current_depth)


def convert_numpytree_hdf5(data_dict, filename):
    r"""Convert a numpy tree of numpy objects to and hd5 file
    Non-numpy data are not recorded!

    >>> tdict = {}
    >>> tdict['dir_a'] = {}
    >>> tdict['data_a'] = np.zeros((3,3))
    >>> tdict['dir_b'] = {}
    >>> tdict['dir_a']['dir_c'] = {}
    >>> tdict['dir_a']['data_b'] = np.zeros((4,4))
    >>> tdict['dir_a']['dir_c']['data_c'] = np.zeros((5,5))
    >>> tdict['dir_b']['cats'] = "this"
    >>> tdict['dir_b']['dogs'] = [1,2,3,4]
    >>> convert_numpytree_hdf5(tdict, "test.hd5")
    writing hd5file test.hd5 from dict tree
     ->data_a (3, 3)
     -dir_a:
      ->data_b (4, 4)
      -dir_c:
       ->data_c (5, 5)
     -dir_b:
    """
    outfile = h5py.File(filename, "w")
    print "writing hd5file %s from dict tree" % filename
    _traverse_data_dict(data_dict, outfile)
    _print_data_dict(outfile)
    outfile.close()


