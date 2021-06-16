odoo.define('flexibite_com_advance.floor', function (require) {
"use strict";

	var floors = require('pos_restaurant.floors')
	var models = require('point_of_sale.models');
	var rpc = require('web.rpc');
	var core = require('web.core');

	var _t = core._t;

	floors.FloorScreenWidget.include({
		show: function(){
	        this._super();
	        setTimeout(function(){
	        	$('#slidemenubtn').hide();
	        }, 10);
		},
		renderElement: function(){
	        var self = this;
	        this._super();
	        this.$('.floor-bottom-button').click(function(event){
	        	var button_name = $(event.currentTarget).data('button-name');
	        	if(button_name){
	        		self.execute_action(button_name);
	        	}else{
	        		alert("Button name undefined.");
	        	}
	        });
		},
		execute_action: function(button_name){
			if(button_name == 'take_away'){
				this.pos.gui.show_popup('take_away_name_popup');
			}else if(button_name == 'delivery'){
				this.create_new_order();
				this.pos.get_order().set_is_delivery_from_floor(true);
				this.pos.chrome.screens.products.confirm_delivery_order();
				this.pos.gui.show_screen('clientlist');
			}
		},
		create_new_order: function(){
			this.pos.table = null;
			var order = new models.Order({},{pos:this.pos});
	        this.pos.get('orders').add(order);
	        this.pos.set('selectedOrder', order);
		},
	});

	floors.TableWidget.include({
        click_handler: function() {
            var self = this;
            var floorplan = this.getParent();
            if (floorplan.editing) {
                setTimeout(function() { // in a setTimeout to debounce with drag&drop start
                    if (!self.dragging) {
                        if (self.moved) {
                            self.moved = false;
                        } else if (!self.selected) {
                            self.getParent().select_table(self);
                        } else {
                            self.getParent().deselect_tables();
                        }
                    }
                }, 50);
            } else {
                if (this.table.parent_linked_table) {
                    floorplan.pos.set_table(this.table.parent_linked_table);
                } else {
                    floorplan.pos.set_table(this.table);
                }
            }
        },
        renderElement: function() {
            var self = this;
            if (!this.table.parent_linked_table) {
                this.table.parent_linked_table = this.pos.get_parent_linked_table(this.table)
            }
            this._super();
        },
    });

});