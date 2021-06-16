odoo.define('web_hid_database.AbstractWebClient', function (require) {

    "use strict";

    var AbstractClient = require('web.AbstractWebClient');

    AbstractClient.include({

        init: function (parent) {
            this._super();
            this.set('title_part', {"zopenerp": "IATL"});

        },

    });

});