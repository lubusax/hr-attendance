# Odoo 16: Models, ORM, and API Standards

`<role_instruction>`

You are writing Python backend code for **Odoo 16.0**. You must strictly adhere to the
V16 ORM methods. Do not use modern Odoo 17 ORM additions like `search_fetch` or
`_compute_display_name`.

`</role_instruction>`

## 1. Custom Display Names (`name_get`) (CRITICAL)

`<rule>`

To customize how a record's name is displayed in Many2one dropdowns and relations, you
MUST override the `name_get()` method. It must return a list of tuples in the format
`(record.id, "Display Name")`.

_Warning: Do not hallucinate the Odoo 17 `_compute_display_name` method._

`</rule>`

`<anti_pattern>`

```
# FATAL ERROR IN V16: Using modern Odoo 17+ display name compute methods
@api.depends('name', 'code')
def _compute_display_name(self):
    pass
```

`</anti_pattern>`

`<example>`

```
# GOOD: Odoo 16 name_get() implementation
def name_get(self):
    result = []
    for record in self:
        name = f"[{record.code}] {record.name}" if record.code else record.name
        result.append((record.id, name))
    return result
```

`</example>`

## 2. Relational Field Operations (The `Command` Namespace)

`<rule>`

When writing to `One2many` or `Many2many` fields, you MUST use the `odoo.fields.Command`
namespace instead of legacy magic tuples.

`</rule>`

`<example>`

```
# GOOD: Odoo 16 Command namespace
from odoo import models, Command

def action_update_lines(self):
    self.write({
        'order_line': [
            Command.clear(),                                      # Clears all linked records
            Command.create({'product_id': 1, 'price_unit': 10}),  # Creates a new record
            Command.link(5)                                       # Links an existing record by ID
        ]
    })
```

`</example>`

## 3. Data Retrieval & Aggregation

`<rule>`

Use `search_read(domain, fields)` for fetching specific dictionary fields. Use the
standard `read_group()` method for aggregations (which returns dictionaries). Do NOT use
`search_fetch()` or `_read_group()`.

`</rule>`
