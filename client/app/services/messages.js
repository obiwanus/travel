import Ember from 'ember';


export default Ember.Service.extend({

  send(obj, type, message, timeout) {
    Ember.get(obj, 'flashMessages').add({
      message: message,
      type: type,
      timeout: timeout || 10000,
    });
  },

  success(obj, message, timeout) {
    this.send(obj, 'success', message, timeout);
  },

  error(obj, message, timeout) {
    this.send(obj, 'error', message, timeout);
  },

  warning(obj, message, timeout) {
    this.send(obj, 'warning', message, timeout);
  },

  info(obj, message, timeout) {
    this.send(obj, 'info', message, timeout);
  },

});
