# Odoo 15: XML Views and UI Standards

`<role_instruction>`

You are writing code for **Odoo 15.0**. You must strictly use the legacy Odoo XML view
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
<!-- FATAL ERROR IN V15: Using modern Python evaluation strings -->
<field name="partner_id" invisible="state == 'draft'"/>
```

`</anti_pattern>`

`<example>`

```
<!-- GOOD: Odoo 15 attrs dictionary syntax -->
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

## 3. Asset Loading (No more assets.xml)

`<rule>`

In Odoo 15, do NOT use XML files (like `assets.xml`) with
`<template id="assets_backend">` to load JavaScript or CSS files. All frontend assets
MUST be declared explicitly in the `__manifest__.py` file under the `"assets"`
dictionary.

`</rule>`

`<example>`

```
# GOOD: Odoo 15 Asset declaration in __manifest__.py
"assets": {
    "web.assets_backend": [
        "your_module/static/src/js/custom_component.js",
        "your_module/static/src/scss/custom_styles.scss",
    ],
    "web.assets_qweb": [
        "your_module/static/src/xml/custom_templates.xml",
    ],
}
```

`</example>
