import json

from odoo import _, api, fields, models

from odoo17.odoo.exceptions import UserError


class StagingResPartner(models.Model):
    _name = "staging.farmer.profile"
    _description = "Staging Faremer Profile"

    name = fields.Char(string='Name')
    partner_data = fields.Json(string='Partner Data (JSON)')

    def publish_record(self):
        # new_rec = json.loads(self.partner_data)
        self.env["res.partner"].create(self.partner_data)

    def action_open_wizard(self):
        self.ensure_one()  # Ensure this action is performed on a single record
        if not self.partner_data:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Create Partner Data',
                'view_mode': 'form',
                'res_model': 'partner.transient',  # Adjust this to your target model
                'target': 'new',
                'context': { # Pre-fill default values if needed
                    'default_json_record_id': self.id,
                    # Add other context keys as required
                },
                # This will open the form in a modal dialog

            }

        # Load JSON data
        json_data = self.partner_data

        # Create and populate the wizard
        wizard = self.env['partner.transient'].create({
            'name': json_data.get('given_name', ''),
            'age': json_data.get('age', 0),
            'json_record_id': self.id
        })

        # Open the wizard form view
        return {
            'type': 'ir.actions.act_window',
            'name': 'Edit Partner Data',
            'res_model': 'partner.transient',
            'view_mode': 'form',
            'res_id': wizard.id,
            'target': 'new',
            'context': {  # Pre-fill default values if needed
                'default_json_record_id': self.id,
                # Add other context keys as required
            },
        }