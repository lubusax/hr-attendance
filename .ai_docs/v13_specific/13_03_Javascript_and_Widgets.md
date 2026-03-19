# Odoo 13: Legacy JavaScript Framework and Widgets

`<role_instruction>`

You are writing frontend JavaScript code for **Odoo 13.0**. You MUST use the legacy Odoo
JavaScript framework (`odoo.define`, `web.Widget`, etc.). The Owl framework and ES6
modules DO NOT exist in this version.

`</role_instruction>`

## 1. Module Definition and Dependencies (CRITICAL)

`<rule>`

Every JavaScript file must be wrapped in `odoo.define()`. Dependencies must be loaded
using the `require()` function provided in the callback. DO NOT use ES6 `import` or
`export`.

`</rule>`

`<anti_pattern>`

```
// FATAL ERROR IN V13: Using modern ES6/Owl syntax
import { Component } from "@odoo/owl";
export class MyComponent extends Component {}
```

`</anti_pattern>`

`<example>`

```
// GOOD: Odoo 13 legacy module definition
odoo.define('nurzeit.CustomWidget', function (require) {
    "use strict";

    var Widget = require('web.Widget');
    var core = require('web.core');
    var rpc = require('web.rpc');

    var _t = core._t;

    // Implementation goes here...
});
```

`</example>`

## 2. Creating Widgets

`<rule>`

To create UI elements, you must extend `web.Widget` (or specific widgets like
`web.AbstractField`). You must rely on jQuery (accessible via `this.$el`) for DOM
manipulation.

`</rule>`

`<example>`

```
// GOOD: Odoo 13 Widget definition
odoo.define('nurzeit.Dashboard', function (require) {
    "use strict";

    var Widget = require('web.Widget');
    var core = require('web.core');

    var NurzeitDashboard = Widget.extend({
        template: 'NurzeitDashboardTemplate',
        events: {
            'click .o_my_button': '_onButtonClicked',
        },

        init: function (parent, options) {
            this._super.apply(this, arguments);
            this.data = [];
        },

        willStart: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                // Fetch data via RPC before rendering
                return self._fetchData();
            });
        },

        start: function () {
            // Widget is rendered, this.$el is available
            return this._super.apply(this, arguments);
        },

        _fetchData: function () {
            // Use legacy web.rpc for server calls
            var rpc = require('web.rpc');
            return rpc.query({
                model: 'res.partner',
                method: 'search_read',
                args: [[], ['name']],
            }).then(function (result) {
                // ... handle data
            });
        },

        _onButtonClicked: function (ev) {
            ev.preventDefault();
            console.log("Button clicked!");
        }
    });

    core.action_registry.add('nurzeit_dashboard_action', NurzeitDashboard);

    return NurzeitDashboard;
});
```

`</example>`
