# Odoo ORM: Architecture, Performance, and Security Rules

`<role_instruction>` You must strictly adhere to these ORM performance and structural
rules when writing Python code for Odoo modules. `</role_instruction>`

## 1. Model Selection

`<rule>` Choose the correct base class based on the data's lifecycle and persistence
requirements. `</rule>`

- **`models.Model`**: Use for persistent, permanent business data (e.g., `sale.order`,
  `res.partner`).
- **`models.TransientModel`**: Use EXCLUSIVELY for temporary data, such as UI Wizards
  and mass-action dialogs. These are cleaned by an autovacuum cron job.
- **`models.AbstractModel`**: Use for Mixins and shared logic (e.g., `mail.thread`).
  These do not create physical database tables.

## 2. Environment (`self.env`) and Security

The `Environment` stores the database cursor, active user, and context. Recordsets are
immutable.

`<rule>` NEVER use `sudo()` globally or carelessly. It bypasses all row-level security
(Record Rules) and object-level security (Access Rights). `</rule>`

`<anti_pattern>`

```
# INSECURE: Bypasses all security checks for the entire method.
self.sudo().unlink()
```

`</anti_pattern>`

`<example>`

```
# SECURE: Only use sudo() on specific recordsets when a background process needs elevated rights to read system parameters.
api_key = self.env['ir.config_parameter'].sudo().get_param('payment.gateway.key')
```

`</example>`

`<rule>` Use `with_context()` to pass runtime variables (like `active_test=False` to
include archived records) without modifying method signatures. `</rule>`

## 3. CRUD Operations and Batch Processing (CRITICAL)

`<rule>`

Odoo ORM is designed for batch processing. NEVER execute `write()`, `create()`, or
`unlink()` inside a `for` loop over a recordset. This causes severe N+1 query
performance degradation. `</rule>`

`<anti_pattern>`

```
# SEVERE PERFORMANCE PENALTY (Executes N SQL UPDATE queries)
for order in orders:
    order.write({'state': 'done'})
```

`</anti_pattern>`

`<example>`

```
# HIGHLY OPTIMIZED (Executes 1 SQL UPDATE query)
orders.write({'state': 'done'})
```

`</example>`

## 4. In-Memory Data Manipulation

`<rule>`

Reduce database queries by utilizing in-memory Recordset operations: `mapped()`,
`filtered()`, and set operations. `</rule>`

`<example>`

```
# Extracts a list of unique country names from the recordset in memory
countries = orders.mapped('partner_id.country_id.name')

# Filters the recordset in memory without a new SQL query
high_value_orders = orders.filtered(lambda o: o.amount_total > 1000)

# Recordset Union (Combines two recordsets)
all_records = set_a | set_b
```

`</example>`

## 5. Modern API Standards (Version Specifics)

`<rule>`

If working in Odoo 16.2, 17.0, 18.0, or 19.0, use `search_fetch()` to combine search and
read operations into a single database hit when you only need specific fields. `</rule>`

`<example>`

```
# Odoo 16.2+ Optimization
records = self.env['sale.order'].search_fetch([('state', '=', 'draft')], ['name', 'amount_total'])
```

`</example>`

`<rule>`

If working in Odoo 17.0 or newer, NEVER use `name_get()`. It is deprecated. Implement
`_compute_display_name` instead. `</rule>`

`<example>`

```
# Modern Odoo 17+ Design Pattern
@api.depends('name', 'company_registry')
def _compute_display_name(self):
    for record in self:
        if record.company_registry:
            record.display_name = f"{record.name} [{record.company_registry}]"
        else:
            record.display_name = record.name
```

`</example>`
