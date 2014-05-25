import re


class Purity(object):
    COMMENT = re.compile('({{!.*?}})', re.S)
    COMMENT_STANDALONE = re.compile('^(\s*{{!.*?}})\s*\r?\n?', re.S | re.M)
    STANDALONE = re.compile('^(?P<whitespace>\s*(?P<tag>{{[#>^/]\s*[\w\d\.]+\s*}})\r?\n)', re.M)


def purify(template):
    template = Purity.COMMENT_STANDALONE.sub('', template)
    template = Purity.COMMENT.sub('', template)
    template = Purity.STANDALONE.sub('\g<tag>', template)
    if template.endswith('\n'):
        template = template[:-1]
    return template


def get_value(context, name):
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
