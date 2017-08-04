import os, sys, inspect
from shutil import copyfile

def generate_default_toc(version_id):
    '''
    INPUT   1. source (string) - Cross site request forgery token used to make rest calls to Akana API.
            2. destination (string) - File path of document to upload.
            3. version_id (string) - App id or version id.
    '''
    dst_path='apidocs/' + version_id
    src_file='templates/toc.{version}.travelportAPI.json'
    dst_file=dst_path + '/' + 'toc.' + version_id + '.json'
    try:
        if not os.path.exists(dst_path):
             os.makedirs(dst_path)
             copyfile(src_file,dst_file)
             print 'Default TOC file created for version - ' + version_id 
        else:
             print 'Skipped TOC file creation. Version - ' + version_id + ' exists'
        return True     
    except IOError, e:
        print '{} > {}() > error = {}'.format(sys.argv[0], inspect.stack()[0][3], e)
        return False
     
