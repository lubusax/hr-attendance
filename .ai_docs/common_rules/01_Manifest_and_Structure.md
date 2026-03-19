# Odoo Module Structure, Manifest, and Linting Standards

`<role_instruction>`

Before writing any business logic, you must ensure the module strictly adheres to the
standard Odoo Community Association (OCA) folder structure and `__manifest__.py`
requirements. Failure to follow these rules will cause CI/CD pipelines (Flake8,
Pylint-Odoo) to fail.

`</role_instruction>`

## 1. Standard Module Directory Structure

`<rule>`

Every Odoo module must follow a strict, predictable directory structure. Do not create
custom root-level folders unless explicitly required by a specific framework feature
(e.g., `static/src/` for web assets).

`</rule>`

`<example>`

```
my_module_name/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── business_model.py
│   └── res_partner.py       # Inherited models named after the original model
├── views/
│   ├── business_model_views.xml
│   ├── res_partner_views.xml
│   └── menu_views.xml       # Keep menus separate if they are extensive
├── security/
│   ├── ir.model.access.csv  # Access rights
│   └── ir_rule.xml          # Record rules
├── data/
│   ├── default_data.xml     # Automated actions, sequences, cron jobs
│   └── noupdate_data.xml    # Data that shouldn't be overwritten on upgrade
├── tests/
│   ├── __init__.py
│   └── test_business_logic.py
└── static/
    ├── description/
    │   └── icon.png
    └── src/                 # JS (Owl), CSS/SCSS, and XML templates
```

`</example>`

## 2. The `__manifest__.py` File

`<rule>`

The manifest file must be a valid Python dictionary and contain all mandatory OCA keys.
The `version` key must strictly follow the format
`[Odoo Version].[Major].[Minor].[Patch]` (e.g., `17.0.1.0.0`).

`</rule>`

`<rule>`

For NURZEIT GmbH modules, always set the author to "NURZEIT GmbH" and use an appropriate
open-source license (typically `LGPL-3` or `AGPL-3`) unless instructed otherwise.

`</rule>`

`<anti_pattern>`

```
# BAD: Missing version prefix, missing license, poor file ordering
{
    'name': 'My Module',
    'version': '1.0',
    'author': 'Me',
    'depends': ['base'],
    'data': ['views/view.xml', 'security/ir.model.access.csv'], # Security must load FIRST
}
```

`</anti_pattern>`

`<example>`

```
# GOOD: Fully OCA-compliant manifest
{
    "name": "NURZEIT Custom Business Logic",
    "summary": "Extends the sales process for NURZEIT specific requirements.",
    "version": "17.0.1.0.0",
    "category": "Sales/Sales",
    "website": "[https://www.nurzeit.de](https://www.nurzeit.de)",
    "author": "NURZEIT GmbH, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "depends": [
        "sale_management",
        "account",
    ],
    "data": [
        "security/ir.model.access.csv",  # Always load security FIRST
        "security/ir_rule.xml",
        "data/sequence.xml",             # Then load foundational data
        "views/sale_order_views.xml",    # Then load UI views
        "views/menu_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
```

`</example>`

## 3. OCA Linting and Pylint-Odoo Standards

`<rule>`

All Python code must pass standard `flake8` checks (PEP8 compliance) and the strict
`pylint-odoo` plugin checks.

`</rule>`

- **Relative Imports:** NEVER use absolute imports for local module files. Use relative
  imports in your `__init__.py` files (e.g., `from . import models`).
- **Translation Wrapper:** All strings presented to the user in Python must be wrapped
  in the translation function `_()`.
- **Method Naming:** \* Compute methods must be prefixed with `_compute_`
  - Onchange methods must be prefixed with `_onchange_`
  - Action methods (called by UI buttons) must be prefixed with `action_`

`<example>`

```
# Example of compliant Python linting and naming conventions
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    nurzeit_custom_field = fields.Char(string="Custom Field")
    nurzeit_score = fields.Integer(compute="_compute_nurzeit_score", store=True)

    @api.depends('amount_total')
    def _compute_nurzeit_score(self):
        for order in self:
            order.nurzeit_score = int(order.amount_total / 10)

    def action_confirm_custom(self):
        self.ensure_one()
        if not self.nurzeit_custom_field:
            # Note the _() wrapper for translatable strings
            raise UserError(_("You must fill in the custom field before confirming."))
        return super(SaleOrder, self).action_confirm()
```

`</example>`
