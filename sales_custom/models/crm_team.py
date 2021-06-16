# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Team(models.Model):
    _inherit = 'crm.team'

    allow_member = fields.Many2many('res.users', string='Allowed Members')

