from openerp.addons.builder.models.fields import snake_case
from openerp import models, fields, api, _
from .base import FIELD_WIDGETS_ALL

__author__ = 'one'


class GanttView(models.Model):
    _name = 'builder.views.gantt'

    _inherit = ['ir.mixin.polymorphism.subclass', 'builder.views.abstract']

    _inherits = {
        'builder.ir.ui.view': 'view_id'
    }

    view_id = fields.Many2one('builder.ir.ui.view', string='View', required=True, ondelete='cascade')
    attr_create = fields.Boolean('Allow Create', default=True)
    attr_edit = fields.Boolean('Allow Edit', default=True)
    attr_delete = fields.Boolean('Allow Delete', default=True)
    attr_date_start_field_id = fields.Many2one('builder.ir.model.fields', 'Date Start Field', ondelete='set null', required=True)
    attr_date_stop_field_id = fields.Many2one('builder.ir.model.fields', 'Date Stop Field', ondelete='set null')
    attr_date_delay_field_id = fields.Many2one('builder.ir.model.fields', 'Date Delay Field', ondelete='set null')
    attr_progress_field_id = fields.Many2one('builder.ir.model.fields', 'Progress Field', ondelete='set null')
    attr_default_group_by_field_id = fields.Many2one('builder.ir.model.fields', 'Default Group By Field', ondelete='set null')


    field_ids = fields.One2many('builder.views.gantt.field', 'view_id', 'Items')

    _defaults = {
        'type': 'gantt',
        'custom_arch': False,
        'subclass_model': lambda s, c, u, cxt=None: s._name,
    }

    @api.onchange('model_id')
    def _onchange_model_id(self):
        self.name = self.model_id.name
        self.xml_id = "view_{snake}_gantt".format(snake = snake_case(self.model_id.model))

    @api.onchange('custom_arch', 'attr_create', 'attr_edit', 'attr_delete', 'attr_date_start_field_id', 'attr_date_stop_field_id', 'attr_date_delay_field_id', 'attr_progress_field_id', 'attr_default_group_by_field_id', 'name')
    def _onchange_generate_arch(self):
        self.arch = self._get_view_arch()

    @api.multi
    def _get_view_arch(self):
        if self.custom_arch:
            return self.arch
        else:
            template_obj = self.env['document.template']
            return template_obj.render_template('builder.view_arch_gantt.xml', {
                'this': self,
                'string': self.name,
                'create': self.attr_create,
                'edit': self.attr_edit,
                'delete': self.attr_delete,
                'date_start': self.attr_date_start_field_id and self.attr_date_start_field_id.name or False,
                'date_stop': self.attr_date_stop_field_id and self.attr_date_stop_field_id.name or False,
                'date_delay': self.attr_date_delay_field_id and self.attr_date_delay_field_id.name or False,
                'progress': self.attr_progress_field_id and self.attr_progress_field_id.name or False,
                'default_group_by': self.attr_default_group_by_field_id and self.attr_default_group_by_field_id.name or False,
            })


class GanttField(models.Model):
    _name = 'builder.views.gantt.field'
    _inherit = 'builder.views.abstract.field'

    view_id = fields.Many2one('builder.views.gantt', string='View', ondelete='cascade')
    