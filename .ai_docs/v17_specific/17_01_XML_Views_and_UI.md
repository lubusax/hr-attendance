# Odoo 17: XML Views and UI Standards

`<role_instruction>`

You are writing code for **Odoo 17.0**. The XML view architecture underwent massive,
breaking changes in this version. You must strictly follow these new syntax rules.
Legacy Odoo 15/16 XML syntax will cause the module to crash immediately.

`</role_instruction>`

## 1. The Deprecation of `attrs` and `states` (CRITICAL)

`<rule>`

The `attrs` and `states` attributes are completely removed in Odoo 17. NEVER use them.

Instead, you must write native Python boolean expressions directly inside the
`invisible`, `readonly`, and `required` attributes.

`</rule>`

`<anti_pattern>`

```
<!-- FATAL ERROR IN V17: Using legacy attrs and states -->
<field name="partner_id" attrs="{'invisible': [('state', '=', 'draft')]}"/>
<field name="date_order" attrs="{'readonly': [('state', '!=', 'draft')], 'required': [('partner_id', '!=', False)]}"/>
<field name="amount" states="draft,sent"/>
```

`</anti_pattern>`

`<example>`

```
<!-- GOOD: Modern Odoo 17 native python expressions -->
<field name="partner_id" invisible="state == 'draft'"/>
<field name="date_order" readonly="state != 'draft'" required="partner_id"/>
<field name="amount" invisible="state not in ('draft', 'sent')"/>
```

`</example>`

## 2. Complex Conditions in UI Attributes

`<rule>`

When combining multiple conditions for visibility or read-only states, use standard
Python logical operators (`and`, `or`, `not`) and evaluation operators (`in`, `not in`,
`==`, `!=`). Do not use Odoo domain tuples (like `|` or `&`) for UI attributes.

`</rule>`

`<example>`

```
<!-- GOOD: Using Python logical operators directly in the XML string -->
<field name="discount" invisible="state == 'done' or not partner_id"/>
<field name="shipping_address" required="type in ('delivery', 'other') and partner_id"/>
<field name="is_manager_approved" readonly="1"/> <!-- Static booleans still use 1 or 0, or True/False -->
```

`</example>`

## 3. Tree/List View Decorations

`<rule>`

Just like `invisible` and `readonly`, Tree/List view decorations (`decoration-muted`,
`decoration-info`, `decoration-danger`, etc.) no longer use domain syntax. They also
require direct Python boolean expressions.

`</rule>`

`<anti_pattern>`

```
<!-- BAD: Legacy Odoo 16 decoration domain -->
<tree decoration-info="[('state', '=', 'draft')]">
    <field name="name"/>
</tree>
```

`</anti_pattern>`

`<example>`

```
<!-- GOOD: Odoo 17 decoration expression -->
<tree decoration-info="state == 'draft'" decoration-danger="amount_total &lt; 0">
    <field name="name"/>
    <field name="amount_total"/>
    <field name="state"/>
</tree>
```

`</example>`

_(Note: Use standard XML escaping like `&lt;` for `<` and `&gt;` for `>` if needed
inside expressions, though Odoo's parser often handles standard operators well if
wrapped carefully)._

## 4. Button Visibility

`<rule>`

Buttons no longer use `states="draft"`. You must use the `invisible` attribute with a
Python expression evaluating the current state.

`</rule>`

`<example>`

```
<!-- GOOD: Button visibility based on state -->
<header>
    <button name="action_confirm" type="object" string="Confirm" class="oe_highlight" invisible="state != 'draft'"/>
    <button name="action_cancel" type="object" string="Cancel" invisible="state in ('done', 'cancel')"/>
    <field name="state" widget="statusbar"/>
</header>
```

`</example>

## 5. XPath Inheritance in V17

`<rule>`

When inheriting and modifying an existing view, if you need to alter the `invisible`,
`readonly`, or `required` condition of an existing field, you must overwrite the
attribute directly using `attributes`.

`</rule>`

`<example>`

```
<!-- GOOD: Modifying an existing field's visibility in an inherited view -->
<record id="view_order_form_inherit_nurzeit" model="ir.ui.view">
    <field name="name">sale.order.form.inherit.nurzeit</field>
    <field name="model">sale.order</field>
    <field name="inherit_id" ref="sale.view_order_form"/>
    <field name="arch" type="xml">
        <xpath expr="//field[@name='payment_term_id']" position="attributes">
            <!-- Overwrites the default invisible condition -->
            <attribute name="invisible">state == 'cancel' or not partner_id</attribute>
        </xpath>
    </field>
</record>
```

`</example>
