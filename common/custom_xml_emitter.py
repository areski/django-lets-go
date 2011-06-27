try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
from django.utils.encoding import smart_unicode
from django.utils.xmlutils import SimplerXMLGenerator
from piston.emitters import Emitter
from piston.utils import Mimer

try:
    from settings import API_ALLOWED_IP
except:
    API_ALLOWED_IP = ['localhost', '127.0.0.1']


class CustomXmlEmitter(Emitter):
    def _to_xml(self, xml, data):
        if isinstance(data, (list, tuple)):
            for item in data:
                self._to_xml(xml, item)
        elif isinstance(data, dict):
            for key, value in data.iteritems():
                xml.startElement(key, {})
                self._to_xml(xml, value)
                xml.endElement(key)
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
            API_ALLOWED_IP.index(request.META['REMOTE_ADDR'])
            return True
        except:
            return False

    def challenge(self):
        resp = HttpResponse("Not Authorized")
        resp.status_code = 401
        return resp
