{
    'name': 'Grove Purchase Enhancement',
    'version': '1.0',
    'summary': 'Enhancements for purchase orders and inventory receiving',
    'description': """
        Adds a check field to the purchase order line and inventory receiving, with conditional formatting.
    """,
    'category': 'Purchases',
    'author': 'Grove',
    'depends': ['purchase', 'stock', 'sale'],
    'data': [
        'views/purchase_order_views.xml',
        'views/stock_picking_views.xml',
        'views/sale_order.xml',
    ],
    'installable': True,
    'application': False,
}
