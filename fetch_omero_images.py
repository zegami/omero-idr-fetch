"""
Grab images from OMERO based on Screen data
"""

import csv
import multiprocessing
import progressbar
import signal
import sys
import time
import requests
import json
import getpass
from argparse import ArgumentParser
from collections import OrderedDict
from omeroidr.images import Images
import omeroidr.connect as connect

parser = ArgumentParser(prog='OMERO screen image downloader')
parser.add_argument('-o', '--output', help='Path to the output images directory')
parser.add_argument('-d', '--data', required=False, default='omero.tab', help='Path to the data source')
parser.add_argument('-s', '--server', required=False, default='http://idr-demo.openmicroscopy.org', help='Base url for OMERO server')
parser.add_argument('-u', '--user', required=False, help='OMERO Username')
parser.add_argument('-w', '--password', required=False, help='OMERO Password')

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
    # login
    session = connect.connect_to_omero(pargs.server, pargs.user, pargs.password)

    omero_images = Images(session, pargs.server, pargs.output)

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
        disconnect(session, pargs.server)
        print('exiting...')
        sys.exit(0)
    finally:
        p.close()
        p.join()
        pbar.finish()

    connect.disconnect(session, pargs.server)
    print('Image fetch complete')

if __name__ == '__main__':
    main()
