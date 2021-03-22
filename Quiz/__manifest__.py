{
    'name': 'Quiz',
    'version': '0.1',
    'summary': """Quiz""",
    'category': 'Tools',
    'author': '@XeviMesones',
    'depends': ['base', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'views/question.xml',
        'views/question_type.xml',
        'views/quiz.xml',
        'views/question_statistics.xml',
        'views/settings.xml',
    ],
    'installable': True,
    'auto_install': False,
}