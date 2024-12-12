
from odoo import models, fields, api
import json

from datetime import date, datetime


class TestResPartner(models.Model):
    _name = 'test.res.partner'
    _description = 'JSON Record for Partner'

    name = fields.Char(string='Name')
    # gender = fields.Char(string='Gender')
    age = fields.Char(string='Age')
    # dob = fields.Date(string='DOB')


class PartnerTransient(models.TransientModel):
    _name = 'partner.transient'
    _inherit = 'test.res.partner'
    _description = 'Transient Model for Partner'

    # Add a reference to the JSON record
    json_record_id = fields.Many2one('staging.farmer.profile', string='JSON Record')


    # active = fields.Boolean(default=True)
    #
    # channel_ids = fields.Many2many(
    #     'mail.channel',  # Related model
    #     'res_partner_transient_mail_channel_rel',  # Unique relation table
    #     'partner_id',  # Column for this model
    #     'channel_id',  # Column for the related model
    #     string='Channels'
    # )
    # meeting_ids = fields.Many2many(
    #     'calendar.event',  # The related model
    #     'res_partner_transient_calendar_event_rel',  # Unique relation table
    #     'partner_id',  # Column for this model
    #     'event_id',  # Column for the related model
    #     string='Meetings'
    # )
    #
    # crop_water_sources = fields.Many2many(
    #     'crop.water.source',  # The related model
    #     'res_partner_transient_crop_water_source_rel',  # Unique relation table
    #     'partner_id',  # Column for this model
    #     'water_source_id',  # Column for the related model
    #     string='Crop Water Sources'
    # )
    #
    # livestock_water_sources = fields.Many2many(
    #     'livestock.water.source',  # The related model
    #     'res_partner_transient_livestock_water_source_rel',  # Unique relation table
    #     'partner_id',  # Column for this model
    #     'water_source_id',  # Column for the related model
    #     string='Livestock Water Sources'
    # )


    # @api.model
    # def create(self, vals):
    #     # Create the transient record
    #     record = super().create(vals)
    #
    #     # Store the record as JSON in another model
    #     if record:
    #         self.env['partner.json.record'].create({
    #             'partner_data': json.dumps(record.read()[0])  # Convert the record to JSON
    #         })
    #
    #     return record

    @api.model
    def load_json_data(self, json_record_id):
        json_record = self.env['partner.json.record'].browse(json_record_id)
        if json_record:
            # Parse the JSON data
            data = json.loads(json_record.partner_data)
            data.update({'json_record_id': json_record.id})
            # Create a transient record with the data
            return self.create(data)
        return False

    def save_new_changes(self):
        print("saving the change")
        if self.json_record_id:
            # Extract specific fields to save
            record_data = {
                "is_group": False,
                "is_farmer": "yes",
                "eid": "New",
                "is_registrant": True,
                'given_name': self.name,
                'name': self.name,
                'age': self.age

            }
            print("record is ", record_data)

            # Convert datetime or date fields to string if necessary
            def serialize_data(value):
                if isinstance(value, (date, datetime)):
                    return value.isoformat()
                return value

            # Serialize the dictionary, converting datetime fields
            serialized_data = {key: serialize_data(value) for key, value in record_data.items()}

            # Serialize and save to JSON
            self.json_record_id.partner_data = record_data

        return {'type': 'ir.actions.act_window_close'}


class PartnerJSONRecord(models.Model):
    _name = 'partner.json.record'
    _description = 'JSON Record for Partner'

    name = fields.Char(string='Name')
    partner_data = fields.Text(string='Partner Data (JSON)')

