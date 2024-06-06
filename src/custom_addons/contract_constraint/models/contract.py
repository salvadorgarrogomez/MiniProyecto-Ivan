from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
import re

class Contract(models.Model):
    _name = "contract"
    _description = "Contract Constraint"
    
    name = fields.Char(string="Nombre: ")
    telephone = fields.Char(
        string="Telefono: ")
    country_id = fields.Many2one(
        comodel_name="res.country",
        string="País")
    mobile = fields.Char(
        string="Movil: ")
    partner_id = fields.Many2one(
        comodel_name = 'res.partner', 
        string="Partner")
    partner_email= fields.Char(
        string = "Correo: ",
        related="partner_id.email")
    
    identifier = fields.Selection([
            ('DNI', 'DNI'),
            ('NIF', 'NIF'),
        ],
        string="Identificador: ")
    identification_number = fields.Char(
        string="Número de Identificación: ")

    @api.constrains('telephone', 'country_id', 'partner_email')
    def _check_required_fields(self):
        if not self.telephone:
            raise UserError("El campo 'Telefono' es obligatorio.")
        if not self.country_id:
            raise UserError("El campo 'País' es obligatorio.")
        if not self.partner_email:
            raise UserError("El campo 'Correo' es obligatorio.")
    
    @api.model
    def clean_phone_number(self, phone_number):
        phone_number = re.sub(r'\s+', '', phone_number)
        if not phone_number.startswith('+34'):
            phone_number = '+34' + phone_number
            if len(phone_number) < 9:
                raise UserError("El número de teléfono debe tener al menos 9 dígitos.")
        formatted_phone_number = ' '.join([phone_number[i:i+3] for i in range(0, len(phone_number), 3)])
        return formatted_phone_number

    @api.onchange('telephone')
    def onchange_telephone(self):
        if self.telephone:
            self.telephone = self.clean_phone_number(self.telephone)
            
    @api.onchange('identifier')
    def onchange_identifier(self):
        if self.identifier == 'DNI':
            self.identification_number = ""
        if self.identifier == 'NIF':
            self.identification_number = ""
            
    @api.constrains('identification_number')
    def _check_identification_number(self):
        for record in self:
            if record.identifier == 'DNI' and record.identification_number:
                if self.country_id and self.country_id.code == 'ES':
                    if not self._validate_dni(record.identification_number):
                        raise UserError("El DNI proporcionado no es válido.")
            elif record.identifier == 'NIF' and record.identification_number:
                if self.country_id and self.country_id.code == 'ES':
                    if not self._validate_nif(record.identification_number):
                        raise UserError("El NIF proporcionado no es válido.")
    
    def _validate_dni(self, dni):
        if len(dni) != 9:
            return False
        dni_digits = dni[:8]
        control_digit = dni[8].upper()
        if not dni_digits.isdigit():
            return False
        expected_control_digit = 'TRWAGMYFPDXBNJZSQVHLCKE'[int(dni_digits) % 23]
        return expected_control_digit == control_digit
    
    def _validate_nif(self, nif):
        tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
        numeros = "1234567890"
        if len(nif) == 9:
            letraControl = nif[8].upper()
            dni = nif[:8]
            if len(dni) == len([n for n in dni if n in numeros]):
                # Obtener los 7 dígitos centrales
                nif_central_digits = dni[1:8]
                
                # Sumar los dígitos de las posiciones pares y almacenar el resultado en A
                a = sum(int(nif_central_digits[i]) for i in range(0, 6, 2))

                # Multiplicar cada dígito de las posiciones impares por 2, sumar los dígitos del resultado y almacenar en B
                b = sum(int(digit) for i in range(1, 7) for digit in str(int(nif_central_digits[i]) * 2) if digit.isdigit())

                # Sumar A + B y tomar el dígito de las unidades
                c = a + b
                e = c % 10

                # Si el dígito E es distinto de 0, restarlo a 10 y almacenar el resultado en D
                d = 10 - e if e != 0 else 0

                # Obtener el dígito de control a partir de D
                if letraControl.isdigit():
                    if str(d) != letraControl:
                        raise UserError("El NIF proporcionado no es válido.")
                else:
                    control_dict = {'J': 0, 'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9}
                    if control_dict[letraControl] != d:
                        raise UserError("El NIF proporcionado no es válido.")
            else:
                raise UserError("El NIF debe contener solo números en los primeros 8 dígitos.")
        else:
            raise UserError("El NIF debe tener una longitud de 9 caracteres.")

