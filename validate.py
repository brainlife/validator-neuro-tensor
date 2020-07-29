#!/usr/bin/python3 -u


from PIL import Image


import binascii
import json
import nibabel as nib
import numpy as np
import os


def normalize(img):
    img -= np.min(img)
    img_max = np.max(img)
    return img / img_max * 500


def process_file(ftype, in_dict, out_dict, verbosity='errors'):
    tag = ftype.lower()
    fname = in_dict.get(tag)
    if fname is not None:
        validate_img(fname, ftype, out_dict, verbosity=verbosity)
        symlink_fname = os.path.join('output', '{}.nii.gz'.format(tag))
        if os.path.lexists(symlink_fname):
            os.remove(symlink_fname)
        os.symlink("../" + fname, symlink_fname)
    else:
        msg = "couldn't be found in config.json."
        out_dict[verbosity].append('"{}" {}'.format(tag, msg))


def validate_img(fname, ftype, dictionary, verbosity='errors'):
    basename = os.path.basename(fname)
    # Make sure nifti starts with gzip marker
    msg = "file doesn't look like a gzip-ed nifti."
    with open(fname, 'rb') as test_f:
        if binascii.hexlify(test_f.read(2)) != b'1f8b':
            dictionary[verbosity].append('"{}" {}'.format(basename, msg))
            return

    try:
        data = nib.load(fname)
        header = data.header
        img = data.get_fdata()

        dims = header['dim']

        # Check dimensions
        if dims[0] != 3:
            dictionary[verbosity].append(
                '"{}" input should be 3D but it has '
                '{} dimensions.'.format(basename, dims[0]))
            return

        slice_x_pos = dims[1] // 2
        slice_y_pos = dims[2] // 2
        slice_z_pos = dims[3] // 2

        slice_x = img[slice_x_pos, :, :]
        slice_y = img[:, slice_y_pos, :]
        slice_z = img[:, :, slice_z_pos]

        slice_x = normalize(slice_x).T
        slice_y = normalize(slice_y).T
        slice_z = normalize(slice_z).T

        lowtype = ftype.lower()
        img_x = Image.fromarray(np.flipud(slice_x)).convert('L')
        img_x.save(os.path.join('secondary', '{}_x.png'.format(lowtype)))
        img_y = Image.fromarray(np.flipud(slice_y)).convert('L')
        img_y.save(os.path.join('secondary', '{}_y.png'.format(lowtype)))
        img_z = Image.fromarray(np.flipud(slice_z)).convert('L')
        img_z.save(os.path.join('secondary', '{}_z.png'.format(lowtype)))
    except Exception as e:
        print(e)
        dictionary[verbosity].append('Nibabel failed on "{}" with error code: '
                                     '{}'.format(basename, e))


if __name__ == '__main__':
    # Initialize results dict
    results = {'errors': [], 'warnings': []}

    # Create Brainlife's output dirs if don't exist
    if not os.path.exists('output'):
        os.mkdir('output')
    if not os.path.exists('secondary'):
        os.mkdir('secondary')

    # Read Brainlife's config.json
    with open('config.json', encoding='utf-8') as config_json:
        config = json.load(config_json)

    # Validate mandatory files
    process_file('FA', config, results)
    process_file('MD', config, results)
    process_file('RD', config, results)
    process_file('AD', config, results)

    # Check optional files
    process_file('CL', config, results, verbosity='warnings')
    process_file('CP', config, results, verbosity='warnings')
    process_file('CL', config, results, verbosity='warnings')
    process_file('Tensors', config, results, verbosity='warnings')
    process_file('Kurtosis', config, results, verbosity='warnings')

    with open('product.json', 'w') as fp:
        json.dump(results, fp)
