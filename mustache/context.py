import collections
from . import utils

Block = collections.namedtuple('Block', ['open', 'close'])
Delimiter = Block('{{', '}}')


def render(buf, context):
    while Delimiter.open in buf and Delimiter.close in buf:
        pos = Block(buf.index(Delimiter.open), buf.index(Delimiter.close))
        type_ = buf[pos.open + len(Delimiter.open)]
        if type_ in ('#', '^'):
            name = buf[pos.open + len(Delimiter.open) + len(type_): pos.close]

            tag_open = buf[pos.open: pos.close + len(Delimiter.close)]
            if type_ == '#':
                tag_open_positive = tag_open
                tag_open_negative = tag_open.replace('#', '^', 1)
            else:
                tag_open_positive = tag_open.replace('^', '#', 1)
                tag_open_negative = tag_open
            tag_close = u''.join((Delimiter.open, '/', name, Delimiter.close))

            start = buf.index(tag_open)
            stop = buf.index(tag_close) + len(tag_close)

            buf_slice = buf[start:stop]
            diff = buf_slice.count(tag_open_positive) + buf_slice.count(tag_open_negative) - buf_slice.count(tag_close)
            while diff != 0:
                stop = stop + buf[stop:].index(tag_close) + len(tag_close)
                buf_slice = buf[start:stop]
                diff = buf_slice.count(tag_open_positive) + buf_slice.count(tag_open_negative) - buf_slice.count(tag_close)
            tag = buf[start: stop]

            value = utils.get_value(context, name)
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
            raise ValueError(u'Unexpected close tag: {}'.format(buf[pos.open:pos.close + len(Delimiter.close)]))
        elif type_ == '{':
            name = buf[pos.open + len(Delimiter.open) + len(type_): pos.close]
            tag = u''.join((Delimiter.open, '{', name, '}', Delimiter.close))
            value = utils.get_value(context, name)
            buf = buf.replace(tag, utils.escape_braces(utils.smart_text(value)), 1)
            continue
        elif type_ == '&':
            name = buf[pos.open + len(Delimiter.open) + len(type_): pos.close]
            tag = u''.join((Delimiter.open, '&', name, Delimiter.close))
            value = utils.get_value(context, name)
            buf = buf.replace(tag, utils.escape_braces(utils.smart_text(value)), 1)
            continue
        elif type_ == '>':
            raise ValueError(u'Partials should be pre-processed: {}'.format(buf[pos.open:pos.close + len(Delimiter.close)]))
        else:
            name = buf[pos.open + len(Delimiter.open): pos.close]
            value = utils.escape(utils.get_value(context, name))
            tag = u''.join((Delimiter.open, name, Delimiter.close))
            buf = buf.replace(tag, utils.smart_text(value), 1)
            continue

    return buf
