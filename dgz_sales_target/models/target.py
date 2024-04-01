from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Target(models.Model):
    _name = 'target.user'
    _inherit = ['mail.thread']

    user_name = fields.Many2one('res.users', string="User", tracking=True)
    target = fields.Monetary("Target", currency_field='currency_id', tracking=True)
    start_date = fields.Date("Start Date", tracking=True)
    end_date = fields.Date("End Date")
    achieved_target = fields.Monetary("Achieved Target", compute='_compute_calculate_target',
                                      currency_field='currency_id', tracking=True)
    currency_id = fields.Many2one('res.currency', "Currency", tracking=True,
                                  default=lambda self: self.env.company.currency_id)
    name = fields.Char(compute='_compute_name', store=True)

    @api.depends('user_name', 'start_date', 'end_date')
    def _compute_name(self):
        for record in self:
            if record.user_name and record.start_date and record.end_date:
                record.name = f"{record.user_name.name}'s Target ({record.start_date} - {record.end_date})"
            else:
                record.name = "New"

    @api.depends('user_name', 'start_date', 'end_date','target_status')
    def _compute_calculate_target(self):
        for record in self:
            data = self.env['account.move'].search([
                ('invoice_user_id', '=', record.user_name.id),
                ('payment_state', 'in', ['paid', 'partial']),
                ('invoice_date', '>=', record.start_date),
                ('invoice_date', '<=', record.end_date)
            ])
            total_signed = sum(invoiced.amount_total_signed for invoiced in data)
            record.achieved_target = total_signed
        self._compute_target_status()

    @api.constrains('user_name', 'start_date', 'end_date')
    def _check_unique_target_per_month(self):
        for record in self:
            if record.user_name and record.start_date and record.end_date:
                existing_targets = self.search([
                    ('user_name', '=', record.user_name.id),
                    ('start_date', '<=', record.end_date),
                    ('end_date', '>=', record.start_date),
                    ('id', '!=', record.id),
                ])
                if existing_targets:
                    raise ValidationError("Only one target can be assigned for a person for this month.")

    @api.constrains('target')
    def _check_positive_target(self):
        for record in self:
            if record.target <= 0:
                raise ValidationError("Target amount must be greater than zero.")

    target_status = fields.Selection([
        ('red', 'Not Achieved'),
        ('orange', 'Partially Achieved'),
        ('green', 'Achieved')
    ], compute='_compute_target_status', string='Target Status', store=True)

    @api.depends('achieved_target', 'target')
    def _compute_target_status(self):
        for record in self:
            if record.target == 0:
                record.target_status = 'red'
            else:
                percentage_achieved = (record.achieved_target / record.target) * 100
                if percentage_achieved < 100:
                    if percentage_achieved <= 50:
                        record.target_status = 'red'
                    else:
                        record.target_status = 'orange'
                else:
                    record.target_status = 'green'

