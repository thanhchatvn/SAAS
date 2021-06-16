odoo.define('pos2.card2cardPos', function(require) {
"use strict";

var screens = require('point_of_sale.screens') //// Require Base screens class
var model = require('point_of_sale.models');
var BarcodeEvents = require('barcodes.BarcodeEvents').BarcodeEvents;

// creating new object form XMLHttpRequest in order to send 
// request to get date trom the local server
var xhr = new XMLHttpRequest()


var PaymentScreenWidget = screens.PaymentScreenWidget;


PaymentScreenWidget.include({

    init: function(parent, options) {
        var self = this;
        this._super(parent, options);
        
        this.keyboard_keydown_handler = function(event){
            if(document.getElementById("cardfrom").style.display === 'block'){
                    return;
            }

            if (event.keyCode === 8 || event.keyCode === 46) { // Backspace and Delete
                event.preventDefault();

                // These do not generate keypress events in
                // Chrom{e,ium}. Even if they did, we just called
                // preventDefault which will cancel any keypress that
                // would normally follow. So we call keyboard_handler
                // explicitly with this keydown event.
                self.keyboard_handler(event);
            }
        };
        
        // This keyboard handler listens for keypress events. It is
        // also called explicitly to handle some keydown events that
        // do not generate keypress events.
        this.keyboard_handler = function(event){
            // On mobile Chrome BarcodeEvents relies on an invisible
            // input being filled by a barcode device. Let events go
            // through when this input is focused.
            if(document.getElementById("cardfrom").style.display === 'block'){
                    return;
            }
            
            if (BarcodeEvents.$barcodeInput && BarcodeEvents.$barcodeInput.is(":focus")) {
                return;
            }

            var key = '';

            if (event.type === "keypress") {
                if (event.keyCode === 13) { // Enter
                    self.validate_order();
                } else if ( event.keyCode === 190 || // Dot
                            event.keyCode === 110 ||  // Decimal point (numpad)
                            event.keyCode === 188 ||  // Comma
                            event.keyCode === 46 ) {  // Numpad dot
                    key = self.decimal_point;
                } else if (event.keyCode >= 48 && event.keyCode <= 57) { // Numbers
                    key = '' + (event.keyCode - 48);
                } else if (event.keyCode === 45) { // Minus
                    key = '-';
                } else if (event.keyCode === 43) { // Plus
                    key = '+';
                }
            } else { // keyup/keydown
                if (event.keyCode === 46) { // Delete
                    key = 'CLEAR';
                } else if (event.keyCode === 8) { // Backspace
                    key = 'BACKSPACE';
                }
            }

            self.payment_input(key);
            event.preventDefault();
        };

    },

    format_date: function(date) {
        var array_date = date.split("-");
        var year = array_date[0];
        var month = array_date[1];
        var last_2_digit = year.slice(2);
        var sending_format = last_2_digit + month;
        return   sending_format
    },

    start: function(){
        
        this.$el.find('#btnCancel').click(_.bind(this.cancelTransformation, this));
        // this.$el.find('#btnSubmit').click(_.bind(this.cardToCardTransformation, this));
//        console.log("The this prototype");
//        console.log(this);
        var send_with_card = false;
        $('#cardfrom').submit( (event) => {
            event.preventDefault();
            var $from_input = $("#fromcard");
            var val = $from_input.val()
            // console.log($from_input.val());
            // var date_val = document.getElementById("expDate").value;
            // console.log(date_val);
            // var res = this.format_date(date_val);
            // console.log(res);
            if (val.length != 16 ) {
                alert(`The Form number must be 16 numbers only, the card number is: ${val.length}`);
            } else {
                this.cardToCardTransformation();
            }
        });
        

        //TODO: Validat the From input 
        // $("#cardfrom").focusout(() => {
        //     var $from_input = $("#fromcard");
        //     // console.log($from_input);
        //     // console.log($from_input.val());
        //     var val = $from_input.val()
        //     if (val.length < 16) {

        //     }
        // });

    },

    //TODO: OverRid the default keyboard POS behaviour







//{
//                'from_card': document.getElementById("cardfrom").value,  //'9888190191237806',
//                'ipn': document.getElementById("ipn").value, //"0000",
//                'expiration_data': document.getElementById("expDate").value, //"2202",
//                'to_card': document.getElementById("tocard").value ,//"9888190191237806",
//                'trans_amount': document.getElementById("amountcard").value//10000
//             }


    cardToCardTransformation: async function() {
        //TODO: The transformation process process
        var res = await this._rpc({
            model: 'pos.card.to.card.transfer.model',
            method: 'transfer',
            args : [[],{
                'from_card':  document.getElementById("fromcard").value,
                'ipn': document.getElementById("ipn").value,
                'expiration_data': this.format_date(document.getElementById("expDate").value), //TODO: this.format_date(date) will send the data in the desired format +> exp: 2022-01-26 ==> 2201 === the last 2 digit of the year + the month
                'to_card': document.getElementById("tocard").value,
                'trans_amount': document.getElementById("amountcard").value
             }

             ]

            });
    //    console.log("The res button");
    //    console.log(res);

//          console.log("The data from the form");
//        console.log(document.getElementById("fromcard").value);
//        console.log(document.getElementById("ipn").value);
//        console.log(document.getElementById("expDate").value);
//        console.log(document.getElementById("tocard").value);
//        console.log(document.getElementById("amountcard").value);

        if (res["ok"]) {
            // var port = browser.runtime.connectNative("ping_pong");
            //TODO: close the popup and empty all the fields
            alert(res["message"]);
            this.cancelTransformation();
            //TODO: proceed
            // port.postMessage(res["message"]);
            // alert(res["message"]);
            // console.log(res);
            //TODO: Given the proceed_to_usual() function a hard coded "confirm" is not appropreate but
            //TODO: make the sending with card false
            this.send_with_card = false;
            //TODO: we will assume that the function is correct when it reach this point
            this.proceed_to_usual("confirm");
            
        } else {
            
            alert(res["message"]);
        }


    },

    cancelTransformation: function() {
        document.getElementById("cardfrom").style.display ="none";
        document.getElementById("fromcard").value ="";
        document.getElementById("ipn").value ="";
        document.getElementById("expDate").value ="";
        document.getElementById("tocard").value ="";
        document.getElementById("amountcard").value ="";
    },

    sleep: function (ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    },

    proceed_to_usual: function(force_validation) {

//        console.log("Is the order valid");
//        console.log(this.order_is_valid(force_validation));

        if (this.order_is_valid(force_validation)) {
            var order = this.pos.get_order();
            var paymwnt = order.get_paymentlines();
            this.finalize_validation();
        }

    },


    open_payment_wizard: function(to_card) {
        // document.getElementById("fromcard").value ="";
        // document.getElementById("ipn").value ="";
        document.getElementById("tocard").value = to_card;
        document.getElementById("cardfrom").style.display ="block";
        document.getElementById("amountcard").value = this.inputbuffer;

        // console.log(document.getElementById("tocard").value);

    },

     call_rpc: async function() {

        var journal_array = await this._rpc({
                    fields: ['card_information_id', 'card_to_card_payment'],
                    model: 'account.journal',
                    method: 'search_read',
                    domain: [['id', 'in', journal_ids]],
                })

        return journal_array

     },


    validate_order: async function(force_validation){

//        console.log("###########From inside pos2 >>>>force_validation###################");
//        console.log(force_validation);
//        console.log("###########From inside pos2 >>>>force_validation###################");



        var order = this.pos.get_order();
        var paymwnt = order.get_paymentlines();
        var journal_ids = [];
        var to_card = 0;
        // console.log(order);
        paymwnt.forEach(obj => {
            journal_ids.push(obj.cashregister.journal.id);
        });
        
        // console.log("$$$$$$$ journal_ids &&&&&&&&&&");
        // console.log(journal_ids);

        ///////////////////////////////////////////////////////////
        // TODO: IF the customer is selected git his card number /
        // and fill the wizard From card input type with it.    /
        ////////////////////////////////////////////////////////
        // var partner_card_filled = false;
        
        try {
            var changed = order.changed;
            var client_id = changed.client.id
            /////////////////////////////////////////////////////////
            //TODO: Get the client array to get the card information/
            ////////////////////////////////////////////////////////
            var ressult = await fetch(
                `/pos_card2card_payment/get_partner?id=${client_id}`,
                {
                    method:'GET',
                    headers: {
                        'Content-Type':'application.json'
                    }
                }
                );
            var client_card_info = await ressult.json();
            if (client_card_info.error) {
                // console.log(client_card_info.message);
            } else {
                document.getElementById("expDate").setAttribute('type','text');
                var client_card_number   = client_card_info.card_number;
                var client_card_exp_date = client_card_info.end_date;
                document.getElementById("expDate").value = client_card_exp_date; 
                // console.log(client_card_number);
                document.getElementById("fromcard").value = client_card_number; 
                // partner_card_filled = true;
    
            }
            // console.log(client_card_info);

        } catch (e) {
            document.getElementById("expDate").setAttribute('type','date');
        }
        
        

        ////////////////////////////////////////////////////////////////////////////////////////
        //TODO: Call the backend to get the journal card information of the seller and the payment type/
        ////////////////////////////////////////////////////////////////////////////////////////
        
        // var bank_array = await this._rpc({
        //         fields: ['bank_id'],
        //         model: 'res.partner.bank',
        //         method: 'search_read',
        //         domain: [['journal_id', 'in', journal_ids]],
        //     })
        
        // var journal_array = await this._rpc({
        //         fields: ['bank_account_id'],
        //         model: 'account.journal',
        //         method: 'search_read',
        //         domain: [['id', 'in', journal_ids]],
        //     })

        var ressult = await fetch(
            `/pos_card2card_payment/get_journal_bank_card?ids=${journal_ids}`,
            {
                method:'GET',
                headers: {
                    'Content-Type':'application.json'
                }
            }
            );
        var journal_bank_card_info = await ressult.json();
        // console.log(" ************* bank_card_info *********** ");
        // console.log(journal_bank_card_info);

        //TODO: if the payment method type is card to card call the wizard else proceed as usual
            
        if (journal_bank_card_info.error == false) {

            var card_index;
            var is_used = journal_bank_card_info.is_used_in_pos;  
            var what_card_used = journal_bank_card_info.card_number;  
            for( var journal_used in is_used) {
                // console.log("##########################")
                // console.log(is_used[journal_used]);
                // console.log(journal_used);
                if(is_used[journal_used]) {
                    this.send_with_card = true;
                    card_index = journal_used
                    // show the wizard if only one line contain card to card payment
                    break;
                }else {
                    this.send_with_card = false;
                }

            }
 
            if(this.send_with_card){
                // console.log("########");
                // console.log(what_card_used[card_index]);
                this.open_payment_wizard(what_card_used[card_index]);
            } else {
                this.proceed_to_usual(force_validation);
            }


        } else {



        }


        
    },

})

});