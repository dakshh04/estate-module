{
    'name': 'Estate',
    'version': '1.0',
    'summary': 'Manage real estate properties and offers',
    'description': """
        Real Estate Management module to handle:
        - Properties
        - Offers
        - Buyers
        - Salespersons
    """,
    'author': 'Your Name or Company',
    'website': 'https://yourcompany.com',
    'category': 'Sales',
    'depends': ['base'],
    'data': [
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_actions.xml',
        'views/estate_menus.xml',
        'views/res_users_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
