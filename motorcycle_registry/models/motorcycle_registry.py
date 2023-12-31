from odoo import api, fields, models
from odoo.exceptions import ValidationError
import re

class MotorcycleRegistry(models.Model):
    _name = 'motorcycle.registry'
    _description = 'Motorcycle Registry'
    _rec_name = "registry_number"
    _sql_constraints = [('vin_unique', 'UNIQUE(vin)', 'VIN must be unique, please verify the list')]
    
    name = fields.Char(string="Motorcycle Registry")
    
    registry_number = fields.Char(string='Registry Number', default="MRN0000", copy=False, required=True, readonly=True)
    certificate_title = fields.Binary(string='Certificate of Title')
    current_mileage = fields.Float(string='Current Mileage')
    #first_name = fields.Char(string='First Name', required=True)
    #last_name = fields.Char(string='Last Name', required=True)
    license_plate = fields.Char(string='License Plate Number')
    registry_date = fields.Date('Registration Date')
    vin = fields.Char(string='VIN', required=True)
    picture = fields.Image (string='Photograph')
    active = fields.Boolean(default=True)
    
    owner_id = fields.Many2one(comodel_name="res.partner", string='Owner', ondelete='restrict', required=True)
    owner_email = fields.Char(string='Owner Email', related='owner_id.email', readonly=True)
    owner_phone = fields.Char(string='Owner Phone', related='owner_id.phone', readonly=True)
    
    make = fields.Char(string='Make', compute='_compute_make_model_year', store=True)
    model = fields.Char(string='Model', compute='_compute_make_model_year', store=True)
    year = fields.Char(string='Year', compute='_compute_make_model_year', store=True)

    @api.depends('vin')
    def _compute_make_model_year(self):
        for record in self:
            if record.vin and len(record.vin) >= 6:
                record.make = record.vin[:2]
                record.model = record.vin[2:4]
                record.year = record.vin[4:6]
            else:
                record.make = False
                record.model = False
                record.year = False
    
       
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('registry_number', ('MRN0000')) == ('MRN0000'):
                vals['registry_number'] = self.env['ir.sequence'].next_by_code('registry.number')
            
            pattern_license_plate = '^[A-Z]{1,3}\d{1,4}[A-Z]{0,2}$'
            if 'license_plate' in vals and not re.match(pattern_license_plate, vals['license_plate']):
                raise ValidationError('Número de Placa Inválido')

            pattern_VIN = '^[A-Z]{4}\d{2}[A-Z0-9]{2}\d{5}$'
            if 'vin' in vals and not re.match(pattern_VIN, vals['vin']):
                raise ValidationError('Número de VIN Inválido')
        return super().create(vals_list)