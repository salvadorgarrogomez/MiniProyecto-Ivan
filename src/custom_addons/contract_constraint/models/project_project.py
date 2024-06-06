from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    def action_view_tasks(self):
        # tasks = self.env['project.task'].search([
        #     # ('project_id.user_id', '!=', False),
        #     # ('user_ids', '!=', False)
        #     ('partner_id', '=', self.id)
        # ])
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Tareas con Usuarios Asignados',
            'res_model': 'project.task',
            'view_mode': 'tree,form',
            'domain': [('partner_id', '=', self.id)],
            'context': {'create': False}
        }
        return action
    
    task_count = fields.Integer(
        compute='_compute_task_count',
    )
    
    def _compute_task_count(self):
        for partner in self:
            partner.task_count = self.env['project.task'].search_count([
                ('partner_id', '=', partner.id)
            ])
