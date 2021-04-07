{
    'name': 'Followers Icons Groups',
    'version': '0.1',
    'summary': """Followers Icons Groups""",
    'category': 'Tools',
    'author': '@XeviMesones - (Addercomputer)',
    'website': "https://papaya.addercomputer.com/",
    'depends': [],
    'data': [
        'views/assets.xml',
        'views/settings.xml',
    ],
    'qweb': [
        'static/src/xml/followers.xml',
        'static/src/xml/name2value.xml',
    ],
    'installable': True,
    'auto_install': False,
    'post_init_hook': 'set_default_settings_values',
}