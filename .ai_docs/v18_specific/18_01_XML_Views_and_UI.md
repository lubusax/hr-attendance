# Odoo 18: XML Views and UI Standards

`<role_instruction>`

You are writing code for **Odoo 18.0**. You must strictly use the modern XML view
architecture. Legacy Odoo 16/15 XML syntax (`attrs`, `states`) is entirely removed from
the core and will cause immediate parsing crashes.

`</role_instruction>`

## 1. Native Python Expressions (CRITICAL)

`<rule>`

The `attrs` and `states` attributes DO NOT EXIST in Odoo 18. You must write native
Python boolean expressions directly inside the `invisible`, `readonly`, and `required`
attributes.

`</rule>`

`<anti_pattern>`

```
<!-- FATAL ERROR IN V18: Using legacy attrs and states -->
<field name="partner_id" attrs="{'invisible': [('state', '=', 'draft')]}"/>
<field name="amount" states="draft,sent"/>
```

`</anti_pattern>`

`<example>`

```
<!-- GOOD: Modern Odoo 18 native python expressions -->
<field name="partner_id" invisible="state == 'draft'"/>
<field name="date_order" readonly="state != 'draft'" required="partner_id"/>
<field name="amount" invisible="state not in ('draft', 'sent')"/>
```

`</example>`

## 2. Complex UI Conditions

`<rule>`

When combining multiple conditions for visibility or read-only states, use standard
Python logical operators (`and`, `or`, `not`) and evaluation operators (`in`, `not in`,
`==`, `!=`).

`</rule>`

`<example>`

```
<!-- GOOD: Using Python logical operators directly in the XML string -->
<field name="discount" invisible="state == 'done' or not partner_id"/>
<field name="shipping_address" required="type in ('delivery', 'other') and partner_id"/>
<!-- For static boolean flags, use standard 1, 0, True, or False -->
<field name="is_manager_approved" readonly="1"/>
```

`</example>`

## 3. Tree/List View Decorations

`<rule>`

Tree/List view decorations (`decoration-muted`, `decoration-info`, `decoration-danger`)
require direct Python boolean expressions. Do NOT use Odoo domain lists.

`</rule>`

`<example>`

```
<!-- GOOD: Odoo 18 decoration expression -->
<tree decoration-info="state == 'draft'" decoration-danger="amount_total &lt; 0">
    <field name="name"/>
    <field name="amount_total"/>
    <field name="state"/>
</tree>
```

`</example>

## 4. XPath Inheritance for Attributes

`<rule>`

When inheriting an existing view to alter `invisible`, `readonly`, or `required`
conditions, you must overwrite the attribute directly using the `position="attributes"`
XPath.

`</rule>`

`<example>`

```
<!-- GOOD: Overwriting visibility in an inherited view -->
<xpath expr="//field[@name='payment_term_id']" position="attributes">
    <attribute name="invisible">state == 'cancel' or not partner_id</attribute>
</xpath>
```

`</example>
