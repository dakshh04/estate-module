{
    'name': 'Everpay NBFC',
    'version': '1.0',
    'summary': 'Manage loans and borrower information for NBFC',
    'sequence': 10,
    'description': """
        Everpay NBFC Module
        =======================
        Manage loan leads and borrower addresses for a Non-Banking Financial Company.
    """,
    'category': 'Finance',
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['base'],
    'data': [
        'views/borrower_address_views.xml',
        'views/geo_tagging_views.xml',
        'views/borrower_bank_account_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
