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
    nombre_proyecto = fields.Char(required=True, string="Nombre Proyecto",)
    # Configuración empresa
    empresa_seleccionada = fields.Many2many(string="Selección de Empresa(s)",
                    comodel_name='product.attribute.value',
                    relation="product_cliente_empresa",
                    help="Selección de Empresas asociadas a la solicitud.",
                    domain="[['attribute_id.name','ilike','Empresa']]",
                    required=True,
                    readonly=True, states={'draft': [('readonly', False)]},)
    producto_seleccionado = fields.Many2many(string="Selección de Producto(s)",
                    comodel_name='product.attribute.value',
                    relation="product_cliente_producto",
                    help="Selección de Productos asociados a la solicitud.",
                    domain="[['attribute_id.name','ilike','Producto']]",
                    required=True,
                    readonly=True, states={'draft': [('readonly', False)]},)
    sede_seleccionada = fields.Many2many(string="Selección de Sede(s)",
                    comodel_name='product.template',
                    help="Selección de Sede(s) asociadas a la solicitud.",
                    domain="[('categ_id.name','ilike','Sede')]",
                    required=True,
                    readonly=True, states={'draft': [('readonly', False)]},)
    tipo_intervencion = fields.Selection([('sede_nueva', 'Sede Nueva'),('adecuacion', 'Adecuación'),('remodelacion', 'Remodelación'),('ampliacion', 'Ampliación')],
                    readonly=True, states={'draft': [('readonly', False)]},)
    # Ocupación centro médico
    numero_usuarios = fields.Float(string="Número de Usuarios", required=True, help="Número de Usuarios",
                                   readonly=True, states={'draft': [('readonly', False)]},)
    numero_empleados = fields.Float(string="Número de Empleados", required=True, help="Número de Empleados",
                                    readonly=True, states={'draft': [('readonly', False)]},)
    terceros = fields.Float(string="Terceros", required=True, help="Terceros",
                    readonly=True, states={'draft': [('readonly', False)]},)

    # Listado de áreas asociadas en campo BoM de mrp.production
    sedes_seleccionadas = fields.Many2many(string="Selección de Sede(s)",
                    comodel_name='mrp.bom',
                    relation="bom_cliente_sedes",
                    help="Selección de Sedes asociados a la solicitud.",
                    domain="[('product_tmpl_id','=',sede_seleccionada)]",
                    required=True,
                    readonly=True, states={'draft': [('readonly', False)]},)
    # TODO: encontrar el filtro necesario por cada una de las variantes E,mpresa y Producto, por lo pronto se dejan solamente las SEDES.
    # TODO: Al momento de editar cada línea no afecte la cantidad preconfigurada
    areas_asociadas_sede = fields.Many2many(string="Selección de Áreas",
                    comodel_name='mrp.bom.line',
                    relation="x_bom_line_cliente_areas_asistenciales",
                    column1="product_id",
                    column2="product_qty",
                    help="Selección de Áreas asociadas a la(s) Sede(s) seleccionada(s).",
                    domain="['|',('parent_product_tmpl_id','in',sede_seleccionada),('product_id.attribute_line_ids.id','=',empresa_seleccionada)]",
                    required=True,
                    copy=True,
                    readonly=True, states={'draft': [('readonly', False)]},)

    # Sistema de Estados
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('confirmed', 'Confirmado'),
        ('done', 'Realizado'),
        ('cancel', 'Cancelado')], string='Estado',
        copy=False, index=True, readonly=True,
        store=True, tracking=True, compute='_compute_state', default='draft',
        help=" * Borrador: El proyecto se encuentra en edición.\n"
             " * Confirmado: El proyecto ha sido confirmado y no es editable por el cliente.\n"
             " * Realizado: El proyecto se ha ejecutado. \n"
             " * Cancelado: El proyecto ha sido cancelado.")

    @api.depends('state')
    def _compute_state(self):
        if not self.state:
            self.state = 'draft'

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
                self.areas_asociadas_sede |= area.bom_line_ids


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
        self.state = 'draft'
        _logger.critical("Validar proyecto")
        return True

    def action_confirmar_proyecto(self):
        self.state = 'confirmed'
        _logger.critical("Confirmar proyecto")
        return True


class MrpBom(models.Model):
    """ Defines bills of material for a product or a product template """
    _name = 'mrp.bom'
    _inherit = 'mrp.bom'

    # M2 Utilizados para áreas cliente, derivadas, y diseño. Cada una contempla un cálculo diferente asignado a la misma variable
    m2 = fields.Float('M2', default=1.0)
    total_m2 = fields.Float('Total', default=1.0, digits=(16, 2), readonly=True, group_operator="sum",
                            compute='_compute_total_m2',)

    @api.depends('m2','total_m2')
    def _compute_total_m2(self):
        for record in self:
            # _logger.critical(" COMPUTE TOTAL_M2 ")
            record.total_m2 = record.product_qty * record.m2

class MrpBomLine(models.Model):
    _name = 'mrp.bom.line'
    _inherit = 'mrp.bom.line'

    # M2 Utilizados para áreas cliente, derivadas, y diseño. Cada una contempla un cálculo diferente asignado a la misma variable
    m2 = fields.Float('M2', default=1.0)
    total_m2 = fields.Float('Total', default=1.0, digits=(16, 2), readonly=True, group_operator="sum",
                            compute='_compute_total_m2',)

    @api.depends('m2','total_m2')
    def _compute_total_m2(self):
        for record in self:
            # _logger.critical(" COMPUTE TOTAL_M2 ")
            record.total_m2 = record.product_qty * record.m2

# TODO: Crear campo adicional en modelo bom_line para que me permita
#  añadir la cantidad sin modificar nada de los productos asociados.
# class Area(models.Model):
#     _name = 'keralty_module.area'
#     _rec_name = "product_id"
#     _description = 'Área'
#
#     product_id = fields.Many2one('product.product', 'Área', required=True)
#     product_tmpl_id = fields.Many2one('product.template', 'Área Template', related='product_id.product_tmpl_id', readonly=False)
#     product_qty = fields.Float(
#         'Quantity', default=1.0,
#         digits='Cantidad Unidades', required=True)

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
    _description = 'Formulario Validación Técnica'
    _rec_name = 'nombre_tecnico'

    nombre_tecnico = fields.Char(required=True, string="Código Revisión")
    formulario_cliente = fields.Many2one(string="Formulario Cliente",
                                comodel_name='keralty_module.formulario.cliente',
                                help="Formulario Cliente asociado para validación técnica.")

    areas_cliente = fields.Many2many(string="Áreas Cliente",
                    comodel_name='mrp.bom.line',
                    relation="validacion_areas_cliente",
                    column1="product_id",
                    column2="product_qty",
                    help="Listado de áreas solicitadas por el cliente.",
                    #domain="['|',('parent_product_tmpl_id','in',sede_seleccionada),('product_id.attribute_line_ids.id','=',empresa_seleccionada)]",
                    required=True,
                    copy=True,)
                    #compute='_compute_areas_cliente',)
                    # readonly=True, states={'draft': [('readonly', False)]},)

    areas_derivadas = fields.Many2many(string="Áreas Derivadas",
                    comodel_name='mrp.bom',
                    relation="validacion_areas_derivadas",
                    # column1="product_id",
                    # column2="product_qty",
                    help="Listado de áreas derivadas de la solicitud del cliente.",
                    domain="[('product_tmpl_id.categ_id.name','ilike','Derivada')]",
                    #domain="['|',('parent_product_tmpl_id','in',sede_seleccionada),('product_id.attribute_line_ids.id','=',empresa_seleccionada)]",
                    required=True,
                    copy=True,)
                    #compute='_compute_areas_cliente',)
                    #readonly=True, states={'draft': [('readonly', False)]},)

    areas_diseño = fields.Many2many(string="Áreas Diseño",
                    comodel_name='mrp.bom',
                    relation="validacion_areas_diseno",
                    # column1="product_id",
                    # column2="product_qty",
                    help="Listado de áreas de diseño de la solicitud del cliente.",
                    domain="[('product_tmpl_id.categ_id.name','ilike','Diseño')]",
                    #domain="['|',('parent_product_tmpl_id','in',sede_seleccionada),('product_id.attribute_line_ids.id','=',empresa_seleccionada)]",
                    required=True,
                    copy=True,)
                    #compute='_compute_areas_cliente',)
                    #readonly=True, states={'draft': [('readonly', False)]},)

    porcentaje_pasillos = fields.Float('Porcentaje de pasillos y muros adicionales', default=30.0)
    total_m2_areas = fields.Float('Total M2 proyecto', default=1.0, digits=(16, 2), readonly=True, group_operator="sum")


    # Sistema de Estados
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('confirmed', 'Confirmado'),
        ('done', 'Realizado'),
        ('cancel', 'Cancelado')], string='Estado',
        copy=False, index=True, readonly=True,
        store=True, tracking=True, compute='_compute_state', default='draft',
        help=" * Borrador: El proyecto se encuentra en edición.\n"
             " * Confirmado: El proyecto ha sido confirmado y no es editable por el cliente.\n"
             " * Realizado: El proyecto se ha ejecutado. \n"
             " * Cancelado: El proyecto ha sido cancelado.")


    '''
        Copia LdM
        Cuando cambia la sede seleccionada copia la lista de materiales (LdM) de la Sede (product)
        y la muestra en el campo areas_asociadas_sede     
    '''
    @api.onchange('formulario_cliente')
    def _onchange_formulario_cliente(self):
        res = {}
        objetoBusqueda = None
        _logger.critical(self.formulario_cliente.areas_asociadas_sede)
        if self.formulario_cliente.areas_asociadas_sede:
            self.areas_cliente = self.formulario_cliente.areas_asociadas_sede

        warning = {
            'title': "Sede Seleccionada PRINT: {}".format(
                self.areas_cliente
            ),
            'message': "objeto búsqueda: {}".format(
                objetoBusqueda
            ),
        }
        res.update({'warning': warning})


    def action_realizar(self):
        self.state = 'done'
        _logger.critical("Realizar proyecto")
        return True

    def action_calcular_areas(self):
        _logger.critical("Calcular Áreas")
        self.total_m2_areas = 0
        '''
            TODO: 
                PRE: 
                    Crear campos M2 Parametrizados y Total para áreas cliente
                                  M2 Calculados y Total para áreas derivadas
                                  M2 Sugeridos y Total para áreas de diseño
                                  Porcentaje de pasillos y muros adicionales
                                  Total para Formulario de Validación Técnica que realice la sumatoria de cada sección de áreas...
                ÁREAS CLIENTE                                  
                    1 Consultar M2 asociados a un área seleccionada (producto)
                    2 Calcular el total de metros cuadrados para área cliente utilizando el valor consultado
                ÁREAS DERIVADAS
                    1 Consultar la fórmula para el área derivada seleccionada desde el formulario de parametrización de cálculos
                    2 Calcular el total m2 del área derivada utilizando la fórmula consultada.
                ÁREAS DISEÑO
                    1 Consultar M2 asociados a un área de diseño o dejar campo en blanco
                    2 Calcular el total de M2 utilizando el valor ingresado/consultado
                
                CÁLCULO TOTAL DE ÁREAS (SUMATORIA) y porcentaje pasillos.
                    Mostrar total
                
                POST: 
                    Crear restricción en edición para cammpos M2 y Total para las áreas de cliente y las áreas derivadas (validar)
            
        '''
        for area_ciente in self.areas_cliente:
            # _logger.warning(area_ciente.product_id.name)
            for child_bom in area_ciente.child_line_ids:
                _logger.critical(child_bom.product_id.name)
                # str.find("soccer")
                # TODO: Validar que la variante sea la misma del área seleccionada para traer el valor de M2 correcto.
                if "Área" in child_bom.product_id.name:
                    # _logger.critical(child_bom.product_qty)
                    area_ciente.m2 = child_bom.product_qty
                    self.total_m2_areas += area_ciente.m2 * area_ciente.product_qty # child_bom.total_m2
                    _logger.critical("ÁREAS CLIENTES -> TOTAL_M2: " + str(self.total_m2_areas))

                    # _logger.critical(" CALC TOTAL_M2 ")
                    # area_ciente.total_m2 = area_ciente.product_qty * area_ciente.m2

        for area_derivada in self.areas_derivadas:
            _logger.warning(area_derivada.display_name)
            for bom_line in area_derivada.bom_line_ids:
                # _logger.critical(bom_line.product_id.name)
                # for child_bom in bom_line.child_line_ids:
                # _logger.critical(child_bom.product_id.name)
                # str.find("soccer")
                # TODO: Validar que la variante sea la misma del área seleccionada para traer el valor de M2 correcto.
                if "Área" in bom_line.product_id.name:
                    # _logger.critical(child_bom.product_qty)
                    area_derivada.m2 = bom_line.product_qty
                    self.total_m2_areas += area_derivada.m2 * area_derivada.product_qty # bom_line.total_m2
                    _logger.critical("ÁREAS DERIVADAS -> TOTAL_M2: " + str(self.total_m2_areas))

            # Consultar si el área derivada tiene formulación creada
            encuentra_formula_area = self.env['keralty_module.calculos'].search([('area_derivada.name', '=', area_derivada.display_name)], order='id asc')
            _logger.critical(encuentra_formula_area.formula_aritmetica)

            if encuentra_formula_area.variable_derivada == 'cantidad':
                # Para calcular la cantidad se debe utilizar la fórmula aritmética configurada
                # Si se utiliza la fuente de criterio = formulario debo extraer el área o campo independiente
                if encuentra_formula_area.fuente_criterio == 'formulario':
                    # _logger.critical(" FORMULA ES FORMULARIO ")
                    if encuentra_formula_area.area_criterio_independiente:
                        # _logger.critical(" TIENE ÁREA COMO CRITERIO INDEPENDIENTE ")
                        for areas_formulario in self.areas_cliente:
                            _logger.critical(areas_formulario)
                            if encuentra_formula_area.area_criterio_independiente.name in areas_formulario.product_id.name:
                                # _logger.critical(" ENCUENTRA ÁREA CRITERIO ")
                                # TODO: Utilizar formula configurada
                                area_derivada.product_qty = areas_formulario.product_qty / 7
                                # self.total_m2_areas += areas_formulario.total_m2

                                _logger.critical("ÁREAS DERIVADAS FORMULAS -> TOTAL_M2: " + str(self.total_m2_areas))

                    # TODO: Consultar valor del campo_criterio y asignarlo
                    # if encuentra_formula_area.campo_criterio_independiente:
                        # self.formulario_cliente
                    # area_derivada.product_qty = 9999
                    # ecuentra_formula_area.formula_aritmetica
                    #
                    # _logger.critical(" CALC TOTAL_M2 ")
                    # area_ciente.total_m2 = area_derivada.product_qty * area_ciente.m2

        for area_diseño in self.areas_diseño:
            # _logger.warning(area_derivada.bom_line_ids)
            for bom_line in area_diseño.bom_line_ids:
                # _logger.critical(bom_line.product_id.name)
                # for child_bom in bom_line.child_line_ids:
                # _logger.critical(child_bom.product_id.name)
                # str.find("soccer")
                # TODO: Validar que la variante sea la misma del área seleccionada para traer el valor de M2 correcto.
                if "Área" in bom_line.product_id.name:
                    # _logger.critical(child_bom.product_qty)
                    area_diseño.m2 = bom_line.product_qty
                    self.total_m2_areas += area_diseño.m2 * area_diseño.product_qty # bom_line.total_m2
                    _logger.critical("ÁREAS DISEÑO -> TOTAL_M2: " + str(self.total_m2_areas))

                    # _logger.critical(" CALC TOTAL_M2 ")
                    # area_ciente.total_m2 = area_derivada.product_qty * area_ciente.m2

        # TODO: Utilizar valor de pasillos...
        # self.total_m2_areas =
        return True

    @api.depends('areas_cliente','areas_derivadas','areas_diseño')
    def _compute_areas_cliente(self):

        for line in self:
            line.areas_cliente = line.areas_cliente

            line.areas_derivadas = line.areas_derivadas
            line.areas_diseño = line.areas_diseño
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
                    domain="[('model_id.model', 'ilike', 'formulario.cliente')]")
    variable_criterio = fields.Selection([('area', 'Área'),('cantidad', 'Cantidad')])
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
