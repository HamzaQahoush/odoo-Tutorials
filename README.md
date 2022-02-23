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
### add image field and show it  /38 .
in models : 

`image=fields.Binary(string='patient name')'` 

in XML :

` <field name="image" widget="image"  class="oe_avatar"/> `

----
### add sample data /39 
- add `sample='1'` in tree or kanban tag
----
###  show optional field /40:
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
- `store=True` attr. to field  to store related field in DB.

----
_wed 23-2-2022_
###  Enable Mass Editing 43 
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


###  Add One2many Field In Odoo  45:
in our model we need to add relation between appointment and medicine.
appointment -> medicine :  every appointment contains  much medicine .
the relation in this case is one to many `One2many`

**in appointment Model**
- appointment.prescription.line : related model  name.
- appointment_id : related field.

` prescription_line_id = fields.One2many('appointment.prescription.line', 'appointment_id',
                                           string="prescription line")
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


- we can add atrr `editable="bottom"` to tree to make edit inline to bottom side or `editable="top"` to add line to bottom side .
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

- where **parent** we get from setting-> technical -> menu item
and the action that we will render corresponding the click.

- add depends module in manifest file.


###  Create PDF Reports In Odoo 51 :
-define report folder 
- add report.xml 
- define an action with unique id.
- define the template.
- add it in manifest.py
docs: is equivalent to self 
`        
<t t-foreach="docs" t-as="o">
`


