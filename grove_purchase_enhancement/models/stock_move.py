from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    is_check = fields.Boolean(string='Check')


class ProductProduct(models.Model):
    _inherit = 'product.product'

    api.onchange('product_tmpl_id')
    def _onchange_product_id(self):
        if self.product_tmpl_id:
            self.sku = self.product_tmpl_id.sku
        else:
            self.sku = ""

    sku = fields.Char(string='SKU')

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    sku = fields.Char(string='SKU')


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    sku = fields.Char(related='product_id.sku', string='SKU', readonly=True)