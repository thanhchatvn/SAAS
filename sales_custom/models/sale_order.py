# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def _action_confirm(self):
        res = super(SaleOrder, self)._action_confirm()
        self.partner_id.customer = True
        self.partner_id.prospect = False
        sales_stage_ids = self.opportunity_id.stage_id.search([('stage', '=', 'won')]).ids
        if sales_stage_ids:
            self.opportunity_id.stage_id = sales_stage_ids[0]
        for rec in self:
            print("opportunity11111",rec.opportunity_id)
            if rec.opportunity_id:
                print("opportunity")
                rec.opportunity_id.write({'stage': 'won'})

        return res

