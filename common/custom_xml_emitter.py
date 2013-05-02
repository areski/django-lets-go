#
# Switch2bill-common License
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (C) 2011-2013 Star2Billing S.L.
#
# The Initial Developer of the Original Code is
# Arezqui Belaid <info@star2billing.com>
#

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
from django.utils.encoding import smart_unicode
from django.utils.xmlutils import SimplerXMLGenerator
from piston.emitters import Emitter
from piston.utils import Mimer
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.conf import settings


class CustomXmlEmitter(Emitter):
    def _to_xml(self, xml, data):
        if isinstance(data, (list, tuple)):
            for item in data:
                self._to_xml(xml, item)
        elif isinstance(data, dict):
            for key, value in data.iteritems():
                xml.startElement(key, {})
                self._to_xml(xml, value)
                xml.endElement(key.split()[0])
        else:
            xml.characters(smart_unicode(data))

    def render(self, request):
        stream = StringIO.StringIO()
        xml = SimplerXMLGenerator(stream, "utf-8")
        xml.startDocument()
        xml.startElement("Response", {})
        self._to_xml(xml, self.construct())
        xml.endElement("Response")
        xml.endDocument()
        return stream.getvalue()

Emitter.register('custom_xml', CustomXmlEmitter, 'text/xml; charset=utf-8')
Mimer.register(lambda *a: None, ('text/xml',))


class IpAuthentication(object):
    """IP Authentication handler
    """
    def __init__(self, auth_func=authenticate, realm='API'):
        self.auth_func = auth_func
        self.realm = realm

    def is_authenticated(self, request):
        try:
            settings.API_ALLOWED_IP.index(request.META['REMOTE_ADDR'])
            return True
        except:
            return False

    def challenge(self):
        resp = HttpResponse("Not Authorized")
        resp.status_code = 401
        return resp
