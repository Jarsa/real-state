# Copyright 2021, Jarsa
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Estate',
    'summary': '',
    'version': '13.0.1.0.0',
    'category': 'Real Estte',
    'website': 'https://www.jarsa.com.mx/',
    'author': 'Jarsa Sistemas',
    'license': 'LGPL-3',
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_views.xml',
    ],
}
