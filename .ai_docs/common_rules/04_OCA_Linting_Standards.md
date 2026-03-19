# OCA Linting and Code Quality Standards

`<role_instruction>`

Your code must pass the official Odoo Community Association (OCA) CI/CD pipelines
without errors or warnings. This means strict compliance with `flake8` (PEP8) and
`pylint-odoo`. Treat the following linting rules as hard constraints.

`</role_instruction>`

## 1. Logging and Debugging

`<rule>`

NEVER use `print()` statements. Always use Python's standard `logging` library.

`</rule>`

`<anti_pattern>`

```
# BAD: Will fail pylint-odoo (print-used)
def action_process(self):
    print("Processing record", self.id)
```

`</anti_pattern>`

`<example>`

```
# GOOD: Standard Odoo logging implementation
import logging

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_process(self):
        _logger.info("Processing record %s", self.id)
```

`</example>`

## 2. Translation and String Formatting

`<rule>`

Every user-facing string in Python code (exceptions, messages, logs intended for users)
MUST be wrapped in the Odoo translation function `_()`.

`</rule>`

`<rule>`

Do not use f-strings or `.format()` _inside_ the translation wrapper if it contains
dynamic variables. The translation wrapper must contain the raw string with `%s`
formatting, and variables are applied outside of it.

`</rule>`

`<anti_pattern>`

```
# BAD: Variables inside the translation wrapper break the translation extractor.
raise UserError(_(f"The order {self.name} cannot be confirmed."))

# BAD: String not translated at all.
raise UserError("You cannot do this.")
```

`</anti_pattern>`

`<example>`

```
# GOOD: The translation string is static, variables are applied after.
from odoo import _, models
from odoo.exceptions import UserError

def action_confirm(self):
    if self.state == 'cancel':
        raise UserError(_("The order %s cannot be confirmed because it is cancelled.") % self.name)
```

`</example>`

## 3. Database Transactions and State

`<rule>`

NEVER use `self.env.cr.commit()` or `self.env.cr.rollback()` in standard business logic.
Odoo handles database transactions automatically at the end of the HTTP request or Cron
job. Manual commits break testing rollbacks and can corrupt the database state.

`</rule>`

`<anti_pattern>`

```
# BAD: Will fail pylint-odoo (invalid-commit)
def update_status(self):
    self.write({'state': 'done'})
    self.env.cr.commit()
```

`</anti_pattern>`

## 4. Import Structure

`<rule>`

Python imports must be grouped in a specific order:

1. Standard Python libraries

2. Third-party libraries

3. Odoo core imports

4. Local relative imports

   `</rule>`

`<example>`

```
# GOOD: Correct import grouping
import json
import logging
from datetime import datetime

import requests

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

from . import utils  # Local relative import
```

`</example>`

## 5. Naming Conventions

`<rule>`

Adhere strictly to OCA naming conventions for methods and variables to ensure
maintainability.

`</rule>`

- **Compute Methods:** `_compute_{field_name}`
- **Inverse Methods:** `_inverse_{field_name}`
- **Search Methods:** `_search_{field_name}`
- **Onchange Methods:** `_onchange_{field_name}`
- **Action Methods (Buttons):** `action_{verb}_{noun}` (e.g., `action_confirm_order`)
- **XML IDs:** `{model_name}_view_{view_type}` (e.g., `sale_order_view_form`)

`<example>`

```
# GOOD: Method naming correctly matches the field it computes
amount_tax = fields.Float(compute='_compute_amount_tax')

@api.depends('order_line.price_tax')
def _compute_amount_tax(self):
    # ... logic ...
```

`</example>`

## 6. XML Code Standards

`<rule>`

In XML files, do not use hardcoded strings for labels or attributes that users will see.
Odoo extracts XML strings automatically, but you must ensure `string=""` or `help=""`
attributes are used correctly.

`</rule>`

`<rule>`

When inheriting views, always use precise XPath expressions. Avoid relying on positional
XPaths (like `//field[2]`) as they break easily during upgrades. Target the `name`
attribute of a field instead.

`</rule>`

`<example>`

```
<!-- GOOD: Targeting a field directly by name -->
<xpath expr="//field[@name='partner_id']" position="after">
    <field name="nurzeit_custom_field"/>
</xpath>
```

`</example>`
