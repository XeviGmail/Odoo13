{
    'name': 'Learn FrontBackend',
    'version': '0.1',
    'summary': """FrontBackend""",
    'category': 'Learning',
    'author': '@XeviMesones',
    'depends': [
        'web',
        'website',
        'product',
        'website_sale',
    ],
    'data': [
        'views/product.xml',
        'views/assets.xml',
    ],
    'qweb': [
        'static/src/xml/field.xml',
        'static/src/xml/followers.xml',
    ],
    'installable': True,
    'auto_install': False,
}