import os
import requests
from omeroidr.constants import API_IMAGE

class Images:

    def __init__(self, session, base_url: str, save_path: str):
        """
        Utils for fetching OMERO data

        :param base_url: The base URL of the OMERO server
        """
        self.session = session
        self.base_url = base_url
        self.save_path = save_path

    def download_image(self, image_id: int):
        """
        retrieve and save OMERO image

        :param image_id: The id of the image to fetch
        """
        fname = os.path.join(self.save_path, '{0}.jpg'.format(image_id))
        if not os.path.isfile(fname):
            downloadLink = self.base_url + API_IMAGE.format(id=image_id)

            # open web handle
            r = self.session.get(downloadLink, stream=True)

            # write file
            with open(fname, 'wb') as fd:
               for o_chunk in r.iter_content(chunk_size=1024):
                   fd.write(o_chunk)
            fd.close()

