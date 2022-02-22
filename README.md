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
