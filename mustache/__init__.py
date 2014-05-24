import cgi
import collections
import os
import re

# from django.conf import settings

TEMPLATES_DIR = ''  # os.path.join(settings.PROJECT_PATH, 'templates/mustache/')
PARTIAL_REGEXS = (
    re.compile('^(?P<whitespace>\s*)(?P<tag>{{>\s*(?P<name>.+?)\s*}}(?(1)\r?\n?))', re.M),
    re.compile('(?P<tag>{{>\s*(?P<name>.+?)\s*}})'),
)
STANDALONE_COMMENT_REGEX = re.compile('^(\s*{{!.*?}})\s*\r?\n?', re.S | re.M)
COMMENT_REGEX = re.compile('({{!.*?}})', re.S)
STANDALONE_REGEX = re.compile('^(?P<whitespace>\s*(?P<tag>{{[#>^/]\s*[\w\d\.]+\s*}})\r?\n)', re.M)
Block = collections.namedtuple('Block', ['open', 'close'])
delimiter = Block('{{', '}}')


def load_template(path, ext='html', prepare=True, partials=None):
    path = os.path.join(TEMPLATES_DIR, '{}.{}'.format(path, ext))
    with open(path, 'r') as fp:
        template = fp.read()
    if prepare:
        template = process(template, partials)
    return template


def process(template, partials=None):
    template = '{}\n'.format(template)
    for regex in PARTIAL_REGEXS:
        for match in regex.finditer(template):
            if partials is None:
                substitution = load_template(match.group('name'))
            else:
                substitution = partials.get(match.group('name'), u'')

            if substitution:
                try:
                    substitution = '\n'.join('{}{}'.format(match.group('whitespace'), s) if s else s for s in substitution.split('\n'))
                except IndexError:
                    pass
                else:
                    substitution = substitution[len(match.group('whitespace')):]

            template = template.replace(match.group('tag'), substitution)
    template = STANDALONE_COMMENT_REGEX.sub('', template)
    template = COMMENT_REGEX.sub('', template)
    template = STANDALONE_REGEX.sub('\g<tag>', template)
    if template.endswith('\n'):
        template = template[:-1]
    return template


def get_value(name, context):
    name = name.strip()
    if '.' not in name:
        return context.get(name, '')

    value = context
    for namespace in name.split('.'):
        try:
            value = value[namespace]
        except KeyError:
            value = ''
            break
    return value


def escape_braces(value):
    return value.replace('{', '&#123;').replace('}', '&#125;')


def smart_text(value, encoding='utf-8'):
    if isinstance(value, unicode):
        value = value.encode(encoding)
    return str(value)


def escape(value):
    return escape_braces(cgi.escape(smart_text(value), quote=True))


def render(buf, context):
    while delimiter.open in buf and delimiter.close in buf:
        pos = Block(buf.index(delimiter.open), buf.index(delimiter.close))
        type_ = buf[pos.open + len(delimiter.open)]
        if type_ in ('#', '^'):
            name = buf[pos.open + len(delimiter.open) + len(type_): pos.close]

            tag_open = buf[pos.open: pos.close + len(delimiter.close)]
            if type_ == '#':
                tag_open_positive = tag_open
                tag_open_negative = tag_open.replace('#', '^', 1)
            else:
                tag_open_positive = tag_open.replace('^', '#', 1)
                tag_open_negative = tag_open
            tag_close = u''.join((delimiter.open, '/', name, delimiter.close))

            start = buf.index(tag_open)
            stop = buf.index(tag_close) + len(tag_close)

            buf_slice = buf[start:stop]
            diff = buf_slice.count(tag_open_positive) + buf_slice.count(tag_open_negative) - buf_slice.count(tag_close)
            while diff != 0:
                stop = stop + buf[stop:].index(tag_close) + len(tag_close)
                buf_slice = buf[start:stop]
                diff = buf_slice.count(tag_open_positive) + buf_slice.count(tag_open_negative) - buf_slice.count(tag_close)
            tag = buf[start: stop]

            value = get_value(name, context)
            if (value and type_ == '^') or (not value and type_ == '#'):
                buf = buf.replace(tag, '')
                continue

            content = tag[len(tag_open): -len(tag_close)]
            if isinstance(value, collections.Mapping):
                buf = buf.replace(tag, render(content, dict(context, **value)))
                continue
            elif isinstance(value, collections.Callable):
                buf = buf.replace(tag, render(content, dict(context, **value())))
                continue
            elif isinstance(value, collections.Sequence) and not isinstance(value, basestring) and type_ == '#':
                buf = buf.replace(tag, ''.join(map(lambda v: render(content, v), value)))
                continue
            elif (value and type_ == '#') or (not value and type_ == '^'):
                buf = buf.replace(tag, content)
                continue
            else:
                raise ValueError(u'Cannot replace tag: {} {}'.format(tag, value))

        elif type_ == '/':
            raise ValueError(u'Unexpected close tag: {}'.format(buf[pos.open:pos.close + len(delimiter.close)]))
        elif type_ == '{':
            name = buf[pos.open + len(delimiter.open) + len(type_): pos.close]
            tag = u''.join((delimiter.open, '{', name, '}', delimiter.close))
            value = get_value(name, context)
            buf = buf.replace(tag, escape_braces(smart_text(value)), 1)
            continue
        elif type_ == '&':
            name = buf[pos.open + len(delimiter.open) + len(type_): pos.close]
            tag = u''.join((delimiter.open, '&', name, delimiter.close))
            value = get_value(name, context)
            buf = buf.replace(tag, escape_braces(smart_text(value)), 1)
            continue
        elif type_ == '>':
            raise ValueError(u'Partials should be pre-processed: {}'.format(buf[pos.open:pos.close + len(delimiter.close)]))
        else:
            name = buf[pos.open + len(delimiter.open): pos.close]
            value = escape(get_value(name, context))
            tag = u''.join((delimiter.open, name, delimiter.close))
            buf = buf.replace(tag, smart_text(value), 1)
            continue

    return buf
