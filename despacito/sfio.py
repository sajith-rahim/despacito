import numpy as np
import soundfile as sf


def read_file(file_name):
    if len(file_name.split('.')) == 2:
        fname, ext = file_name.split('.')
    else:
        raise ValueError('Invalid file name/extension!')

    data, sr = sf.read(file_name)

    #### remove this
    #data = data[1:1000000,:]
    ###

    ch = data.shape[1] if data.shape[1] else 1

    if ch == 1:  # is_mono
        data = data.reshape(-1, 1)

    length = len(data)

    # convert to dB
    data_in_dB = convert_to_decibel(data)

    return {
        'file_name': fname,
        'ext': ext,
        'data': data,
        'sample_rate': sr,
        'n_channels': ch,
        'length': length,
        'data_in_db': data_in_dB,
        'is_mono': ch == 1
    }


def convert_to_decibel(np_array, replace_neg_spikes_with_const=False):
    if not replace_neg_spikes_with_const:
        np_array[np.where(np_array == 0)] = 0.00001  # avoid log(0)

    ref = 1
    if np_array.any() != 0:  # avoid log(0)
        return 20 * np.log10(abs(np_array) / ref)
    else:
        return -100


def write_file(file_name, data, sr, subtype='PCM_24', ext='.wav'):
    file = file_name +ext
    print(f"Writing {file}...")
    try:
        sf.write(file, data, sr, subtype)
        print(f"Writing success!")
    except IOError as e:
        print(f"Failed to write {file} !")


