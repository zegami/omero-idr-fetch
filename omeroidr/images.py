import os
import requests
from omeroidr.constants import API_IMAGE, API_IMAGE_CHANNEL, API_IMAGE_THUMBNALE

class Images:

    def __init__(self, session, base_url: str, save_path: str):
        """
        Utils for fetching OMERO data

        :param base_url: The base URL of the OMERO server
        """
        self.session = session
        self.base_url = base_url
        self.save_path = save_path


    def download_image(self, image_id: int, z=0, t=0, render_setting="", explicit=False) -> str:
        """
        retrieve and save OMERO image

        :param image_id: The id of the image to fetch
        :param z: The z stack number of the image to fetch
        :param t: The t time serial number of the image to fetch
        :param explicit: if True, filename will even in the default case contaon z value, t value and render setting.
        :return: Filename string
        """
        # filename
        if explicit or (z !=0) or (t !=0) or (len(render_setting) > 0):
            fname = os.path.join(self.save_path, '{}_z{}_t{}{}.jpg'.format(image_id,z,t,render_setting))
        else:
            fname = os.path.join(self.save_path, '{}.jpg'.format(image_id))

        # if file not yet downloaded
        if not os.path.isfile(fname) or len(render_setting) > 0:
            downloadLink = self.base_url + API_IMAGE.format(id=image_id,z=z,t=t) + render_setting

            # open web handle
            r = self.session.get(downloadLink, stream=True)

            # write file
            with open(fname, 'wb') as fd:
               for o_chunk in r.iter_content(chunk_size=1024):
                   fd.write(o_chunk)
            fd.close()

        # return file name
        return(fname)


    def download_imagechannel(self, image_id: int, z=0, t=0, render_setting="", explicit=False) -> str:
        """
        retrieve and save OMERO image, each active channel in a separate panel

        :param image_id: The id of the image to fetch
        :param z: The z stack number of the image to fetch
        :param t: The t time serial number of the image to fetch
        :param explicit: if True, filename will even in the default case contaon z value, t value and render setting.
        :return: Filename string
        """
        # filename
        if explicit or (z !=0) or (t !=0) or (len(render_setting) > 0):
            fname = os.path.join(self.save_path, '{}channel_z{}_t{}{}.jpg'.format(image_id,z,t,render_setting))
        else:
            fname = os.path.join(self.save_path, '{}channel.jpg'.format(image_id))

        # if file not yet downloaded
        if not os.path.isfile(fname) or len(render_setting) > 0:
            downloadLink = self.base_url + API_IMAGE_CHANNEL.format(id=image_id,z=z,t=t) + render_setting

            # open web handle
            r = self.session.get(downloadLink, stream=True)

            # write file
            with open(fname, 'wb') as fd:
               for o_chunk in r.iter_content(chunk_size=1024):
                   fd.write(o_chunk)
            fd.close()

        # return file name
        return(fname)


    def download_imagethumb(self, image_id: int, w=64, z=0, t=0, explicit=False) -> str:
        """
        retrieve and save OMERO thumbnale image

        :param image_id: The id of the image to fetch
        :param w: The thumbnale width
        :param z: The z stack number of the image to fetch
        :param t: The t time serial number of the image to fetch
        :param explicit: if True, filename will even in the default case contaon z value, t value and render setting.
        :return: Filename string
        """
        # filename
        if explicit or (w != 64) or (z !=0) or (t !=0):
            fname = os.path.join(self.save_path, '{}thumbnale_w{}_z{}_t{}.jpg'.format(image_id, w, z, t))
        else:
            fname = os.path.join(self.save_path, '{}thumbnale.jpg'.format(image_id))

        # if file not yet downloaded
        if not os.path.isfile(fname):
            downloadLink = self.base_url + API_IMAGE_THUMBNALE.format(id=image_id, w=w, z=z, t=t)

            # open web handle
            r = self.session.get(downloadLink, stream=True)

            # write file
            with open(fname, 'wb') as fd:
               for o_chunk in r.iter_content(chunk_size=1024):
                   fd.write(o_chunk)
            fd.close()

        # return file name
        return(fname)
