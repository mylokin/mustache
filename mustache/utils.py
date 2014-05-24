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
