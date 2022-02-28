# menu item

- every menu item needs action and view:
- action example:

```
    <record id="search_appointment_action" model="ir.actions.act_window">
        <field name="name">search appointment</field>
        <field name="type">ir.actions.act_window</field>
        <field name="res_model">search.appointment.wizard</field>
        <field name="view_mode">form</field>
        <field name="view_id" ref="search_appointment_form"/>
        <field name="target">new</field>
    </record>

```

res.model: the model which we will use it to get data

view example :

```
   <record id="search_appointment_form" model="ir.ui.view">
        <field name="name">search.appointment_wizard</field>
        <field name="model">search.appointment.wizard</field>
        <field name="arch" type="xml">
            <form string="Show Appointment ">
                <group class="oe_title">

                    <field name="patient_id"/>

                </group>
                <footer>

                    <button name="view_appointments_action" type="object" string="view appointment"
                            class="btn-primary"/>
                    <button string="Cancel" class="btn-secondary" special="cancel"/>

                </footer>
            </form>
        </field>
    </record>

```

- when using button in view we need to define a method in our model.
- we need to add access right
- add the file in manifest.py

----

### Add Buttons In List View Header in Odoo 37:

- `confirm ='are you sure ?''` attr. that show confirmation msg with `name="action_confirm"`
- name : method name in model.
- to get view name from dev.tools->Edit View list
- in tree view we don't need to set id for button

----

### add image field and show it /38 .

in models :

`image=fields.Binary(string='patient name')'`

in XML :

` <field name="image" widget="image"  class="oe_avatar"/> `

----

### add sample data /39

- add `sample='1'` in tree or kanban tag

----

### show optional field /40:

- add `optional="show"` to field that we want to show. or `optional='hide'` it will be by default hidden.

----

### use _rec_name 41

to reference a name of model in many2one field.

`_rec_name = 'field_name'`


----

### order attr. in odoo 42

- it's by default asc , we can add it in our **model** we can add many args
- syntax -> `_order='field desc'`
- `_order="id desc , name "`
- we can add `default_order="id desc"` as an attr. in kanban view.
- `store=True` attr. to field to store related field in DB.

----
_wed 23-2-2022_

### Enable Mass Editing 43

- in tree view `multi_edit='1'`

---

### Notebook and Pages :

```
           <notebook>
                        <page string="Doctor prescription" name="doctor_prescription">
                            <group>
                                <field name="prescription"/>
                            </group>

                        </page>
                        <page string="Medicine" name="doctor_medicine">

                        </page>
                        <page string="other info" name="doctor_notes">

                                <field name="note"/>



                        </page>
               </notebook>
```

### Add One2many Field In Odoo  45:

in our model we need to add relation between appointment and medicine. appointment -> medicine :  every appointment
contains much medicine . the relation in this case is one to many `One2many`

**in appointment Model**

- appointment.prescription.line : related model name.
- appointment_id : related field.

` prescription_line_id = fields.One2many('appointment.prescription.line', 'appointment_id', string="prescription line")
`

**in medicine Model:**

```

class AppointmentPrescriptionLine(models.Model):
    _name = "appointment.prescription.line"
    _description = "appointment prescription line"

    name = fields.Char(string='Medicine')
    qty = fields.Integer(string="Quantity")
    appointment_id = fields.Many2one('hospital.appointment', string="appointment")


```

where:

- hospital.appointment :  is the related model.

then we define in our view the related field as tree and form view.

```
 <field name="prescription_line_id">
                                <tree>
                                    <field name="name"/>
                                    <field name="qty"/>

                                </tree>


                                <form>
                                    <group>
                                        <field name="name"/>
                                        <field name="qty"/>
                                    </group>

                                </form>
                            </field>
```

- we can add atrr `editable="bottom"` to tree to make edit inline to bottom side or `editable="top"` to add line to
  bottom side .
- we can assign `create="0"` `delete="0"` to disable these properties in form or tree view.

----

### Override Copy Function in Odoo 46

`copy = "False" to prevent copying field`
example:

```
    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('doctor_name'):
            default['doctor_name'] = f'copy {self.doctor_name}'
        rec = super(HospitalDoctor, self).copy(default)
        return rec


```

-----

### override delete method: 47

**_example:_**

```
   def unlink(self):
        """
        to override delete method
        """
        if self.state == 'done':
            raise ValidationError(f'You cannot Delete {self.ref} as it in Done state!!')
        return super(HospitalAppointment, self).unlink()
```

### Model Constraints || Python Constrains in Odoo: 48

`'name'` : is the field we want to add constrains on

`["hospital.patient"]` : the model that we want to search.

example :

```
    @api.constrains('name')
    def check_name(self):
        for rec in self:
            patient = self.env["hospital.patient"].search([('name', '=', rec.name), ('id', '!=', rec.id)])
            if patient:
                raise ValidationError(f'You cannot add  {rec.name} twice !!')


```

### Name Get Function In Odoo  show two  field in one field 49

example : set refernce and name as one field

```
    def name_get(self):
        result = []
        for rec in self:
            name = f'[ {rec.reference}]  {rec.name}'
            result.append((rec.id, name))
        return result

```

### To Inherit And Add Menu To Existing Module In Odoo 50

    <menuitem id="menu_sale_appointment" name="appointments" sequence="9"
              parent="sale.sale_order_menu" action="appointments_action"/>

- where **parent** we get from setting-> technical -> menu item and the action that we will render corresponding the
  click.

- add depends module in manifest file.

### Create PDF Reports In Odoo 51 :

-define report folder

- add report.xml
- define an action with unique id.
- define the template.
- add it in manifest.py docs: is equivalent to self
  `        
  <t t-foreach="docs" t-as="o">
  `

### Create Excel Report In Odoo 52 :

- download Base report xlsx from odoo store.
- add it in same directory of your module.
- `pip3 install xlsxwriter`
- `pip3 install xlrd`
- add `'report_xlsx'` in manifest file of module.
- add report record in report file as we did in pdf , be sure to add the report directory in manifest file.
-

Example:

```
        <record id="report_patient_card_xls" model="ir.actions.report">
        <field name="name">Patient Card Excel </field>
        <field name="model">hospital.patient</field>
        <field name="report_type">xlsx</field>
        <field name="report_name">hospital.report_patient_card_xlsx</field>
        <field name="report_file">hospital.report_patient_card_xlsx</field>
        <field name="binding_model_id" ref="model_hospital_patient"/>
        <field name="binding_type">report</field>


```

- add python file e.g `file_xls.py`
- add init file and import created file.
    - import `report` file in module `__init__` file.

- add class in python file as following , don't forget to use the id

```
from odoo import models
import base64
import io

class PatientXlsx(models.AbstractModel):
    _name = 'report.hospital.report_patient_card_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, patients):
        sheet = workbook.add_worksheet('patient ID xls')
        bold = workbook.add_format({'bold': True})
        row, col = 3, 3
        for obj in patients:
            print(type(patients))
            # report_name = obj.name
            # One sheet by partner
            bold = workbook.add_format({'bold': True})
            row += 1
            sheet.merge_range(row, col, row, col + 1, 'ID Card')
            row += 1
            sheet.write(row, col, 'Name')
            sheet.write(row, col + 1, obj.name)
            row += 1
            sheet.write(row, col, 'age')
            sheet.write(row, col + 1, obj.age)
            row+=1
            sheet.write(row, col, 'ref')
            sheet.write(row, col + 1, obj.reference)



```

- if we need to generate seperate sheet for each record ,
- add sheet with dynamic name in for loop , row, col also
- `sheet.set_column('D:D',12)` to set width of column.
- To add image field we need to import base64, io
- syntax for image :
- ` if obj.image:
  patient_image = io.BytesIO(base64.b64decode(obj.image))
  sheet.insert_image(row, col, "image.png", {'image_data': patient_image, 'x_scale': 0.5, 'y_scale': 0.5})
  `

### Server Action Add New Action To Action Button In Odoo 53

example in appointment view:

```
    <record id="action_confirm_appointments" model="ir.actions.server">
        <field name="name">Confirm appointment</field>
        <field name="model_id" ref="model_hospital_patient"/>
        <field name="binding_model_id" ref="model_hospital_patient"/>
        <field name="state">code</field>
        <field name="code">records.action_confirm()</field>

    </record>

```

### 54.URL Actions In Odoo

- add button under action:

` <button  name="action_url" string="open URL" type="object"
/>
`

- define a function in the model :
  `'target': 'new'` to add it in new window,

```
    def action_url(self):
        return {
            'type': 'ir.actions.act_url',
            'url': 'https://www.youtube.com/watch?v=7jbaJSZLL8A&list=PLqRRLx0cl0homY1elJbSoWfeQbRKJ-oPO&index=54',
            'target': 'self',
        }


```

### 55.How To Add Smart Buttons In Odoo14 | Odoo Smart Button Of Type Object

```
     <div class="oe_button_box" name="button_box">
                        <button name="action_open_appointment" type="object" class="oe_stat_button" icon="fa-calendar">
                            <div class="o_stat_info">
                                <field name="appointment_count" class="o_stat_value"/>
                                <span class="o_stat_text">Appointments</span>
                            </div>
                        </button>
                    </div>
```

- we need to define a function , if we need to return a view. example :

```
    def action_open_appointment(self):
        # to return view of appointment after clicking on Smart Buttons
        return {
            'name': _('appointment'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'hospital.appointment',
            'target': 'current',
            'domain': [('patient_id', '=', self.id)]
        }


```

or return record for that action:

```
    <record id="action_open_appointments" model="ir.actions.act_window">
        <field name="name">appointments</field>
        <field name='type'>ir.actions.act_window</field>
        <field name="res_model">hospital.appointment</field>
        <field name="view_mode">tree,form</field>
        <field name="domain">[('doctor_id','=', active_id)]</field>
        <field name="help" type="html">
            <p class="o_view_nocontent_empty_folder">
                create an appointment
            </p>
        </field>
    </record>

```
----

### 56.How To Add Archive And Unarchive Option In Odoo

- define a boolean field in the model.
- `    active = fields.Boolean(string="Active", default=True)
  `
- To set the archive in form view we need to add it in the form view as field.
- `  <field name="active" invisible="1"/>`

----

### 57.Use Of Active_ID In Odoo Development 
- we can get the active id  from `self._context`  
- we can assign   `res['patient_id'] = self._context.get('active_id')`
- we can assign active_id in 'ir.actions.act_window'
- `  <field name="domain">[('doctor_id','=', active_id)]</field>`
- `<field name="context">{'default_doctor_id' : active_id}</field>`
----
### 58. Change Position Of Field, Page or Group Using Move Attribute
- we created xml file add it in manifest.py for example : partner.py
add this code 
```
    <record id="view_partner_tree" model="ir.ui.view">
        <field name="name">res.partner</field>
        <field name="model">res.partner</field>
        <field name="inherit_id" ref="base.view_partner_tree"/>
        <field name="arch" type="xml">
            <xpath expr="//field[@name='phone']" position="before">
                <field name="email"  position="move"> </field>
            </xpath>

        </field>
    </record>

```
------
### 59.How To Add Ribbon To Form View In Odoo Development:
in form view :

`                    <widget name="web_ribbon" title="Archived" bg_color="bg-danger"
                            attrs="{'invisible': [('active', '=', True)]}"/>
`
-----
### 60.How To Add Search Panel In Odoo side bar  :
- from Home menu -> dev.tools -> Edit ControlPanelView
- look for `<searchpanel>`
- we add the search panel in search view 
- under the search tag
```
 <searchpanel>
                    <field name="state" string="status" select="multi" enable_counters="1"/>
                </searchpanel>
```

### 61.Default Group By Expand Option in tree view

- `<tree expand="1">`

-----
### 63.Create PDF Report From Wizard In Odoo14 :
- create wizard directory
- create python file with Transient Model add your fields with relations , add the button action .
- set access right in security folder.
- import the created file in local `__init__.py` of wizard.
- create your view in as xml ,if it menuitem you need to create action and view.
- DON'T FORGET TO ADD THE XML IN manifest FILE.
- add record in Report folder 
e.g 
```
  <record id="action_report_appointment" model="ir.actions.report">
        <field name="name">Appointment details</field>
        <field name="model">appointment.report.wizard</field>
        <field name="report_type">qweb-pdf</field>
        <field name="report_name">hospital.report_appointment_details</field>
        <field name="report_file">hospital.report_appointment_details</field>
        <field name="binding_model_id" ref="model_appointment_report_wizard"/>
        <field name="binding_type">report</field>


    </record>
```

- add template in report directory. and **don't forget manifest file**, 
- `"report_name"` from record as template id ,

- add the new view in manifest file , the template which we created in manifest file.

- add the logic you want in model and in render data in template file.

----
### 64.Create PDF Report Using Parser Function In Odoo:
- define abstract class as ` all_patient_abstract.py`
- send data via doc
- add the ` all_patient_abstract.py` in init.

----
### 65.Disable Opening And Create And Edit from Option Many2one:
add `options="{'no_create': True, 'no_create_edit':True}"` to the field you want .

`'no_open': True`  to prevent opening the record.

----
### 66.How To Create Excel Report From Wizard :
- add report Module from odoo store , then  add it in `manifest.py` in depends on as ` 'report_xlsx'`

- in wizard file ; create python file and create your TransientModel  to add the fields you want. add it in init file , in security.

- create the function for the buttons.
- create the menu item with action and view in wizard folder .
- add  a record in report/report.xml 
- add the template in report as xml  .
- add the created files in `manifest.py ` template and reports `xml`.
- create python file that contains a class and the method of rendering the data.
- import `py` it from `__init__`
- set the class name as in the record. `name="report_name"`

### add new item in selction field in Model.
```
class ProductTemplate(models.Model):
    _inherit = 'product.template'

    type = fields.Selection(selection_add=[
        ('test', 'test'), ('field_position_before')
    ], ondelete={'test': 'set default'},ondelete={'test2': 'cascade'} )
    
    
    # we have many option : set null / cascade 
```

 ```
 selection = [('a', 'A'), ('b', 'B')]

  selection_add = [('c', 'C'), ('b',)]

  > result = [('a', 'A'), ('c', 'C'), ('b', 'B')]
 ```


### Sales videos :
- create Quotation
- set variant to product for example : for specific color higher price.
- online Quotation , send by mail , design a template and send it to user.
- Delivery : we can add it a free based on total amount or set some rules depends on weight, volume,
- Pricelists :Set multiple prices per product, automated discounts, etc. from sales -> configuration-> price list
  - we specify the pricelist from contact -> Sales and purchase tab 



### purchase videos :
- **request for Quotation** :also known as an invitation for bid (IFB)
- 
- **Purchase Order Approval** : Request managers to approve orders above a minimum amount.
- Reordering Rules :
- select a product from sales--> product
- click on reordering 
- create a reordering form , set the product , min , max quantity , lead time etc...
- select the vendor from purchase -- save
- create a quotation 
- run a scheduler -> from inventory->operation-> run scheduler
- Purchase Agreements  : Manage your purchase agreements (call for tenders, blanket orders)
- purchase agreement : to call for tenders .
- 3 way matching :To make sure you only pay bills for which you received the goods you ordered.

