from odoo import models, fields


class StockMove(models.Model):
    _inherit = 'stock.move'

    is_check = fields.Boolean(string='Check')
