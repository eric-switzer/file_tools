import os
import cPickle

def save_pickle(pickle_data, filename):
    r"""wrap cPickle; useful for general class load/save
    note that if you load a pickle outside of the class that saved itself, you
    must fully specify the class space as if you were the class, e.g.:
    from correlate.freq_slices import * to import the freq_slices object
    This clobbers anything in the requested file.
    """
    pickle_out_root = os.path.dirname(filename)
    if not os.path.isdir(pickle_out_root):
        os.mkdir(pickle_out_root)

    pickle_handle = open(filename, 'wb')
    cPickle.dump(pickle_data, pickle_handle, -1)
    pickle_handle.close()


def load_pickle(filename):
    r"""Return `pickle_data` saved in file with name `filename`.
    """
    pickle_handle = open(filename, 'r')
    pickle_data = cPickle.load(pickle_handle)
    pickle_handle.close()
    return pickle_data
