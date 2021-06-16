from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    #user_industry_id = fields.Many2one('res.partner.industry', 'Industry', )
    prospect = fields.Boolean(string="Is a Prospect")
    sale_team_id = fields.Many2one("crm.team", string="Sales Team", related='user_id.sale_team_id', readonly=True,
                                   required=False)
    user_id = fields.Many2one('res.users', string='KAM', index=True, track_visibility='onchange', track_sequence=2,
                              default=lambda self: self.env.user,)

    industry_id = fields.Many2one('res.partner.industry', 'Industry')

    @api.onchange('user_id')
    def onchange_kam(self):
       industury_ids= self.industry_id.search([('sales_person','=',self.user_id.id)])
       self.industry_id=industury_ids and industury_ids[0] or False


class ResPartnerIndustry(models.Model):
    _inherit = 'res.partner.industry'

    sales_person = fields.Many2many('res.users', string='KAM')
    #sales_person = fields.Boolean('User')



# class Users(models.Model):
#     _inherit = 'res.users'
#
#     industry_id = fields.Many2one('res.partner.industry', 'Industry',)

