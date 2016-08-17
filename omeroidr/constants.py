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
# Annotation for a well
API_WELL_ANNOTATIONS = '/webclient/api/annotations/?type={type}&image={id}'
# Table for a well
API_WELL_TABLES = '/webgateway/table/Screen.plateLinks.child.wells/{wellId}/query/?query=Well-{wellId}'
# Image for a well
API_IMAGE = '/webclient/render_image/{id}'

# Annotation types, used in conjunction with API_WELL_ANNOTATIONS
API_WELL_ANNOTATION_TYPES = ['tag', 'map', 'file', 'rating', 'comment', 'custom']
