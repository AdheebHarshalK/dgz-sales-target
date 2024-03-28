/** @odoo-module **/
import core from 'web.core';
import SystrayMenu from 'web.SystrayMenu';
import Widget from 'web.Widget';

const qweb = core.qweb;

const SystrayWidget = Widget.extend({
    template: 'SystrayTarget',
    events: {
        'click .o-dropdown': '_onClick',
    },
    _onClick: function(ev){
        let dropBox = $(ev.currentTarget.parentElement).find('#systray_notif');
        if (dropBox[0].style.display == 'block'){
            dropBox[0].style.display = 'none';
        } else {
            dropBox[0].style.display = 'block';
        }
        ev.stopPropagation();
    },
    init: function (parent, options) {
        this._super.apply(this, arguments);
        var self = this;

        function fetchAndUpdate() {
            self._rpc({
                model: 'custom.login',
                method: 'get_user_details',
            }).then(function (data) {
                if (data.target_count > 0) {
                    $('.systray_notification').html((qweb.render("SystrayDetails", {user_details: data})));
                    $('.target_count').show();
                    $('.target_count').text(data.target_count);
                      if (data.target_amount <= data.target_achieved_amount) {
                        $('.target_count').css('background-color', 'rgb(40, 167, 69)');
                    } else {
                        $('.target_count').css('background-color', 'red');
                    }
                } else {
                    $('.systray_notification').html("<div class='no-target-message'>No current target for you</div>");
                    $('.target_count').hide();
                }
            });
        }


        fetchAndUpdate();

        setInterval(fetchAndUpdate, 5000);

        $(document).on('click', function(ev) {
            if (!$(ev.target).closest('.o-dropdown').length) {
                $('#systray_notif').hide();
            }
        });
    },
});

SystrayMenu.Items.push(SystrayWidget);
export default SystrayWidget;
