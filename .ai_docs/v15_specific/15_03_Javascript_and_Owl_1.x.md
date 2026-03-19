# Odoo 15: JavaScript Framework and Owl 1.x

`<role_instruction>`

You are writing frontend JavaScript code for **Odoo 15.0**. You MUST use `odoo.define`
to wrap your files. Odoo 15 heavily utilizes **Owl 1.x**. Do NOT use native ES6 module
imports (`import` / `export`), and do NOT use Owl 2.0 namespaces like `@odoo/owl`.

`</role_instruction>`

## 1. Module Definition (CRITICAL)

`<rule>`

Every JavaScript file MUST be wrapped in `odoo.define()`. You must extract Owl
components directly from the global `owl` object. Native ES6 modules will break the V15
asset compiler.

`</rule>`

`<anti_pattern>`

```
// FATAL ERROR IN V15: Using modern ES6/Owl 2.0 syntax
import { Component } from "@odoo/owl";
export class MyComponent extends Component {}
```

`</anti_pattern>`

`<example>`

```
// GOOD: Odoo 15 Owl 1.x module definition
odoo.define('nurzeit.CustomOwlComponent', function (require) {
    "use strict";

    const { Component, useState } = owl;

    class MyComponent extends Component {
        constructor() {
            super(...arguments);
            this.state = useState({ value: 1 });
        }
    }

    // In V15, templates are either defined inline or loaded via QWeb xml files
    // defined in the "web.assets_qweb" bundle.
    MyComponent.template = 'nurzeit.MyComponentTemplate';

    return MyComponent;
});
```

`</example>`

## 2. Integrating Owl with the Legacy Web Client

`<rule>`

To attach an Owl component to the standard backend (like a client action or a field
widget), you often need to wrap it using the legacy `Widget` or `AbstractAction` API, or
use the `WidgetAdapter`.

`</rule>`

`<example>`

```
// GOOD: Wrapping an Owl component to act as an Odoo 15 Client Action
odoo.define('nurzeit.DashboardAction', function (require) {
    "use strict";

    const core = require('web.core');
    const AbstractAction = require('web.AbstractAction');
    const MyOwlComponent = require('nurzeit.CustomOwlComponent'); // Require the Owl class

    const DashboardAction = AbstractAction.extend({
        start: async function () {
            await this._super(...arguments);
            // Instantiate and mount the Owl 1.x component
            this.owlComponent = new MyOwlComponent(this);
            await this.owlComponent.mount(this.el);
        },
        destroy: function () {
            if (this.owlComponent) {
                this.owlComponent.destroy();
            }
            this._super.apply(this, arguments);
        }
    });

    core.action_registry.add('nurzeit_dashboard', DashboardAction);

    return DashboardAction;
});
```

`</example>`
