"""
Grab screen data from OMERO based on Screen ID
"""

import csv
import multiprocessing
import progressbar
import signal
import sys
import time
import requests
import json
from argparse import ArgumentParser
import omeroidr.connect as connect
from omeroidr.data import Data

parser = ArgumentParser(prog='OMERO screen data downloader')
parser.add_argument('-i', '--id', help='Id of the screen')
parser.add_argument('-o', '--output', required=False, default='omero.tab', help='Path to the tab separated output file')
parser.add_argument('-s', '--server', required=False, default='http://idr-demo.openmicroscopy.org', help='Base url for OMERO server')
parser.add_argument('-u', '--user', required=False, help='OMERO Username')
parser.add_argument('-w', '--password', required=False, help='OMERO Password')

pargs = parser.parse_args()

# list of well metadata
wells_data = []

# initialize the progress bar
widgets = [progressbar.Percentage(), " ", progressbar.Bar(), " ", progressbar.ETA()]
pbar = progressbar.ProgressBar(widgets=widgets)


def init_worker():
    """
    Initialise multiprocessing pool
    """
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def well_details_callback(well):
    """
    Callback from apply_async. Used to update progress bar

    :param well: Well metadata object
    """
    pbar.update(pbar.previous_value + 1)
    # append well the wells data list
    wells_data.append(well)


def main():
    # login
    session = connect.connect_to_omero(pargs.server, pargs.user, pargs.password)

    # init data    
    omero_data = Data(session, pargs.server)

    # get wells for screen
    print('loading plates...')
    wells = omero_data.get_wells(pargs.id)

    print('Retrieving annotations...')
    # get all annotations

    # using a pool of processes
    p = multiprocessing.Pool(multiprocessing.cpu_count(), init_worker)

    pbar.max_value = len(wells)
    pbar.start()
    for well in wells:
        p.apply_async(omero_data.get_well_details, args=(well,), callback=well_details_callback)
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

    # sort results by id
    wells_sorted = sorted(wells_data, key=lambda k: k['id'])

    print('Writing flat file...')

    # build a dict of all keys which will form the header row of the flat file
    # this is necessary as the metadata key-value pairs might not be uniform across the dataet
    columns = set()
    for well in wells_sorted:
        columns |= set(well.keys())

    # write to a tab delimited file
    with open(pargs.output, 'w') as output:
        w = csv.DictWriter(output, columns, delimiter='\t', lineterminator='\n')
        w.writeheader()
        w.writerows(wells_sorted)
    output.close()

    connect.disconnect(session, pargs.server)
    print('Metadata fetch complete')

if __name__ == '__main__':
    main()
