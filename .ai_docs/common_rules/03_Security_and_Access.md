# Odoo Security: Access Rights and Record Rules

`<role_instruction>`

Security is a foundational requirement. You must explicitly define access rights for
every new model you create. Failure to define access rights will result in Odoo throwing
access errors or showing empty views. Adhere strictly to these security guidelines.

`</role_instruction>`

## 1. Object-Level Access (`ir.model.access.csv`)

`<rule>`

Every custom model (except `AbstractModel`) MUST have at least one defined access right
in `security/ir.model.access.csv`.

`</rule>`

`<rule>`

Follow the strict naming convention for the `id` and `name` columns:

- `id`: `access_{model_name_with_underscores}_{group_name}`
- `name`: `{model.name.with.dots} {group name}` `</rule>`

`<anti_pattern>`

```
# BAD: Missing the group_id (grants access to all users, which is rarely intended) and incorrect ID formatting.
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_sale_order,sale order access,model_sale_order,,1,1,1,1
```

`</anti_pattern>`

`<example>`

```
# GOOD: Explicitly grants Read/Write/Create to a specific group, and Read-only to another.
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_nurzeit_custom_model_manager,nurzeit.custom.model manager,model_nurzeit_custom_model,sales_team.group_sale_manager,1,1,1,1
access_nurzeit_custom_model_user,nurzeit.custom.model user,model_nurzeit_custom_model,sales_team.group_sale_salesman,1,0,0,0
```

`</example>`

## 2. Row-Level Access (Record Rules via `ir_rule.xml`)

Record rules restrict which specific database rows a user can access, typically based on
their assigned company, department, or user ID.

`<rule>`

Use `ir.rule` in XML to define row-level security. If a model contains a `company_id`
field, you MUST implement a multi-company record rule to prevent data leakage between
companies.

`</rule>`

`<example>`

```
<!-- GOOD: Standard Multi-Company Record Rule -->
<odoo>
    <data noupdate="1">
        <record id="rule_nurzeit_custom_model_company" model="ir.rule">
            <field name="name">NURZEIT Custom Model Multi-Company</field>
            <field name="model_id" ref="model_nurzeit_custom_model"/>
            <!-- Applies rule globally across all users -->
            <field name="global" eval="True"/>
            <field name="domain_force">['|', ('company_id', '=', False), ('company_id', 'in', company_ids)]</field>
        </record>

        <!-- GOOD: User-specific Record Rule (e.g., Users only see their own records) -->
        <record id="rule_nurzeit_custom_model_personal" model="ir.rule">
            <field name="name">NURZEIT Custom Model Personal</field>
            <field name="model_id" ref="model_nurzeit_custom_model"/>
            <field name="groups" eval="[(4, ref('sales_team.group_sale_salesman'))]"/>
            <field name="domain_force">[('user_id', '=', user.id)]</field>
        </record>
    </data>
</odoo>
```

`</example>

## 3. Privilege Escalation (`sudo`)

`<rule>`

The `.sudo()` method bypasses ALL object-level and row-level security. It must NEVER be
used to bypass bad security design. Only use `.sudo()` when a standard user triggers a
background process that legitimately requires system-level access (e.g., generating an
invoice from a public website form).

`</rule>`

`<anti_pattern>`

```
# BAD: Using sudo() just to avoid writing proper ir.rule definitions.
def get_all_company_records(self):
    return self.env['nurzeit.custom.model'].sudo().search([])
```

`</anti_pattern>`

## 4. Manifest Loading Order

`<rule>`

Security files must be loaded BEFORE any views, data, or demo files in
`__manifest__.py`.

`</rule>`

`<example>`

```
# GOOD: Loading order in __manifest__.py
"data": [
    "security/security_groups.xml", # Create groups first (if applicable)
    "security/ir.model.access.csv", # Then grant object access
    "security/ir_rule.xml",         # Then restrict row access
    "views/model_views.xml",        # Then load the UI
],
```

`</example>`
