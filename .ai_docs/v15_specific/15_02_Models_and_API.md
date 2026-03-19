# Odoo 15: Models, ORM, and API Standards

`<role_instruction>`

You are writing Python backend code for **Odoo 15.0**. You must strictly adhere to the
V15 ORM methods. This version introduced the `Command` namespace for relational
operations, which you MUST use over legacy tuples.

`</role_instruction>`

## 1. Relational Field Operations (The `Command` Namespace)

`<rule>`

When writing to `One2many` or `Many2many` fields, NEVER use the legacy magic tuples
(e.g., `(0, 0, values)`, `(4, id)`, `(5, 0, 0)`). You MUST use the `odoo.fields.Command`
namespace. This makes code vastly more readable and prevents syntax errors.

`</rule>`

`<anti_pattern>`

```
# BAD: Legacy Odoo 14- tuple syntax
order.write({
    'order_line': [
        (0, 0, {'product_id': 1, 'price_unit': 10}), # Create
        (4, 5, 0),                                   # Link
        (5, 0, 0)                                    # Clear
    ]
})
```

`</anti_pattern>`

`<example>`

```
# GOOD: Odoo 15 Command namespace
from odoo import models, Command

def action_update_lines(self):
    self.write({
        'order_line': [
            Command.clear(),                                      # Equivalent to (5, 0, 0)
            Command.create({'product_id': 1, 'price_unit': 10}),  # Equivalent to (0, 0, {})
            Command.link(5)                                       # Equivalent to (4, 5)
        ]
    })
```

`</example>`

## 2. Custom Display Names (`name_get`)

`<rule>`

To customize how a record's name is displayed, you MUST override the `name_get()`
method. Modern `_compute_display_name` does not exist in V15.

`</rule>`

`<example>`

```
# GOOD: Odoo 15 name_get() implementation
def name_get(self):
    result = []
    for record in self:
        name = f"[{record.code}] {record.name}" if record.code else record.name
        result.append((record.id, name))
    return result
```

`</example>`

## 3. Data Retrieval & Aggregation

`<rule>`

Use `search_read(domain, fields)` for fetching specific dictionary fields. Use the
legacy `read_group()` method for aggregations. Do NOT use `search_fetch()` or
`_read_group()`, as they were introduced in later versions.

`</rule>`
