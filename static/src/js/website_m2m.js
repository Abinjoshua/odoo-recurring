odoo.define('billing_schedule_page.m2m_widget', function (require) {
   "use strict";
   const publicWidget = require('web.public.widget');
   publicWidget.registry.M2MSelectWidget = publicWidget.Widget.extend({
       selector: '#tag_ids',
       start: function () {
           if ($(this.selector).length) {
               $(this.selector).select2({
                   placeholder: "Select multiple tags",
                   width: '100%'
               });
           }
       },
   });
});
