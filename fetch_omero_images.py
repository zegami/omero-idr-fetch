"""
Grab images from OMERO IDR demo based on Screen data
"""

import csv
import multiprocessing
import progressbar
import signal
import sys
import time
from argparse import ArgumentParser
from collections import OrderedDict

from omeroidr.images import Images

parser = ArgumentParser(prog='OMERO IDR screen image downloader')
parser.add_argument('-o', '--output', help='Path to the output images directory')
parser.add_argument('-d', '--data', required=False, default='idr.tab', help='Path to the data source')
parser.add_argument('-u', '--url', required=False, default='http://idr-demo.openmicroscopy.org', help='Base url for OMERO server')

pargs = parser.parse_args()

# initialize the progress bar
widgets = [progressbar.Percentage(), " ", progressbar.Bar(), " ", progressbar.ETA()]
pbar = progressbar.ProgressBar(widgets=widgets)


def init_worker():
    """
    Initialise multiprocessing pool
    """
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def download_image_callback(val):
    """
    Callback from apply_async download image method.

    :param val: Callback value
    """
    # update progress bar
    pbar.update(pbar.previous_value + 1)


def main():
    omero_images = Images(pargs.url, pargs.output)

    # open tab metadata file
    with open(pargs.data, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        # get headers
        headers = [i.strip() for i in next(csv_reader)]
        # transform into dict
        wells = list(OrderedDict(zip(headers, row)) for row in csv_reader)

    # get list of image ids from wells
    image_ids = [well['id'] for well in wells]

    print('Fetching images...')

    # using a pool of processes
    p = multiprocessing.Pool(multiprocessing.cpu_count(), init_worker)

    pbar.max_value = len(wells)
    pbar.start()
    for image_id in image_ids:
        p.apply_async(omero_images.download_image, args=(image_id,), callback=download_image_callback)
    try:
        # wait 10 seconds, this allows for the capture of the KeyboardInterrupt exception
        time.sleep(10)
    except KeyboardInterrupt:
        p.terminate()
        p.join()
        print('exiting...')
        sys.exit(0)
    finally:
        p.close()
        p.join()
        pbar.finish()

    print('Image fetch complete')

if __name__ == '__main__':
    main()
