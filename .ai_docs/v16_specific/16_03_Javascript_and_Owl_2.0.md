# Odoo 16: JavaScript Framework and Owl 2.0

`<role_instruction>`

You are writing frontend JavaScript code for **Odoo 16.0**. This version introduces a
massive paradigm shift. You MUST use **Native ES6 Modules** (`import` / `export`)
accompanied by the `/** @odoo-module **/` transpiler directive. You must use **Owl
2.0**. Do NOT use the legacy `odoo.define` or `require` syntax.

`</role_instruction>`

## 1. ES6 Modules and the Odoo Compiler (CRITICAL)

`<rule>`

NEVER use `odoo.define()`. Every JavaScript file must begin exactly with the comment
`/** @odoo-module **/` on the very first line. This tells the Odoo asset compiler to
transpile the file. Use native `import` and `export` statements for dependencies.

`</rule>`

`<anti_pattern>`

```
// FATAL ERROR IN V16: Using legacy Odoo 15- module definition
odoo.define('nurzeit.CustomOwlComponent', function (require) {
    var Component = require('owl.Component');
});
```

`</anti_pattern>`

`<example>`

```
/** @odoo-module **/
// GOOD: Modern Odoo 16 ES6 Imports
import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class MyComponent extends Component {
    setup() {
        this.orm = useService("orm");
        this.state = useState({ value: 1 });
    }
}
```

`</example>`

## 2. Component Registration

`<rule>`

To integrate your Owl 2.0 component into the Odoo UI (e.g., as an action, a field, or a
view), you must add it to the `@web/core/registry`. You no longer need to wrap Owl
components in legacy `AbstractAction` widgets.

`</rule>`

`<example>`

```
/** @odoo-module **/
import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class NurzeitDashboard extends Component {
    static template = "nurzeit.DashboardTemplate";
}

// Directly registering the Owl component as a client action
registry.category("actions").add("nurzeit_dashboard", NurzeitDashboard);
```

`</example>`

## 3. Patching Existing Components

`<rule>`

To modify the behavior of existing Odoo web components in V16, use the `patch` utility
from `@web/core/utils/patch`.

`</rule>`

`<example>`

```
/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { FormController } from "@web/views/form/form_controller";

patch(FormController.prototype, "nurzeit_form_patch", {
    setup() {
        this._super(...arguments);
        console.log("NURZEIT patch initialized");
    },
    async saveRecord() {
        console.log("Intercepting save");
        return this._super(...arguments);
    }
});
```

`</example>`
