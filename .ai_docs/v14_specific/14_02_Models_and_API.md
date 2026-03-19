# Odoo 14: Models, ORM, and API Standards

`<role_instruction>`

You are writing Python backend code for **Odoo 14.0**. You must strictly adhere to the
V14 ORM methods. Do not use modern ORM additions like `search_fetch` or
`_compute_display_name`.

`</role_instruction>`

## 1. Custom Display Names (`name_get`)

`<rule>`

To customize how a record's name is displayed in Many2one dropdowns and relations, you
MUST override the `name_get()` method. It must return a list of tuples in the format
`(record.id, "Display Name")`.

`</rule>`

`<anti_pattern>`

```
# FATAL ERROR IN V14: Using modern Odoo 17+ display name compute methods
@api.depends('name', 'code')
def _compute_display_name(self):
    pass
```

`</anti_pattern>`

`<example>`

```
# GOOD: Odoo 14 name_get() implementation
def name_get(self):
    result = []
    for record in self:
        if record.code:
            name = f"[{record.code}] {record.name}"
        else:
            name = record.name
        result.append((record.id, name))
    return result
```

`</example>`

## 2. Data Retrieval: `search_read()`

`<rule>`

When fetching specific fields from the database, use `search_read(domain, fields)`. This
returns a list of dictionaries. Do NOT use `search_fetch()`, as it does not exist in
V14.

`</rule>`

`<example>`

```
# GOOD: Odoo 14 search_read()
partner_dicts = self.env['res.partner'].search_read(
    [('is_company', '=', True)],
    ['name', 'email']
)
```

`</example>`

## 3. Aggregation: `read_group()`

`<rule>`

For grouping data and aggregating sums or counts, use the legacy `read_group()` method.
It returns a list of dictionaries with the grouped data.

`</rule>`

`<example>`

```
# GOOD: Odoo 14 read_group()
grouped_data = self.env['sale.order'].read_group(
    domain=[('state', '=', 'sale')],
    fields=['partner_id', 'amount_total'],
    groupby=['partner_id']
)
```

`</example>`
