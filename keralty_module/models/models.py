# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)
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
    empresa_seleccionada = fields.Many2many(string="Selección de Empresa(s)",
                    comodel_name='product.attribute.value',
                    relation="product_cliente_empresa",
                    help="Selección de Empresas asociadas a la solicitud.",
                    domain="[['attribute_id.name','ilike','Empresa']]",
                    required=True)
    producto_seleccionado = fields.Many2many(string="Selección de Producto(s)",
                    comodel_name='product.attribute.value',
                    relation="product_cliente_producto",
                    help="Selección de Productos asociados a la solicitud.",
                    domain="[['attribute_id.name','ilike','Producto']]",
                    required=True)
    sede_seleccionada = fields.Many2many(string="Selección de Sede(s)",
                    comodel_name='product.template',
                    help="Selección de Sede(s) asociadas a la solicitud.",
                    domain="[('categ_id.name','ilike','Sede')]",
                    required=True)
    tipo_intervencion = fields.Selection([('sede_nueva', 'Sede Nueva'),('adecuacion', 'Adecuación'),('remodelacion', 'Remodelación'),('ampliacion', 'Ampliación')])
    # Ocupación centro médico
    numero_usuarios = fields.Float(string="Número de Usuarios", required=True, help="Número de Usuarios")
    numero_empleados = fields.Float(string="Número de Empleados", required=True, help="Número de Empleados")
    terceros = fields.Float(string="Terceros", required=True, help="Terceros")

    # Listado de áreas asociadas en campo BoM de mrp.production
    sedes_seleccionadas = fields.Many2many(string="Selección de Sede(s)",
                    comodel_name='mrp.bom',
                    relation="bom_cliente_sedes",
                    help="Selección de Sedes asociados a la solicitud.",
                    domain="[('product_tmpl_id','=',sede_seleccionada)]",
                    required=True)
    # TODO: encontrar el filtro necesario por cada una de las variantes E,mpresa y Producto, por lo pronto se dejan solamente las SEDES.
    # TODO: Al momento de editar cada línea no afecte la cantidad preconfigurada
    areas_asociadas_sede = fields.Many2many(string="Selección de Áreas",
                    comodel_name='mrp.bom.line',
                    relation="bom_line_cliente_areas_asistenciales",
                    column1="product_id",
                    column2="product_qty",
                    help="Selección de Áreas asociadas a la(s) Sede(s) seleccionada(s).",
                    domain="['|',('parent_product_tmpl_id','in',sede_seleccionada),('product_id.attribute_line_ids.id','=',empresa_seleccionada)]",
                    required=True,
                    copy=False)

    # Sistema de Estados
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('confirmed', 'Confirmado'),
        ('done', 'Hecho'),
        ('cancel', 'Cancelado')], string='Estado',
        copy=False, index=True, readonly=True,
        store=True, tracking=True,
        help=" * Borrador: El poryecto se encuentra en edición.\n"
             " * Confirmado: El proyecto ha sido confirmado y no es editable por el cliente.\n"
             " * Hecho: El proyecto se ha ejecutado. \n"
             " * Cancelado: El proyecto ha sido cancelado.")

    #
    '''
        Copia LdM
        Cuando cambia la sede seleccionada copia la lista de materiales (LdM) de la Sede (product)
        y la muestra en el campo areas_asociadas_sede     
    '''
    @api.onchange('sede_seleccionada')
    def _onchange_sede_seleccionada(self):
        res = {}
        objetoBusqueda = None
        self.areas_asociadas_sede = None

        for sede_product_template in self.sede_seleccionada:
            for area in sede_product_template.bom_ids:
                _logger.critical("área: ")
                _logger.critical(area)
                _logger.critical(area.product_tmpl_id.name)
                _logger.critical(area.product_qty)
                for linea_bom in area.bom_line_ids:
                    _logger.critical("------------- BOM LINE -----------")
                    _logger.warning(linea_bom.product_tmpl_id.name)
                    _logger.warning(linea_bom.product_qty)
                    # _logger.warning("template product: " + str(type(linea_bom.product_tmpl_id)))
                    # _logger.warning("template product: " + str(type(self.areas_asociadas_sede.product_tmpl_id)))
                    # _logger.warning("product_id: " + str(type(linea_bom.product_id)))
                    # _logger.warning("product_id: " + str(type(self.areas_asociadas_sede.product_id)))
                    # _logger.warning("product_qty: " + str(type(linea_bom.product_qty)))

                    #self.areas_asociadas_sede += self.env['mrp.bom.line'].create(linea_bom)
                    #producto_duplicado =
                    # self.areas_asociadas_sede += self.env['mrp.bom.line'].create(
                    #         {
                    #             'product_tmpl_id': linea_bom.product_tmpl_id,
                    #             'product_id': linea_bom.product_id,
                    #             'product_qty': linea_bom.product_qty,
                    #         }
                    #     )
                #self.areas_asociadas_sede += area.bom_line_ids
                self.areas_asociadas_sede |= area.bom_line_ids
                #self.areas_asociadas_sede = [(0,0,area.bom_line_ids)]
                #self.areas_asociadas_sede = [(4,id,area.bom_line_ids)]
                #self.areas_asociadas_sede = [(6,0,area.bom_line_ids)]
                    #self.areas_asociadas_sede = (0,0,linea_bom)
                #self.areas_asociadas_sede = vals['area.bom_line_ids'][0][2]
                #self.areas_asociadas_sede = vals['area.bom_line_ids'][0][2]


        for linea_bom in self.areas_asociadas_sede:
            linea_bom.product_qty = 1

        warning = {
            'title': "Sede Seleccionada PRINT: {}".format(
                self.sedes_seleccionadas
            ),
            'message': "objeto búsqueda: {}".format(
                objetoBusqueda
            ),
        }
        res.update({'warning': warning})


    def action_validar_proyecto(self):
        self.state = 'confirmed'
        _logger.critical("Validar proyecto")
        return True

    def action_confirmar_proyecto(self):
        self.state = 'draft'
        _logger.critical("Confirmar proyecto")
        return True


# TODO: Crear campo adicional en modelo bom_line para que me permita
#  añadir la cantidad sin modificar nada de los productos asociados.

# class MrpBomLineK(models.Model):
#     _name = 'keralty_module.bom_line'
#     _rec_name = "product_id"
#     _description = 'Bill of Material Line Keralty'
#
#     product_id = fields.Many2one( 'product.product', 'Área', required=True, check_company=True)
#     product_tmpl_id = fields.Many2one('product.template', 'Product Template', related='product_id.product_tmpl_id', readonly=False)
#     product_qty = fields.Float(
#         'Quantity', default=1.0,
#         digits='Product Unit of Measure', required=True)
#     company_id = fields.Many2one(
#         related='bom_id.company_id', store=True, index=True, readonly=True)
#     bom_id = fields.Many2one(
#         'mrp.bom', 'Parent BoM',
#         index=True, ondelete='cascade', required=True)
#     parent_product_tmpl_id = fields.Many2one('product.template', 'Parent Product Template', related='bom_id.product_tmpl_id')


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
