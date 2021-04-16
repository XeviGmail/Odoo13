{
    'name': 'Quiz Snippet',
    'version': '0.1',
    'summary': """Quiz""",
    'category': 'Tools',
    'author': '@XeviMesones',
    'depends': ['base', 'website', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/question.xml',
        'views/question_type.xml',
        'views/quiz.xml',
        'views/question_statistics.xml',
        'views/templates.xml',
        'views/snippets.xml',
        'views/issues.xml',
    ],
    'qweb': [
        'static/src/xml/chatter.xml',
    ],
    'installable': True,
    'auto_install': False,
}