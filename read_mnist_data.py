import struct

import numpy as np


def get_images(labelfile, imagefile):
    with open(labelfile, 'rb') as lblfile, open(imagefile, 'rb') as imgfile:
        print('lbl magic number: {0}'.format(struct.unpack('>I', lblfile.read(4))[0]))
        print('img magic number: {0}'.format(struct.unpack('>I', imgfile.read(4))[0]))

        num_labels = struct.unpack('>I', lblfile.read(4))[0]
        num_images = struct.unpack('>I', imgfile.read(4))[0]
        num_pixels = struct.unpack('>I', imgfile.read(4))[0] * struct.unpack('>I', imgfile.read(4))[0]
        print('num_pixels: {0}'.format(num_pixels))

        lbls = np.empty([num_labels])
        imgs = np.empty([num_images, num_pixels])

        if num_labels != num_images:
            raise Exception('Number of items in files is not the same')

        for image_index in range(num_labels):
            if image_index % 1000 == 0:
                print(image_index)

            lbls[image_index] = struct.unpack('>B', lblfile.read(1))[0]

            pixel_data = np.empty([num_pixels])
            for pixel_index in range(num_pixels):
                pixel = struct.unpack('>B', imgfile.read(1))[0]
                pixel = (1 - pixel / 255)
                pixel_data[pixel_index] = pixel

            imgs[image_index] = pixel_data

    return lbls, imgs


def main():
    labels, images = get_images('train-images.idx3-ubyte', 'train-labels.idx1-ubyte')
    np.savez('test_set.npz', labels=labels, images=images)

    labels, images = get_images('t10k-images.idx3-ubyte', 't10k-labels.idx1-ubyte')
    np.savez('test_set.npz', labels=labels, images=images)


if __name__ == "__main__":
    main()
