# -*- coding: utf-8 -*-
import itertools, mimetools, mimetypes, urllib, urllib2
from cStringIO import StringIO

class MultiPartForm(object):
    def __init__(self):
        self.form_fields = []
        self.files = []
        self.boundary = mimetools.choose_boundary()
        return

    def get_content_type(self):
        return 'multipart/form-data; boundary=%s' % self.boundary

    def add_field(self, name, value):
        self.form_fields.append((name, value))
        return

    def add_file(self, fieldname, filename, fileHandle, mimetype=None):
        body = fileHandle.read()
        if mimetype is None:
            mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'

        self.files.append((fieldname, filename, mimetype, body))
        return

    def __str__(self):
        parts = []
        part_boundary = '--' + self.boundary

        # Add the form fields
        parts.extend(
            [part_boundary,
              'Content-Disposition: form-data; name="%s"' % name,
              '',
              value,
            ] for name, value in self.form_fields)

        # Add the files to upload
        parts.extend(
            [part_boundary,
              'Content-Disposition: file; name="%s"; filename="%s"' % (field_name, filename),
              'Content-Type: %s' % content_type,
              '',
              body,
            ] for field_name, filename, content_type, body in self.files)

        # Flatten the list and add closing boundary marker,
        # then return CR+LF separated data
        flattened = list(itertools.chain(*parts))
        flattened.append('--' + self.boundary + '--')
        flattened.append('')
        return '\r\n'.join(flattened)
