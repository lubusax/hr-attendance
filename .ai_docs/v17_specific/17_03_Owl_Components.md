# Odoo 17: Owl 2 Components and Frontend Architecture

`<role_instruction>`

You are writing frontend JavaScript code for **Odoo 17.0**. You must exclusively use
**Owl 2** and native ES6 modules. The legacy Odoo JavaScript framework (`odoo.define`,
`AbstractAction`, `Widget`, and `require`) is completely obsolete and will cause the
module to crash.

`</role_instruction>`

## 1. ES6 Modules and Imports (CRITICAL)

`<rule>`

NEVER use `odoo.define()` or `require()`. All JavaScript files must be written as native
ES6 modules using `import` and `export`.

Odoo core libraries and Owl are imported using the `@web/` and `@odoo/owl` aliases.

`</rule>`

`<anti_pattern>`

```
// FATAL ERROR IN V17: Legacy Odoo module definition
odoo.define('nurzeit.CustomWidget', function (require) {
    "use strict";
    var Widget = require('web.Widget');
    var rpc = require('web.rpc');
});
```

`</anti_pattern>`

`<example>`

```
/** @odoo-module **/
// GOOD: Modern Odoo 17 ES6 Imports
// Note: The /** @odoo-module **/ comment at the top is REQUIRED for the Odoo bundler.

import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
```

`</example>`

## 2. Component Definition and Registration

`<rule>`

All UI elements must be defined as classes extending `Component` from `@odoo/owl`. To
make a component available to the Odoo UI (e.g., as an action, a field widget, or a
view), you must add it to the appropriate Odoo `registry`.

`</rule>`

`<example>`

```
/** @odoo-module **/
import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class NurzeitDashboard extends Component {
    static template = "nurzeit.DashboardTemplate";

    setup() {
        this.actionService = useService("action");
        this.orm = useService("orm");
    }
}

// Registering the component as a client action so it can be opened from a menu
registry.category("actions").add("nurzeit_dashboard_action", NurzeitDashboard);
```

`</example>`

## 3. The `setup()` Method and Services

`<rule>`

Do not use a `constructor()` for initialization logic. All component initialization,
state management (`useState`), lifecycle hooks (`onWillStart`, `onMounted`), and service
injections (`useService`) MUST be declared synchronously inside the `setup()` method.

`</rule>`

`<example>`

```
/** @odoo-module **/
import { Component, useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class DataFetcher extends Component {
    static template = "nurzeit.DataFetcherTemplate";

    setup() {
        this.orm = useService("orm");

        // Reactive state
        this.state = useState({
            records: [],
            isLoading: true,
        });

        // Lifecycle hook to fetch data before the component renders
        onWillStart(async () => {
            this.state.records = await this.orm.searchRead("res.partner", [], ["name"]);
            this.state.isLoading = false;
        });
    }
}
```

`</example>`

## 4. Patching Existing Components

`<rule>`

To modify the behavior of an existing Odoo core component, you must use the `patch`
utility from `@web/core/utils/patch`. Do not attempt to use legacy `include` or
prototype manipulation.

`</rule>`

`<example>`

```
/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { FormController } from "@web/views/form/form_controller";

// Patching the core FormController to add custom logic on save
patch(FormController.prototype, {
    setup() {
        super.setup(...arguments); // Always call super.setup() when patching setup
        // Add custom setup logic here
    },

    async saveButtonClicked() {
        console.log("NURZEIT Intercept: Save button clicked");
        // Await the original save functionality
        await super.saveButtonClicked(...arguments);
    }
});
```

`</example>`

## 5. Templates and the Asset Bundle

`<rule>`

Owl templates must be written in separate XML files and placed in the `static/src/xml/`
directory. They do NOT go into the standard `views/` folder.

Furthermore, both your JavaScript and XML files MUST be explicitly declared in the
`__manifest__.py` file under the `assets` dictionary, typically targeting the
`web.assets_backend` bundle.

`</rule>`

`<example>`

```
<!-- File: static/src/xml/dashboard_template.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<templates xml:space="preserve">
    <t t-name="nurzeit.DashboardTemplate" owl="1">
        <div class="o_nurzeit_dashboard">
            <h1>NURZEIT Control Panel</h1>
            <button t-on-click="() => this.actionService.doAction('base.action_partner_form')" class="btn btn-primary">
                Open Partners
            </button>
        </div>
    </t>
</templates>
```

```
# File: __manifest__.py snippet
"assets": {
    "web.assets_backend": [
        "your_module_name/static/src/xml/dashboard_template.xml",
        "your_module_name/static/src/js/dashboard_component.js",
    ],
},
```

`</example>`
