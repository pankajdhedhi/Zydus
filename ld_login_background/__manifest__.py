# -*- encoding: utf-8 -*-
{
    'name': 'Odoo Login page background',
    'summary': 'The new configurable Odoo Web Login Screen',
    'version': '16.0.0.1',
    'category': 'website',
    'summary': """
    You can customised login page like add background image or color and change position of login form.
    """,
    'author': 'TiMAD IT Solutions',
    'company': 'TiMAD IT Solutions',
    'maintainer': 'TiMAD IT Solutions',
    'website': 'https://timadit.com',
    'license': 'LGPL-3',
    'depends': ['base', 'base_setup', 'web', 'auth_signup'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
        'views/login_image.xml',
        'templates/assets.xml',
        'templates/left_login_template.xml',
        'templates/right_login_template.xml',
        'templates/middle_login_template.xml',
    ],
    # 'assets': {
    #     'web.assets_frontend': [
    #         'ld_login_background/static/src/css/web_login_style.css',
    #     ]
    # },
    'qweb': [
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
}

