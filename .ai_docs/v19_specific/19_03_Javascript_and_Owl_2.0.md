# Odoo 19: JavaScript Framework and Owl 2.0

`<role_instruction>`

You are writing frontend JavaScript code for **Odoo 19.0**. You MUST use **Native ES6
Modules** (`import` / `export`) with the `/** @odoo-module **/` transpiler directive.
You must build UI elements exclusively using **Owl 2.0**. Legacy `odoo.define` and
`web.Widget` do not exist.

`</role_instruction>`

## 1. ES6 Modules and the Odoo Compiler (CRITICAL)

`<rule>`

NEVER use `odoo.define()`. Every JavaScript file must begin exactly with the comment
`/** @odoo-module **/` on the very first line. This instructs the Odoo asset compiler to
transpile the file. Use native `import` and `export` statements for all dependencies.

`</rule>`

`<anti_pattern>`

```
// FATAL ERROR IN V19: Using legacy module definition
odoo.define('nurzeit.CustomOwlComponent', function (require) {
    var Component = require('owl.Component');
});
```

`</anti_pattern>`

`<example>`

```
/** @odoo-module **/
// GOOD: Modern Odoo 19 ES6 Imports
import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class NurzeitComponent extends Component {
    setup() {
        this.orm = useService("orm");
        this.state = useState({ isReady: false });

        onWillStart(async () => {
            // Pre-fetch data before mounting
            this.state.isReady = true;
        });
    }
}
```

`</example>`

## 2. Component Registration

`<rule>`

To integrate your Owl component into the Odoo UI (as a client action, field widget, or
view), you must register it via `@web/core/registry`.

`</rule>`

`<example>`

```
/** @odoo-module **/
import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class NurzeitDashboard extends Component {
    static template = "nurzeit.DashboardTemplate";
}

// Registering the Owl component as a client action
registry.category("actions").add("nurzeit_dashboard", NurzeitDashboard);
```

`</example>`

## 3. Patching Existing Components

`<rule>`

To intercept or modify the behavior of existing Odoo web components in V19, use the
`patch` utility from `@web/core/utils/patch`.

`</rule>`

`<example>`

```
/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { FormController } from "@web/views/form/form_controller";

patch(FormController.prototype, {
    setup() {
        super.setup(...arguments); // Call super explicitly in modern patches
        console.log("NURZEIT patch initialized");
    },
    async saveButtonClicked() {
        console.log("Intercepting save execution");
        return super.saveButtonClicked(...arguments);
    }
});
```

`</example>`
