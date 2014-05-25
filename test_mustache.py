import unittest
import mustache


class TestPartials(unittest.TestCase):
    def test_partials_0(self):
        template = u'"{{>text}}"'
        template = mustache.template.build(template, partials={u'text': u'from partial'})
        context = {}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'"from partial"')

    def test_partials_1(self):
        template = u'"{{>text}}"'
        template = mustache.template.build(template, partials={})
        context = {}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'""')

    def test_partials_2(self):
        template = u'"{{>partial}}"'
        template = mustache.template.build(template, partials={u'partial': u'*{{text}}*'})
        context = {u'text': u'content'}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'"*content*"')

    def test_partials_3(self):
        template = u'{{>node}}'
        template = mustache.template.build(template, partials={u'node': u'{{content}}<{{#nodes}}{{>node}}{{/nodes}}>'})
        context = {u'content': u'X', u'nodes': [{u'content': u'Y', u'nodes': []}]}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'X<Y<>>')

    def test_partials_4(self):
        template = u'| {{>partial}} |'
        template = mustache.template.build(template, partials={u'partial': u'\t|\t'})
        context = {}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'| \t|\t |')

    def test_partials_5(self):
        template = u'  {{data}}  {{> partial}}\n'
        template = mustache.template.build(template, partials={u'partial': u'>\n>'})
        context = {u'data': u'|'}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'  |  >\n>\n')

    def test_partials_6(self):
        template = u'|\r\n{{>partial}}\r\n|'
        template = mustache.template.build(template, partials={u'partial': u'>'})
        context = {}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'|\r\n>|')

    def test_partials_7(self):
        template = u'  {{>partial}}\n>'
        template = mustache.template.build(template, partials={u'partial': u'>\n>'})
        context = {}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'  >\n  >>')

    def test_partials_8(self):
        template = u'>\n  {{>partial}}'
        template = mustache.template.build(template, partials={u'partial': u'>\n>'})
        context = {}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'>\n  >\n  >')

    def test_partials_9(self):
        template = u'\\\n {{>partial}}\n/\n'
        template = mustache.template.build(template, partials={u'partial': u'|\n{{{content}}}\n|\n'})
        context = {u'content': u'<\n->'}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'\\\n |\n <\n->\n |\n/\n')

    def test_partials_10(self):
        template = u'|{{> partial }}|'
        template = mustache.template.build(template, partials={u'partial': u'[]'})
        context = {u'boolean': True}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'|[]|')


class TestInverted(unittest.TestCase):
    def test_inverted_0(self):
        template = u'"{{^boolean}}This should be rendered.{{/boolean}}"'
        template = mustache.template.build(template, partials=None)
        context = {u'boolean': False}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'"This should be rendered."')

    def test_inverted_1(self):
        template = u'"{{^boolean}}This should not be rendered.{{/boolean}}"'
        template = mustache.template.build(template, partials=None)
        context = {u'boolean': True}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'""')

    def test_inverted_2(self):
        template = u'"{{^context}}Hi {{name}}.{{/context}}"'
        template = mustache.template.build(template, partials=None)
        context = {u'context': {u'name': u'Joe'}}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'""')

    def test_inverted_3(self):
        template = u'"{{^list}}{{n}}{{/list}}"'
        template = mustache.template.build(template, partials=None)
        context = {u'list': [{u'n': 1}, {u'n': 2}, {u'n': 3}]}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'""')

    def test_inverted_4(self):
        template = u'"{{^list}}Yay lists!{{/list}}"'
        template = mustache.template.build(template, partials=None)
        context = {u'list': []}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'"Yay lists!"')

    def test_inverted_5(self):
        template = u'{{^bool}}\n* first\n{{/bool}}\n* {{two}}\n{{^bool}}\n* third\n{{/bool}}\n'
        template = mustache.template.build(template, partials=None)
        context = {u'bool': False, u'two': u'second'}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'* first\n* second\n* third\n')

    def test_inverted_6(self):
        template = u'| A {{^bool}}B {{^bool}}C{{/bool}} D{{/bool}} E |'
        template = mustache.template.build(template, partials=None)
        context = {u'bool': False}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'| A B C D E |')

    def test_inverted_7(self):
        template = u'| A {{^bool}}B {{^bool}}C{{/bool}} D{{/bool}} E |'
        template = mustache.template.build(template, partials=None)
        context = {u'bool': True}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'| A  E |')

    def test_inverted_8(self):
        template = u"[{{^missing}}Cannot find key 'missing'!{{/missing}}]"
        template = mustache.template.build(template, partials=None)
        context = {}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u"[Cannot find key 'missing'!]")

    def test_inverted_9(self):
        template = u'"{{^a.b.c}}Not Here{{/a.b.c}}" == ""'
        template = mustache.template.build(template, partials=None)
        context = {u'a': {u'b': {u'c': True}}}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'"" == ""')

    def test_inverted_10(self):
        template = u'"{{^a.b.c}}Not Here{{/a.b.c}}" == "Not Here"'
        template = mustache.template.build(template, partials=None)
        context = {u'a': {u'b': {u'c': False}}}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'"Not Here" == "Not Here"')

    def test_inverted_11(self):
        template = u'"{{^a.b.c}}Not Here{{/a.b.c}}" == "Not Here"'
        template = mustache.template.build(template, partials=None)
        context = {u'a': {}}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'"Not Here" == "Not Here"')

    def test_inverted_12(self):
        template = u' | {{^boolean}}\t|\t{{/boolean}} | \n'
        template = mustache.template.build(template, partials=None)
        context = {u'boolean': False}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u' | \t|\t | \n')

    def test_inverted_13(self):
        template = u' | {{^boolean}} {{! Important Whitespace }}\n {{/boolean}} | \n'
        template = mustache.template.build(template, partials=None)
        context = {u'boolean': False}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u' |  \n  | \n')

    def test_inverted_14(self):
        template = u' {{^boolean}}NO{{/boolean}}\n {{^boolean}}WAY{{/boolean}}\n'
        template = mustache.template.build(template, partials=None)
        context = {u'boolean': False}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u' NO\n WAY\n')

    def test_inverted_15(self):
        template = u'| This Is\n{{^boolean}}\n|\n{{/boolean}}\n| A Line\n'
        template = mustache.template.build(template, partials=None)
        context = {u'boolean': False}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'| This Is\n|\n| A Line\n')

    def test_inverted_16(self):
        template = u'| This Is\n  {{^boolean}}\n|\n  {{/boolean}}\n| A Line\n'
        template = mustache.template.build(template, partials=None)
        context = {u'boolean': False}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'| This Is\n|\n| A Line\n')

    def test_inverted_17(self):
        template = u'|\r\n{{^boolean}}\r\n{{/boolean}}\r\n|'
        template = mustache.template.build(template, partials=None)
        context = {u'boolean': False}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'|\r\n|')

    def test_inverted_18(self):
        template = u'  {{^boolean}}\n^{{/boolean}}\n/'
        template = mustache.template.build(template, partials=None)
        context = {u'boolean': False}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'^\n/')

    def test_inverted_19(self):
        template = u'^{{^boolean}}\n/\n  {{/boolean}}'
        template = mustache.template.build(template, partials=None)
        context = {u'boolean': False}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'^\n/\n')

    def test_inverted_20(self):
        template = u'|{{^ boolean }}={{/ boolean }}|'
        template = mustache.template.build(template, partials=None)
        context = {u'boolean': False}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'|=|')


class TestSections(unittest.TestCase):
    def test_sections_0(self):
        template = u'"{{#boolean}}This should be rendered.{{/boolean}}"'
        template = mustache.template.build(template, partials=None)
        context = {u'boolean': True}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'"This should be rendered."')

    def test_sections_1(self):
        template = u'"{{#boolean}}This should not be rendered.{{/boolean}}"'
        template = mustache.template.build(template, partials=None)
        context = {u'boolean': False}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'""')

    def test_sections_2(self):
        template = u'"{{#context}}Hi {{name}}.{{/context}}"'
        template = mustache.template.build(template, partials=None)
        context = {u'context': {u'name': u'Joe'}}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'"Hi Joe."')

    def test_sections_3(self):
        template = u'{{#a}}\n{{one}}\n{{#b}}\n{{one}}{{two}}{{one}}\n{{#c}}\n{{one}}{{two}}{{three}}{{two}}{{one}}\n{{#d}}\n{{one}}{{two}}{{three}}{{four}}{{three}}{{two}}{{one}}\n{{#e}}\n{{one}}{{two}}{{three}}{{four}}{{five}}{{four}}{{three}}{{two}}{{one}}\n{{/e}}\n{{one}}{{two}}{{three}}{{four}}{{three}}{{two}}{{one}}\n{{/d}}\n{{one}}{{two}}{{three}}{{two}}{{one}}\n{{/c}}\n{{one}}{{two}}{{one}}\n{{/b}}\n{{one}}\n{{/a}}\n'
        template = mustache.template.build(template, partials=None)
        context = {u'a': {u'one': 1}, u'c': {u'three': 3}, u'b': {u'two': 2}, u'e': {u'five': 5}, u'd': {u'four': 4}}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'1\n121\n12321\n1234321\n123454321\n1234321\n12321\n121\n1\n')

    def test_sections_4(self):
        template = u'"{{#list}}{{item}}{{/list}}"'
        template = mustache.template.build(template, partials=None)
        context = {u'list': [{u'item': 1}, {u'item': 2}, {u'item': 3}]}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'"123"')

    def test_sections_5(self):
        template = u'"{{#list}}Yay lists!{{/list}}"'
        template = mustache.template.build(template, partials=None)
        context = {u'list': []}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'""')

    def test_sections_6(self):
        template = u'{{#bool}}\n* first\n{{/bool}}\n* {{two}}\n{{#bool}}\n* third\n{{/bool}}\n'
        template = mustache.template.build(template, partials=None)
        context = {u'bool': True, u'two': u'second'}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'* first\n* second\n* third\n')

    def test_sections_7(self):
        template = u'| A {{#bool}}B {{#bool}}C{{/bool}} D{{/bool}} E |'
        template = mustache.template.build(template, partials=None)
        context = {u'bool': True}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'| A B C D E |')

    def test_sections_8(self):
        template = u'| A {{#bool}}B {{#bool}}C{{/bool}} D{{/bool}} E |'
        template = mustache.template.build(template, partials=None)
        context = {u'bool': False}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'| A  E |')

    def test_sections_9(self):
        template = u"[{{#missing}}Found key 'missing'!{{/missing}}]"
        template = mustache.template.build(template, partials=None)
        context = {}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'[]')

    def test_sections_10(self):
        template = u'"{{#a.b.c}}Here{{/a.b.c}}" == "Here"'
        template = mustache.template.build(template, partials=None)
        context = {u'a': {u'b': {u'c': True}}}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'"Here" == "Here"')

    def test_sections_11(self):
        template = u'"{{#a.b.c}}Here{{/a.b.c}}" == ""'
        template = mustache.template.build(template, partials=None)
        context = {u'a': {u'b': {u'c': False}}}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'"" == ""')

    def test_sections_12(self):
        template = u'"{{#a.b.c}}Here{{/a.b.c}}" == ""'
        template = mustache.template.build(template, partials=None)
        context = {u'a': {}}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'"" == ""')

    def test_sections_13(self):
        template = u' | {{#boolean}}\t|\t{{/boolean}} | \n'
        template = mustache.template.build(template, partials=None)
        context = {u'boolean': True}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u' | \t|\t | \n')

    def test_sections_14(self):
        template = u' | {{#boolean}} {{! Important Whitespace }}\n {{/boolean}} | \n'
        template = mustache.template.build(template, partials=None)
        context = {u'boolean': True}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u' |  \n  | \n')

    def test_sections_15(self):
        template = u' {{#boolean}}YES{{/boolean}}\n {{#boolean}}GOOD{{/boolean}}\n'
        template = mustache.template.build(template, partials=None)
        context = {u'boolean': True}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u' YES\n GOOD\n')

    def test_sections_16(self):
        template = u'| This Is\n{{#boolean}}\n|\n{{/boolean}}\n| A Line\n'
        template = mustache.template.build(template, partials=None)
        context = {u'boolean': True}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'| This Is\n|\n| A Line\n')

    def test_sections_17(self):
        template = u'| This Is\n  {{#boolean}}\n|\n  {{/boolean}}\n| A Line\n'
        template = mustache.template.build(template, partials=None)
        context = {u'boolean': True}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'| This Is\n|\n| A Line\n')

    def test_sections_18(self):
        template = u'|\r\n{{#boolean}}\r\n{{/boolean}}\r\n|'
        template = mustache.template.build(template, partials=None)
        context = {u'boolean': True}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'|\r\n|')

    def test_sections_19(self):
        template = u'  {{#boolean}}\n#{{/boolean}}\n/'
        template = mustache.template.build(template, partials=None)
        context = {u'boolean': True}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'#\n/')

    def test_sections_20(self):
        template = u'#{{#boolean}}\n/\n  {{/boolean}}'
        template = mustache.template.build(template, partials=None)
        context = {u'boolean': True}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'#\n/\n')

    def test_sections_21(self):
        template = u'|{{# boolean }}={{/ boolean }}|'
        template = mustache.template.build(template, partials=None)
        context = {u'boolean': True}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'|=|')


class TestComments(unittest.TestCase):
    def test_comments_0(self):
        template = u'12345{{! Comment Block! }}67890'
        template = mustache.template.build(template, partials=None)
        context = {}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'1234567890')

    def test_comments_1(self):
        template = u'12345{{!\n  This is a\n  multi-line comment...\n}}67890\n'
        template = mustache.template.build(template, partials=None)
        context = {}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'1234567890\n')

    def test_comments_2(self):
        template = u'Begin.\n{{! Comment Block! }}\nEnd.\n'
        template = mustache.template.build(template, partials=None)
        context = {}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'Begin.\nEnd.\n')

    def test_comments_3(self):
        template = u'Begin.\n  {{! Indented Comment Block! }}\nEnd.\n'
        template = mustache.template.build(template, partials=None)
        context = {}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'Begin.\nEnd.\n')

    def test_comments_4(self):
        template = u'|\r\n{{! Standalone Comment }}\r\n|'
        template = mustache.template.build(template, partials=None)
        context = {}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'|\r\n|')

    def test_comments_5(self):
        template = u"Begin.\n{{!\nSomething's going on here...\n}}\nEnd.\n"
        template = mustache.template.build(template, partials=None)
        context = {}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'Begin.\nEnd.\n')

    def test_comments_6(self):
        template = u"Begin.\n  {{!\n    Something's going on here...\n  }}\nEnd.\n"
        template = mustache.template.build(template, partials=None)
        context = {}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'Begin.\nEnd.\n')

    def test_comments_7(self):
        template = u'  12 {{! 34 }}\n'
        template = mustache.template.build(template, partials=None)
        context = {}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'  12 \n')

    def test_comments_8(self):
        template = u'12345 {{! Comment Block! }} 67890'
        template = mustache.template.build(template, partials=None)
        context = {}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'12345  67890')


class TestInterpolation(unittest.TestCase):
    def test_interpolation_0(self):
        template = u'Hello from {Mustache}!\n'
        template = mustache.template.build(template, partials=None)
        context = {}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'Hello from {Mustache}!\n')

    def test_interpolation_1(self):
        template = u'Hello, {{subject}}!\n'
        template = mustache.template.build(template, partials=None)
        context = {u'subject': u'world'}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'Hello, world!\n')

    def test_interpolation_2(self):
        template = u'These characters should be HTML escaped: {{forbidden}}\n'
        template = mustache.template.build(template, partials=None)
        context = {u'forbidden': u'& " < >'}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'These characters should be HTML escaped: &amp; &quot; &lt; &gt;\n')

    def test_interpolation_3(self):
        template = u'These characters should not be HTML escaped: {{{forbidden}}}\n'
        template = mustache.template.build(template, partials=None)
        context = {u'forbidden': u'& " < >'}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'These characters should not be HTML escaped: & " < >\n')

    def test_interpolation_4(self):
        template = u'These characters should not be HTML escaped: {{&forbidden}}\n'
        template = mustache.template.build(template, partials=None)
        context = {u'forbidden': u'& " < >'}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'These characters should not be HTML escaped: & " < >\n')

    def test_interpolation_5(self):
        template = u'"{{mph}} miles an hour!"'
        template = mustache.template.build(template, partials=None)
        context = {u'mph': 85}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'"85 miles an hour!"')

    def test_interpolation_6(self):
        template = u'"{{{mph}}} miles an hour!"'
        template = mustache.template.build(template, partials=None)
        context = {u'mph': 85}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'"85 miles an hour!"')

    def test_interpolation_7(self):
        template = u'"{{&mph}} miles an hour!"'
        template = mustache.template.build(template, partials=None)
        context = {u'mph': 85}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'"85 miles an hour!"')

    def test_interpolation_8(self):
        template = u'"{{power}} jiggawatts!"'
        template = mustache.template.build(template, partials=None)
        context = {u'power': 1.21}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'"1.21 jiggawatts!"')

    def test_interpolation_9(self):
        template = u'"{{{power}}} jiggawatts!"'
        template = mustache.template.build(template, partials=None)
        context = {u'power': 1.21}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'"1.21 jiggawatts!"')

    def test_interpolation_10(self):
        template = u'"{{&power}} jiggawatts!"'
        template = mustache.template.build(template, partials=None)
        context = {u'power': 1.21}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'"1.21 jiggawatts!"')

    def test_interpolation_11(self):
        template = u'I ({{cannot}}) be seen!'
        template = mustache.template.build(template, partials=None)
        context = {}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'I () be seen!')

    def test_interpolation_12(self):
        template = u'I ({{{cannot}}}) be seen!'
        template = mustache.template.build(template, partials=None)
        context = {}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'I () be seen!')

    def test_interpolation_13(self):
        template = u'I ({{&cannot}}) be seen!'
        template = mustache.template.build(template, partials=None)
        context = {}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'I () be seen!')

    def test_interpolation_14(self):
        template = u'"{{person.name}}" == "{{#person}}{{name}}{{/person}}"'
        template = mustache.template.build(template, partials=None)
        context = {u'person': {u'name': u'Joe'}}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'"Joe" == "Joe"')

    def test_interpolation_15(self):
        template = u'"{{{person.name}}}" == "{{#person}}{{{name}}}{{/person}}"'
        template = mustache.template.build(template, partials=None)
        context = {u'person': {u'name': u'Joe'}}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'"Joe" == "Joe"')

    def test_interpolation_16(self):
        template = u'"{{&person.name}}" == "{{#person}}{{&name}}{{/person}}"'
        template = mustache.template.build(template, partials=None)
        context = {u'person': {u'name': u'Joe'}}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'"Joe" == "Joe"')

    def test_interpolation_17(self):
        template = u'"{{a.b.c.d.e.name}}" == "Phil"'
        template = mustache.template.build(template, partials=None)
        context = {u'a': {u'b': {u'c': {u'd': {u'e': {u'name': u'Phil'}}}}}}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'"Phil" == "Phil"')

    def test_interpolation_18(self):
        template = u'"{{a.b.c}}" == ""'
        template = mustache.template.build(template, partials=None)
        context = {u'a': {}}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'"" == ""')

    def test_interpolation_19(self):
        template = u'"{{a.b.c.name}}" == ""'
        template = mustache.template.build(template, partials=None)
        context = {u'a': {u'b': {}}, u'c': {u'name': u'Jim'}}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'"" == ""')

    def test_interpolation_20(self):
        template = u'"{{#a}}{{b.c.d.e.name}}{{/a}}" == "Phil"'
        template = mustache.template.build(template, partials=None)
        context = {u'a': {u'b': {u'c': {u'd': {u'e': {u'name': u'Phil'}}}}}, u'b': {u'c': {u'd': {u'e': {u'name': u'Wrong'}}}}}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'"Phil" == "Phil"')

    def test_interpolation_21(self):
        template = u'| {{string}} |'
        template = mustache.template.build(template, partials=None)
        context = {u'string': u'---'}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'| --- |')

    def test_interpolation_22(self):
        template = u'| {{{string}}} |'
        template = mustache.template.build(template, partials=None)
        context = {u'string': u'---'}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'| --- |')

    def test_interpolation_23(self):
        template = u'| {{&string}} |'
        template = mustache.template.build(template, partials=None)
        context = {u'string': u'---'}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'| --- |')

    def test_interpolation_24(self):
        template = u'  {{string}}\n'
        template = mustache.template.build(template, partials=None)
        context = {u'string': u'---'}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'  ---\n')

    def test_interpolation_25(self):
        template = u'  {{{string}}}\n'
        template = mustache.template.build(template, partials=None)
        context = {u'string': u'---'}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'  ---\n')

    def test_interpolation_26(self):
        template = u'  {{&string}}\n'
        template = mustache.template.build(template, partials=None)
        context = {u'string': u'---'}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'  ---\n')

    def test_interpolation_27(self):
        template = u'|{{ string }}|'
        template = mustache.template.build(template, partials=None)
        context = {u'string': u'---'}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'|---|')

    def test_interpolation_28(self):
        template = u'|{{{ string }}}|'
        template = mustache.template.build(template, partials=None)
        context = {u'string': u'---'}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'|---|')

    def test_interpolation_29(self):
        template = u'|{{& string }}|'
        template = mustache.template.build(template, partials=None)
        context = {u'string': u'---'}
        rendered = mustache.render(template, context)
        self.assertEqual(rendered, u'|---|')


if __name__ == '__main__':
    unittest.main()
