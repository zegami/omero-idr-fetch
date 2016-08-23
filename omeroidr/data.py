import json
import requests
from omeroidr.constants import API_WELL_ANNOTATIONS, API_WELL_ANNOTATION_TYPES, API_PLATE, API_PLATES, API_WELL_TABLES, API_IMAGE_DATA

class Data:
    def __init__(self, session, base_url: str):
        """
        Utils for fetching OMERO data

        :param base_url: The base URL of the OMERO server
        """
        self.base_url = base_url
        self.session = session

#    @staticmethod
    def get_json(self, url: str) -> dict:
        """
        Get response object for a URL and return JSON object

        :param url: The URL of the endpoint to retrieve
        :return: Dict representing the JSON object
        """
#        request = urllib.request.Request(url)
#        response = urllib.request.urlopen(request)
#        return json.loads(response.read().decode('utf-8'))
        r = self.session.get(url)
        return r.json()

    def get_wells(self, screen_id: int) -> list:
        """
        Get all wells for a screen

        :param screen_id: Screen unique id
        :return: List of wells
        """
        # get all plates
        url = self.base_url + API_PLATES.format(screenId=screen_id)
        plates = self.get_json(url)

        # get wells for each plate
        wells = []
        for plate in plates['plates']:
            url = self.base_url + API_PLATE.format(id=plate['id'])
            plate_data = self.get_json(url)

            # create list of well objects
            for rIdx, rows in enumerate(plate_data['grid']):
                for wIdx, well in enumerate(rows):
                    # construct well object and return
                    if (well != None):
                        wells.append({
                            'id': well['id'],
                            'name': well['name'],
                            'date': well['date'],
                            'author': well['author'],
                            'field': well['field'],
                            'wellId': well['wellId'],
                            'column': plate_data['collabels'][wIdx],
                            'row': plate_data['rowlabels'][rIdx]
                         })
        return wells

    def get_well_details(self, well: dict) -> dict:
        """
        Get all the associated metadata for a well

        :param well: Basic well metadata containing the image and well id
        :return: Dict of the well metadata
        """
        # get annotations of all types
        annotations = {}
        for t in API_WELL_ANNOTATION_TYPES:
            url = self.base_url + API_WELL_ANNOTATIONS.format(type=t, id=well['id'])
            annotation = self.get_json(url)
            if 'annotations' in annotation:
                for a in annotation['annotations']:
                    if 'values' in a:
                        for value in a['values']:
                            val = value[1]
                            annotations[value[0]] = val if type(val) is not str else val if len(val) > 0 else None

        # get well tables
        url = self.base_url + API_WELL_TABLES.format(wellId=well['wellId'])
        tables = self.get_json(url)
        table_data = tables['data']
        for idx, column in enumerate(table_data['columns']):
            if 'rows' in table_data and len(table_data['rows']) > 0:
                val = table_data['rows'][0][idx]
                annotations[column] = val if type(val) is not str else val if len(val) > 0 else None

        # merge annotations
        return dict(well, **annotations)


    def get_imagedata(self, image_id: int) -> dict:
        """
        Get all the associated metadata for an OMERO image

        :param image_id: The id of the image to fetch metadata
        :return: Dict of the image metadata
        """
        # set empty output
        d_json = None

        # get image metadata
        url = self.base_url + API_IMAGE_DATA.format(id=image_id)
        d_json = self.get_json(url)
        # output
        return(d_json)
