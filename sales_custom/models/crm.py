from odoo import api, fields, models, _
from odoo.exceptions import UserError, AccessError, ValidationError


class Stage(models.Model):
    _inherit = 'crm.stage'

    stage = fields.Selection(string="Stage",
                             selection=[('offer', 'Offer'), ('won', 'Won'), ('lost', 'Lost'), ('other', 'Other'), ])


class Lead(models.Model):
    _inherit = 'crm.lead'

    prospect = fields.Boolean(string="Is a Prospect", default=True, readonly=True)
    industry_id = fields.Many2one('res.partner.industry', 'Sector', related='partner_id.industry_id',store=True, track_visibility='onchange')
    team_id = fields.Many2one('crm.team', string='Sales Team', oldname='section_id',
                              default=lambda self: self.env['crm.team'].sudo()._get_default_team_id(
                                  user_id=self.env.uid),
                              index=True, track_visibility='onchange',
                              help='When sending mails, the default email address is taken from the Sales Team.')
    template_id = fields.Many2one('sale.order.template', 'Service',track_visibility='onchange', )
    lead_id = fields.Many2one('sale.order')
    #service and sector for lead
    template = fields.Many2one('sale.order.template', 'Service', track_visibility='onchange', )
    sector = fields.Many2one('res.partner.industry', 'Sector',  store=True,
                                  track_visibility='onchange')




    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if not self.partner_id.prospect:
            self.prospect = False
        else:
            self.prospect = True

    @api.multi
    def action_new_quotation(self):
        self.ensure_one()
        sale_order_obj = self.env['sale.order']
        sale_order_line_obj = self.env['sale.order.line']
        if not self.partner_id:
            raise UserError(_('Please select customer for this opportunity.'))
        so_id = sale_order_obj.create({'partner_id': self.partner_id.id,
                                       'team_id': self.team_id.id,
                                       'campaign_id': self.campaign_id.id,
                                       'medium_id': self.medium_id.id,
                                       'source_id': self.source_id.id,
                                       'sale_order_template_id': self.template_id.id,
                                       'opportunity_id': self.id,
                                       })

        so_id.onchange_sale_order_template_id()
        so_id.state = 'draft'

        offer_stage_ids = self.stage_id.search([('stage', '=', 'offer')]).ids
        if offer_stage_ids:
            self.stage_id = offer_stage_ids[0]
        return {'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'sale.order',
                'res_id': so_id.id,
                }

    @api.constrains('stage_id', 'order_ids')
    def _check_quotation(self):
        if self.sale_number == 0 and self.stage_id.stage == 'offer' and not self.zip:
            raise ValidationError(_("You have to Create Quotation First!"))
        #if self.sale_number == 0 or self.sale_number != 0 and self.stage_id.stage == 'won' and self.order_ids.state != 'sale':
            #raise ValidationError(_("You have to Create Quotation First And Confirmed To Quotation!"))

