import requests
from odoo import models, api
import logging

_logger = logging.getLogger(__name__)


class GroveOrderSync(models.Model):
    _name = 'grove.order.sync'
    _description = 'Grove Order Sync'

    @api.model
    def sync_orders(self):
        # Replace with the actual URL and fetch credentials from system parameters
        url = self.env['ir.config_parameter'].sudo().get_param('grove_app.api_url')
        api_key = self.env['ir.config_parameter'].sudo().get_param('grove_app.secret_token')

        headers = {
            'secret_token': api_key
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            try:
                orders = response.json()
                _logger.error('orders: %s', orders)
                self._create_odoo_order(orders)
            except ValueError as e:
                _logger.error('Failed to parse JSON response from Grove app: %s', e)
        except requests.exceptions.RequestException as e:
            _logger.error('Failed to fetch orders from Grove app: %s', e)

    def _create_odoo_order(self, data):
        _logger.error('data: %s', data)
        # Group data by order_id
        orders_grouped = {}
        for line in data:
            order_id = line['order_id']
            if order_id not in orders_grouped:
                orders_grouped[order_id] = []
            orders_grouped[order_id].append(line)

        # Process each order
        for order_id, lines in orders_grouped.items():
            # Check if the order_id already exists in sales.order
            existing_order = self.env['sale.order'].search([('grove_order_id', '=', order_id)], limit=1)
            if existing_order:
                continue  # Skip if the order already exists

            order_data = lines[0]  # Use the first line to get customer details, delivery date, etc.

            partner = self.env['res.partner'].search([('name', '=', order_data['customer_first_name'])], limit=1)
            if not partner:
                partner = self.env['res.partner'].create({
                    'name': order_data['customer_first_name'],
                    'phone': order_data['phone'],
                })
            else:
                partner.write({'phone': order_data['phone']})

            order_lines = []
            for line in lines:
                product = self.env['product.template'].search([('sku', '=', line['SKU'])], limit=1)
                if not product:
                    product = self.env['product.template'].create({
                        'name': f'Dummy Product {line["SKU"]}',
                        'default_code': "",
                        'sku': line['SKU'],
                        'type': 'product',
                        'list_price': 0.0,  # Set an initial price, which can be updated later
                    })

                order_lines.append((0, 0, {
                    'product_template_id': product.id,
                    'product_id': product.product_variant_id.id,
                    'product_uom_qty': line['quantity'],
                    'price_unit': product.list_price,  # Use the product's list price
                }))

            order_values = {
                'partner_id': partner.id,
                'grove_order_id': order_data['order_id'],
                'state': 'draft',
                'origin': str(order_data['order_id']),
                'commitment_date': order_data['delivery_date'],
                'order_line': order_lines,
            }

            self.env['sale.order'].sudo().create(order_values)
