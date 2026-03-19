# Odoo 17: Models, ORM, and API Standards

`<role_instruction>`

You are writing Python backend code for **Odoo 17.0**. The ORM introduced significant
optimizations and deprecations in this version. You must strictly adhere to these modern
API patterns. Using legacy Odoo 15/16 ORM methods will result in rejected Pull Requests.

`</role_instruction>`

## 1. The Death of `name_get()` (CRITICAL)

`<rule>`

The `name_get()` method is completely removed in Odoo 17. You must NEVER define or
override `name_get()`.

To customize how a record's name is displayed across the system, you must override the
`_compute_display_name` method instead.

`</rule>`

`<anti_pattern>`

```
# FATAL ERROR IN V17: Using legacy name_get()
def name_get(self):
    result = []
    for record in self:
        name = f"[{record.code}] {record.name}"
        result.append((record.id, name))
    return result
```

`</anti_pattern>`

`<example>`

```
# GOOD: Modern Odoo 17 _compute_display_name implementation
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

When you need to retrieve specific fields from the database based on a domain, do not
use `search().read()` or `search().mapped()`. Use the highly optimized
`search_fetch(domain, field_names)` method, which combines the operation into a single,
exact SQL query.

`</rule>`

`<anti_pattern>`

```
# BAD: Less efficient, pulls full records into memory before reading/mapping
partners = self.env['res.partner'].search([('is_company', '=', True)])
names = partners.mapped('name')

# BAD: Legacy search_read syntax (returns dictionaries, not recordsets)
partner_dicts = self.env['res.partner'].search_read([('is_company', '=', True)], ['name', 'email'])
```

`</anti_pattern>`

`<example>`

```
# GOOD: Odoo 17 search_fetch() - returns a recordset but ONLY fetches requested fields from the DB
# This is incredibly fast and memory-efficient.
companies = self.env['res.partner'].search_fetch(
    [('is_company', '=', True)],
    ['name', 'email']
)
for company in companies:
    # Accessing company.name or company.email will NOT trigger a new query
    _logger.info("Company: %s, Email: %s", company.name, company.email)
```

`</example>`

## 3. Modern Aggregation: `_read_group()`

`<rule>`

Odoo 17 strongly favors the new `_read_group()` method over the legacy `read_group()`.

`_read_group(domain, groupby, aggregates)` returns a flat list of tuples, which is
significantly faster and easier to unpack in Python than the nested dictionaries
returned by the old `read_group()`.

`</rule>`

`<anti_pattern>`

```
# BAD: Legacy read_group() returns clunky dictionaries
grouped_data = self.env['sale.order'].read_group(
    [('state', '=', 'sale')],
    ['partner_id', 'amount_total:sum'],
    ['partner_id']
)
for group in grouped_data:
    partner_id = group['partner_id'][0] if group['partner_id'] else False
    total = group['amount_total']
```

`</anti_pattern>`

`<example>`

```
# GOOD: Modern Odoo 17 _read_group()
# Syntax: _read_group(domain, groupby_fields, aggregate_fields)
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

## 4. Environment Query Execution (Advanced)

`<rule>`

If you are explicitly forced to write raw SQL to bypass ORM limitations (which must be
exceptionally rare), use `self.env.execute_query()` instead of `self.env.cr.execute()`.
It automatically handles parameter escaping and returns the fetched rows as a list of
tuples, drastically reducing boilerplate code.

`</rule>`

`<example>`

```
# GOOD: Odoo 17 raw SQL execution
# Automatically executes and fetches all results safely
query = """
    SELECT id, name
    FROM res_partner
    WHERE active = %s AND is_company = %s
"""
results = self.env.execute_query(query, (True, True))

for partner_id, name in results:
    pass
```

`</example>`
