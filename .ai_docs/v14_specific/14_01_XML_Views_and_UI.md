# Odoo 14: XML Views and UI Standards

`<role_instruction>`

You are writing code for **Odoo 14.0**. You must strictly use the legacy Odoo XML view
architecture. Do not use modern Odoo 17+ Python expressions for UI attributes.

`</role_instruction>`

## 1. Dynamic Attributes (`attrs`)

`<rule>`

To make a field dynamically invisible, readonly, or required based on other fields, you
MUST use the `attrs` attribute with a dictionary mapping. The values in the dictionary
must be Odoo domain lists.

`</rule>`

`<anti_pattern>`

```
<!-- FATAL ERROR IN V14: Using modern Python evaluation strings -->
<field name="partner_id" invisible="state == 'draft'"/>
```

`</anti_pattern>`

`<example>`

```
<!-- GOOD: Odoo 14 attrs dictionary syntax -->
<field name="partner_id" attrs="{'invisible': [('state', '=', 'draft')]}"/>
<field name="date_order" attrs="{'readonly': [('state', '!=', 'draft')], 'required': [('partner_id', '!=', False)]}"/>
```

`</example>`

## 2. The `states` Attribute

`<rule>`

If visibility or read-only status depends purely on a field named `state`, use the
`states` attribute as a shortcut instead of `attrs`. Provide a comma-separated list of
the states where the field should be editable/visible.

`</rule>`

`<example>`

```
<!-- GOOD: Using the states attribute for UI control -->
<button name="action_confirm" type="object" string="Confirm" states="draft,sent"/>
<field name="amount" states="draft"/>
```

`</example>`

## 3. Tree/List View Decorations

`<rule>`

In Odoo 14, Tree view decorations (e.g., `decoration-danger`, `decoration-info`) require
an Odoo domain list as a string, evaluated against the current record.

`</rule>`

`<example>`

```
<!-- GOOD: Odoo 14 decoration domains -->
<tree decoration-info="[('state', '=', 'draft')]" decoration-danger="[('amount_total', '&lt;', 0)]">
    <field name="name"/>
    <field name="amount_total"/>
    <field name="state"/>
</tree>
```

`</example>
