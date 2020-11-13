# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class FormularioParametrizacion(models.Model):
#     _name = 'keralty_module.formulario.param'
#     _description = 'Formulario Parametrización'
#
#     nombre_codigo = fields.Char(required=True, string="Nombre o Código")
#     casilleros = fields.Float(string="Área de casilleros para funcionarios", required=True, help="Area de casilleros para funcionarios", digits=(8, 2))
#     banios_hombres = fields.Float(string="Baños públicos hombres", required=True, help="Baños públicos hombres", digits=(8, 2))
#     banios_mujeres = fields.Float(string="Baños públicos mujeres", required=True, help="Baños públicos mujeres", digits=(8, 2))
#     banios_hombres_disc = fields.Float(string="Baños públicos hombres en condición de discapacidad.", required=True, help="Baños publícos hombres en condición de discapacidad", digits=(8, 2))
#     banios_mujeres_disc = fields.Float(string="Baños públicos mujeres en condición de discapacidad", required=True, help="Baños públicos mujeres en condición de discapacidad", digits=(8, 2))
#     cafeteria_empleados = fields.Float(string="Cafeteria empleados", required=True, help="Cafeteria empleados", digits=(8, 2))
#     cuarto_aseo = fields.Float(string="Cuarto de aseo (poceta)", required=True, help="Cuarto de aseo (poceta)", digits=(8, 2))
#     banios_hombres_emp = fields.Float(string="Baño hombres para empleados", required=True, help="Baño hombres para empleados", digits=(8, 2))
#     banios_mujeres_emp = fields.Float(string="Baño mujeres para empleados", required=True, help="Baño mujeres para empleados", digits=(8, 2))
#     # Laboratorio
#     banios_hombres_lab = fields.Float(string="Baños públicos hombres laboratorio", required=True, help="Baños públicos hombres laboratorio", digits=(8, 2))
#     banios_mujeres_lab = fields.Float(string="Baños públicos mujeres laboratorio", required=True, help="Baños públicos mujeres laboratorio", digits=(8, 2))
#     banios_hombres_lab_disc = fields.Float(string="Baños públicos hombres en condición de discapacidad laboratorio", required=True, help="Baños públicos hombres en condición de discapacidad laboratorio", digits=(8, 2))
#     banios_mujeres_lab_disc = fields.Float(string="Baños públicos mujeres en condición de discapacidad laboratorio", required=True, help="Baños públicos mujeres en condición de discapacidad laboratorio", digits=(8, 2))
#     banio_mixto = fields.Float(string="Baño mixto para empleados", required=True, help="Baño mixto para empleados", digits=(8, 2))
#     vestier = fields.Float(string="Vestier con casilleros mixto para empleados", required=True, help="Vestier con casilleros mixto para empleados", digits=(8, 2))
#     oficina_admon = fields.Float(string="Oficina coordinación adminsitrativa", required=True, help="Oficina coordinación adminsitrativa", digits=(8, 2))
#
#     #     value = fields.Integer()

class StockMove(models.Model):
    _inherit = 'stock.move'

    listado_areas_cliente = fields.Many2one(
        'keralty_module.formulario.cliente', 'Listado de Áreas', check_company=True)

class FormularioCliente(models.Model):
    _name = 'keralty_module.formulario.cliente'
    _description = 'Formulario Cliente'
    _rec_name = 'nombre_proyecto'

    #
    nombre_proyecto = fields.Char(required=True, string="Nombre Proyecto")
    # Configuración empresa
    sede = fields.Many2many(string="Sedes", comodel_name='keralty_module.sede',
                    help="Sedes asociadas")
    # Ocupación centro médico
    numero_usuarios = fields.Float(string="Número de Usuarios", required=True, help="Número de Usuarios")
    numero_empleados = fields.Float(string="Número de Empleados", required=True, help="Número de Empleados")
    terceros = fields.Float(string="Terceros", required=True, help="Terceros")

    # Listado de áreas asociadas en campo BoM de mrp.production
    #move_raw_ids = fields.Many2many('product.template')


    def action_confirmar_proyecto(self):
        print("Confirmar proyecto")
        return True






class FormularioValidacion(models.Model):
    _name = 'keralty_module.formulario.validacion'
    _description = 'Formulario Validacion'
    _rec_name = 'nombre_tecnico'

    nombre_tecnico = fields.Char(required=True, string="Nombre Proyecto")
    descripcion = fields.Char(required=True, string="Descripcion")
    formulario_cliente = fields.Many2one(string="Formulario Cliente", comodel_name='keralty_module.formulario.cliente',
                    help="Formulario Cliente asociado para validacion tecnica.")

# hereda de producto y añade campo para relación con Categoría
# class ProductProduct(models.Model):
#     _inherit = 'product.product'
#     categorias_ids = fields.Char(required=True, string="Categorias")
#     #categoria_ids = fields.Many2one(string="Categorías", comodel_name='keralty_module.categoria',
#     #                                help='Categorías asociadas al producto.')

class Categoria(models.Model):
    _name = 'keralty_module.categoria'
    _description = 'Categoria'

    formulario_cliente = fields.Many2one(string="Formulario Cliente", comodel_name='keralty_module.formulario.cliente',
                    help="Formulario Cliente asociado para validacion tecnica.")
    #productos_asociados = fields.One2many('product.TEMPLATE', 'categoria_ids', 'Productos Asociados')

class Sede(models.Model):
    _name = 'keralty_module.sede'
    _description = 'Sedes'
    _rec_name = 'nombre'

    nombre = fields.Char(required=True, string="Nombre Sede")
    descripcion = fields.Char(required=True, string="Descripción")

# Parametrización de Cálculos
class Calculos(models.Model):
    _name = 'keralty_module.calculos'
    _description = 'Parametrización de Cálculos'
    #_rec_name = 'nombre'

    # Restricción Cálculo Único
    _sql_constraints = [('unique_calculo', 'unique(empresa, area_derivada, variable_derivada)',
                         'Empresa, área derivada y variable derivada ya configuradas previamente!\nPor favor, verifique la información.')]

    empresa = fields.Many2one(string="Empresa", comodel_name='res.company',
                    help="Empresa asociada al cálculo.", required=True)
    area_derivada = fields.Many2one(string="Área Derivada", comodel_name='product.template',
                    help="Área Derivada asociada al cálculo.",
                    domain="[('categ_id.name','ilike','Derivada')]",
                    required=True)
    variable_derivada = fields.Selection([('area', 'Área'),('cantidad', 'Cantidad')])
    fuente_criterio = fields.Selection([('predeterminado', 'Valor Predeterminado'),('formulario', 'Formulario de Cliente')])
    area_criterio_independiente = fields.Many2one(string="Área como criterio independiente", comodel_name='product.template',
                    help="Criterio a utilizar en el cálculo.",
                    domain="[('categ_id.name','ilike','Cliente')]")
    campo_criterio_independiente = fields.Many2one(string="Campo como criterio independiente", comodel_name='ir.model.fields',
                    help="Criterio a utilizar en el cálculo.",
                    domain="[('model_id.model', 'ilike', 'formulario.cliente'), ('readonly', '=', False)]")
    variable_criterio = fields.Selection([('predeterminado', 'Valor Predeterminado'),('formulario', 'Formulario de Cliente')])
    formula_aritmetica = fields.Char(required=True, string="Fórmula")

    @api.onchange('fuente_criterio')
    def _onchange_fuente_criterio(self):
        res = {}
        if self.fuente_criterio == "predeterminado":
            self.area_criterio_independiente = None
            self.campo_criterio_independiente = None
            self.variable_criterio = None

    @api.onchange('formula_aritmetica')
    def _onchange_formula_aritmetica(self):
        res = {}
        if self.fuente_criterio == "formulario":
            if self.area_criterio_independiente.name:
                if not ('"' + self.area_criterio_independiente.name + '"' in self.formula_aritmetica):
                    warning = {
                        'title': "Error validación en la fórmula: {}".format(
                            self.formula_aritmetica
                        ),
                        'message': "La fórmula aritmética debe contener entre comillas dobles el nombre del criterio independiente: \"{}\" ".format(
                            self.area_criterio_independiente.name
                        ),
                    }
                    self.formula_aritmetica = ""
                    res.update({'warning': warning})
            if self.campo_criterio_independiente.name:
                if not ('"' + self.campo_criterio_independiente.field_description + '"' in self.formula_aritmetica):
                    warning = {
                        'title': "Error validación en la fórmula: {}".format(
                            self.formula_aritmetica
                        ),
                        'message': "La fórmula aritmética debe contener entre comillas dobles el nombre del criterio independiente: \"{}\" ".format(
                            self.campo_criterio_independiente.field_description
                        ),
                        #'type': 'notification',
                    }
                    self.formula_aritmetica = ""
                    res.update({'warning': warning})

            if not (self.area_criterio_independiente.name or self.campo_criterio_independiente.field_description):
                warning = {
                    'title': "Error validación en la fórmula: {}".format(
                        self.formula_aritmetica
                    ),
                    'message': "Debe seleccionar un criterio independiente, Área o Campo para la fuente de criterio: \"{}\" ".format(
                        dict(self._fields['fuente_criterio'].selection).get(self.fuente_criterio)
                    ),
                    # 'type': 'notification',
                }
                res.update({'warning': warning})
        return res

    def name_get(self):
        result = []
        for s in self:
            name = s.area_derivada.name + ' - (' + dict(s._fields['variable_derivada'].selection).get(s.variable_derivada) + ')'
            result.append((s.id, name))
        return result

# class keralty_module(models.Model):
#     _name = 'keralty_module.keralty_module'
#     _description = 'keralty_module.keralty_module'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Char(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = Char(record.value) / 100
