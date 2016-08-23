# constants

"""
API Endpoints
"""
# Login/logout
API_LOGIN = '/webclient/login/'
API_LOGOUT = '/webclient/logout/'
# List of all plates
API_PLATES = '/webclient/api/plates/?id={screenId}'
# List of all wells in a plate
API_PLATE = '/webgateway/plate/{id}'
# Annotation for a well field
API_WELL_ANNOTATIONS = '/webclient/api/annotations/?type={type}&image={id}'
# Table for a well
API_WELL_TABLES = '/webgateway/table/Screen.plateLinks.child.wells/{wellId}/query/?query=Well-{wellId}'
# Image for a well filed
API_IMAGE = '/webclient/render_image/{id}/{z}/{t}/'
# Image per channel for a well filed
API_IMAGE_CHANNEL = '/webclient/render_split_channel/{id}/{z}/{t}/'
# Image thumbnale
API_IMAGE_THUMBNALE = '/webgateway/render_thumbnail/{id}/{w}/?z={z}&t={t}/'
# Image data in json file format
API_IMAGE_DATA = '/webgateway/imgData/{id}/'
# Annotation types, used in conjunction with API_WELL_ANNOTATIONS
API_WELL_ANNOTATION_TYPES = ['tag', 'map', 'file', 'rating', 'comment', 'custom']
