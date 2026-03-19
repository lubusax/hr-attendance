# Odoo 14: Hybrid JavaScript Framework (Legacy + Owl 1.0)

`<role_instruction>`

You are writing frontend JavaScript code for **Odoo 14.0**. This is a hybrid version.
The module definition MUST use `odoo.define`. For standard backend UI extensions (like
field widgets or form controllers), use the legacy `web.Widget` API. Owl 1.0 is
available but should only be used for standalone components like the Point of Sale or
custom Dashboards.

`</role_instruction>`

## 1. Module Definition (CRITICAL)

`<rule>`

Even if you are writing Owl 1.0 components, every JavaScript file MUST be wrapped in
`odoo.define()`. Native ES6 modules (`import`/`export` without `odoo.define`) will not
work in the Odoo 14 asset pipeline.

`</rule>`

`<anti_pattern>`

```
// FATAL ERROR IN V14: Using native ES6 imports without odoo.define
import { Component } from "@odoo/owl";
export class MyComponent extends Component {}
```

`</anti_pattern>`

## 2. Standard Backend UI (Legacy Widgets)

`<rule>`

If you are modifying standard backend views, adding a button to a form view, or creating
a custom field widget, you MUST use the legacy `web.Widget` or `web.AbstractField`
architecture based on jQuery.

`</rule>`

`<example>`

```
// GOOD: Odoo 14 legacy field widget
odoo.define('nurzeit.CustomField', function (require) {
    "use strict";

    var AbstractField = require('web.AbstractField');
    var registry = require('web.field_registry');

    var CustomColorField = AbstractField.extend({
        template: 'CustomColorFieldTemplate',
        events: _.extend({}, AbstractField.prototype.events, {
            'click .o_color_picker': '_onColorPicked',
        }),

        _renderReadonly: function () {
            this.$el.text(this.value);
        },
    });

    registry.add('nurzeit_color', CustomColorField);
    return CustomColorField;
});
```

`</example>`

## 3. Creating Standalone Dashboards (Owl 1.0)

`<rule>`

If you are building a completely custom client action (like a standalone Dashboard), you
may use Owl 1.0. You must extract Owl from the global `owl` object provided by Odoo,
inside `odoo.define`.

`</rule>`

`<example>`

```
// GOOD: Odoo 14 Owl 1.0 Component inside odoo.define
odoo.define('nurzeit.OwlDashboard', function (require) {
    "use strict";

    const { Component, useState } = owl;
    const core = require('web.core');
    const AbstractAction = require('web.AbstractAction');

    class DashboardComponent extends Component {
        constructor() {
            super(...arguments);
            this.state = useState({ clicks: 0 });
        }
        increment() {
            this.state.clicks++;
        }
    }
    // In V14, Owl templates are often defined inline or via an xml file loaded into the qweb registry
    DashboardComponent.template = owl.tags.xml`
        <div class="nurzeit-dashboard">
            <button t-on-click="increment">Clicks: <t t-esc="state.clicks"/></button>
        </div>`;

    // To use an Owl component in the V14 backend, it must be wrapped in an AbstractAction
    const DashboardWrapper = AbstractAction.extend({
        start: async function () {
            await this._super(...arguments);
            this.component = new DashboardComponent();
            await this.component.mount(this.el);
        }
    });

    core.action_registry.add('nurzeit_owl_dashboard', DashboardWrapper);
    return DashboardWrapper;
});
```

`</example>`
