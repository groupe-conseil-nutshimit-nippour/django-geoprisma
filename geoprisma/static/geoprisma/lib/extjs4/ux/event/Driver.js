/**
 * This is the base class for {@link Ext4.ux.event.Recorder} and {@link Ext4.ux.event.Player}.
 */
Ext4.define('Ext4.ux.event.Driver', {
    active: null,
    mixins: {
        observable: 'Ext4.util.Observable'
    },

    constructor: function (config) {
        var me = this;

        me.mixins.observable.constructor.apply(this, arguments);

        me.addEvents(
            /**
             * @event start
             * Fires when this object is started.
             * @param {Ext4.ux.event.Driver} this
             */
            'start',

            /**
             * @event stop
             * Fires when this object is stopped.
             * @param {Ext4.ux.event.Driver} this
             */
            'stop'
        );
    },

    getTime: function () {
        return new Date().getTime();
    },

    /**
     * Returns the number of milliseconds since start was called.
     */
    getTimestamp: function () {
        var d = this.getTime();
        return d - this.startTime;
    },

    onStart: function () {},

    onStop: function () {},

    /**
     * Starts this object. If this object is already started, nothing happens.
     */
    start: function () {
        var me = this;

        if (!me.active) {
            me.active = new Date();
            me.startTime = me.getTime();
            me.onStart();
            me.fireEvent('start', me);
        }
    },

    /**
     * Stops this object. If this object is not started, nothing happens.
     */
    stop: function () {
        var me = this;

        if (me.active) {
            me.active = null;
            me.onStop();
            me.fireEvent('stop', me);
        }
    }
});
