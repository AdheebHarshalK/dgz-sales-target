from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models


class loginpage(models.Model):
    _name = 'custom.login'

    image = fields.Binary(string="Image", compute='_compute_user_image', store=True)
    user_name = fields.Char("Name")
    target_amount = fields.Monetary("Target Amount", currency_field='currency_id')
    start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")
    target_achieved_amount = fields.Monetary("Achieved Amount", currency_field='currency_id')
    bool = fields.Boolean("Check visibility", default=True)
    currency_id = fields.Many2one('res.currency', "Currency", default=lambda self: self.env.company.currency_id)

    @api.depends('user_name')
    def _compute_user_image(self):
        for record in self:
            user = self.env.user.partner_id
            record.image = user.image_1920 if user else False

    @api.onchange('user_name', 'target_amount', 'start_date', 'end_date', 'target_achieved_amount', 'currency_id')
    def update_character_field(self):
        data = self.env['account.move'].search([])
        user_id = self.env.user
        current_date = fields.Date.today()
        start_of_month = current_date.replace(day=1)
        end_of_month = (start_of_month + relativedelta(months=1, days=-1))

        activity = self.env['target.user'].search([
            ('user_name', '=', user_id.id),
            ('start_date', '>=', start_of_month),
            ('end_date', '<=', end_of_month)
        ])

        if activity:
            self.user_name = activity.user_name.name
            self.target_amount = activity.target
            self.start_date = activity.start_date
            self.end_date = activity.end_date
            self.target_achieved_amount = activity.achieved_target
        else:
            self.user_name = user_id.name
            self.bool = False

    @api.model
    def get_user_details(self):
        user_id = self.env.user
        current_date = fields.Date.today()
        start_of_month = current_date.replace(day=1)
        end_of_month = (start_of_month + relativedelta(months=1, days=-1))

        activity = self.env['target.user'].search([
            ('user_name', '=', user_id.id),
            ('start_date', '>=', start_of_month),
            ('end_date', '<=', end_of_month)
        ])

        if activity:
            target_count = len(activity)
            return {
                'user_name': activity.user_name.name,
                'target_amount': activity.target,
                'start_date': activity.start_date,
                'end_date': activity.end_date,
                'target_achieved_amount': activity.achieved_target,
                'target_count': target_count,
            }
        return {}
