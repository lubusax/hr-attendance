# Odoo 19: Models, ORM, and API Standards

`<role_instruction>`

You are writing Python backend code for **Odoo 19.0**. This version introduces highly
optimized access checks, a unified `Query` object, and the JSON2 API. You must strictly
adhere to these modern API patterns.

`</role_instruction>`

## 1. The `Query` Object for Advanced Data Retrieval

`<rule>`

Odoo 19 introduces the `Query` object to abstract raw data queries and securely pass
parameters. If you are ever forced to construct complex SQL (which should be rare), do
not use raw string concatenation. Rely on the ORM's underlying query building tools to
ensure SQL injection protection.

`</rule>`

## 2. Unified Security and Access Checks

`<rule>`

In Odoo 19, access rights (modellbasiert) and record rules (zeilenbasiert) have been
restructured and unified into highly optimized methods. Avoid writing redundant, manual
security loops. Rely on native `check_access()` and `_filtered_access()` methods which
handle both tiers of security in a single, memory-efficient call.

`</rule>`

`<example>`

```
# GOOD: Using native optimized access filtering in V19
# This safely removes records the user shouldn't see without crashing
accessible_records = records._filtered_access('read')
```

`</example>`

## 3. Custom Display Names

`<rule>`

The legacy `name_get()` method does not exist. To customize how a record's name is
displayed, you MUST override the `_compute_display_name` method.

`</rule>`

`<example>`

```
# GOOD: Modern Odoo 19 _compute_display_name implementation
@api.depends('name', 'code')
def _compute_display_name(self):
    for record in self:
        if record.code:
            record.display_name = f"[{record.code}] {record.name}"
        else:
            record.display_name = record.name
```

`</example>`

## 4. Optimized Data Retrieval & Aggregation

`<rule>`

- **Fetching:** Use `search_fetch(domain, field_names)` to combine search and read into
  a single SQL query. NEVER use `search().read()`.
- **Grouping:** Use `_read_group(domain, groupby, aggregates)` which returns a flat list
  of tuples. `</rule>`

## 5. External API endpoints (JSON2)

`<rule>`

If you are developing external API controllers in Odoo 19, utilize the new `JSON2`
endpoint specifications. It leverages semantisch korrekte HTTP-Statuscodes (e.g.,
404, 500) and token-based API keys instead of legacy XML-RPC/cleartext passwords.

`</rule>`
