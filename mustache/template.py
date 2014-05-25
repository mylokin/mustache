import os
import re
from . import utils


PARTIAL = re.compile('(?P<tag>{{>\s*(?P<name>.+?)\s*}})')
PARTIAL_CUSTOM = re.compile('^(?P<whitespace>\s*)(?P<tag>{{>\s*(?P<name>.+?)\s*}}(?(1)\r?\n?))', re.M)


# def get_template(path, ext='html', partials=None):
#     path = os.path.join(TEMPLATES_DIR, '{}.{}'.format(path, ext))
#     with open(path, 'r') as fp:
#         template = fp.read()
#     return build(template, partials)


def build(template, partials=None):
    template = '{}\n'.format(template)
    for regex in (PARTIAL_CUSTOM, PARTIAL):
        for match in regex.finditer(template):
            if partials is None:
                substitution = get_template(match.group('name'))
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
    return utils.purify(template)
