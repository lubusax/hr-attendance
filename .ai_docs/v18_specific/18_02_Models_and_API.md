# Odoo 18: Models, ORM, and API Standards

`<role_instruction>`

You are writing Python backend code for **Odoo 18.0**. You must strictly adhere to
modern API patterns. Using legacy Odoo 16/15 ORM methods will result in immediate
crashes or rejected Pull Requests.

`</role_instruction>`

## 1. Custom Display Names (CRITICAL)

`<rule>`

The `name_get()` method is completely removed in Odoo 18. You must NEVER define or
override `name_get()`. To customize how a record's name is displayed, you MUST override
the `_compute_display_name` method.

`</rule>`

`<anti_pattern>`

```
# FATAL ERROR IN V18: Using legacy name_get()
def name_get(self):
    pass
```

`</anti_pattern>`

`<example>`

```
# GOOD: Modern Odoo 18 _compute_display_name implementation
@api.depends('name', 'code')
def _compute_display_name(self):
    for record in self:
        if record.code:
            record.display_name = f"[{record.code}] {record.name}"
        else:
            record.display_name = record.name
```

`</example>`

## 2. Optimized Data Retrieval: `search_fetch()`

`<rule>`

When retrieving specific fields from the database, NEVER use `search().read()` or
`search().mapped()`. You MUST use the highly optimized
`search_fetch(domain, field_names)` method to combine the search and read into a single
SQL query.

`</rule>`

`<example>`

```
# GOOD: Odoo 18 search_fetch() - Memory-efficient and fast
companies = self.env['res.partner'].search_fetch(
    [('is_company', '=', True)],
    ['name', 'email']
)
for company in companies:
    _logger.info("Company: %s, Email: %s", company.name, company.email)
```

`</example>`

## 3. Modern Aggregation: `_read_group()`

`<rule>`

Odoo 18 relies entirely on the new `_read_group(domain, groupby, aggregates)` method for
aggregations. It returns a flat list of tuples. Do NOT use the legacy `read_group()`
method which returns clunky dictionaries.

`</rule>`

`<example>`

```
# GOOD: Modern Odoo 18 _read_group()
grouped_data = self.env['sale.order']._read_group(
    domain=[('state', '=', 'sale')],
    groupby=['partner_id'],
    aggregates=['amount_total:sum']
)

# Returns a clean list of tuples: [(partner_record, amount_total_sum), ...]
for partner, amount_total_sum in grouped_data:
    _logger.info("Partner %s bought %s total", partner.name, amount_total_sum)
```

`</example>`

## 4. Relational Fields (Command Namespace)

`<rule>`

Always use the `odoo.fields.Command` namespace for relational operations on One2many and
Many2many fields. Never use magic tuples (e.g., `(0, 0, {})`).

`</rule>`
