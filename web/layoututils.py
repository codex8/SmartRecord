import xml.etree.cElementTree as Et
import collections
import re

UINode = collections.namedtuple('UINode', [
    'xml',
    'bounds',
    'clickable',
    'resource_id',
    'text', 'content_desc',
    'package'])


def dump_nodes(hierarchy_view):
    """Dump current screen UI to list
    Returns:
        List of UINode object, For
        example:

        [UINode(
            bounds=Bounds(left=0, top=0, right=480, bottom=168),
            checkable=False,
            class_name='android.view.View',
            text='',
            resource_id='',
            package='com.sonyericsson.advancedwidget.clock')]
    """
    root = Et.fromstring(hierarchy_view)
    nodes = root.iter('node')
    ui_nodes = []
    for node in nodes:
        ui_nodes.append(_parse_xml_node(node))
    return ui_nodes


def _parse_xml_node(node):
        # ['bounds', 'checkable', 'class', 'text', 'resource_id', 'package']
        __alias = {
            'class': 'class_name',
            'resource-id': 'resource_id',
            'content-desc': 'content_desc',
            'long-clickable': 'long_clickable',
        }

        def parse_bounds(text):
            m = re.match(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', text)
            if m is None:
                return None
            return Bounds(*map(int, m.groups()))

        def str2bool(v):
            return v.lower() in ("yes", "true", "t", "1")

        def convstr(v):
            return v.encode('utf-8')

        parsers = {
            'bounds': parse_bounds,
            'text': convstr,
            'resource_id': convstr,
            'package': convstr,
            'clickable': str2bool,
            'content_desc': convstr,
        }
        ks = {}
        for key, value in node.attrib.items():
            key = __alias.get(key, key)
            f = parsers.get(key)
            if value is None:
                pass
            elif f:
                ks[key] = f(value)
        for key in parsers.keys():
            ks[key] = ks.get(key)
        ks['xml'] = node

        return UINode(**ks)


__boundstuple = collections.namedtuple('Bounds', ['left', 'top', 'right', 'bottom'])


class Bounds(__boundstuple):
    def __init__(self, *args, **kwargs):
        self._area = None

    def is_inside(self, x, y):
        v = self
        return x > v.left and x < v.right and y > v.top and y < v.bottom

    @property
    def area(self):
        if not self._area:
            v = self
            self._area = (v.right-v.left) * (v.bottom-v.top)
        return self._area

    @property
    def center(self):
        v = self
        return (v.left+v.right)/2, (v.top+v.bottom)/2

    def __mul__(self, mul):
        return Bounds(*(int(v*mul) for v in self))


with open('settings.xml') as f:
    t = f.read()
    a = dump_nodes(t)
    for node in a:
        print(node)
