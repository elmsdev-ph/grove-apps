from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    grove_order_id = fields.Integer(string='Grove Order ID', readonly=True, copy=False)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    sku = fields.Char(related='product_template_id.sku', string='SKU', readonly=True) 
