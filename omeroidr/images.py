import os
import urllib.request, urllib.error
from omeroidr.constants import API_IMAGE

class Images:

    def __init__(self, base_url: str, save_path: str):
        """
        Utils for fetching OMERO data

        :param base_url: The base URL of the OMERO server
        """
        self.base_url = base_url
        self.save_path = save_path

    def download_image(self, image_id: int):
        """
        retrieve and save OMERO image

        :param image_id: The id of the image to fetch
        """
        fname = self.save_path + '\\{0}.jpg'.format(image_id)
        if not os.path.isfile(fname):
            downloadLink = self.base_url + API_IMAGE.format(id=image_id)
            try:
                urllib.request.urlretrieve(downloadLink, fname)
            except urllib.error.HTTPError as ex:
                print(ex)
