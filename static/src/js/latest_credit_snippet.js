/** @odoo-module */
import { renderToElement } from "@web/core/utils/render";
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";
publicWidget.registry.get_product_tab = publicWidget.Widget.extend({
   selector : '.categories_section',
   async willStart() {
       const result = await rpc('/get_latest_credits', {});
       if(result){
           const chunks = [];
           let carousel_id = Math.random()
           for (let i = 0; i < result.credits.length; i +=4) {
               chunks.push(result.credits.slice(i, i+4))
           }
           chunks[0].is_active = true;
           this.$target.empty().html(renderToElement('dynamic_snippet.credit_data', {chunks: chunks,carousel_id:carousel_id}))
       }
   },
});
