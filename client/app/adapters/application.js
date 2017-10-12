import Ember from 'ember';
import DS from 'ember-data';
import ENV from 'client/config/environment';

Ember.$.ajaxSetup({
  xhrFields: {
    withCredentials: true
  },
  crossDomain: true,
});

export default DS.RESTAdapter.extend({
  host: ENV.APP.API_HOST,
  csrf: Ember.inject.service(),
  namespace: 'api',
  headers: Ember.computed('csrf.token', function () {
    return {
      "X-CSRFToken": this.get('csrf.token')
    };
  }),

  buildURL(modelName, id, snapshot, requestType, query) {
    let url = this._super(...arguments);
    if (url.charAt(url.length - 1) !== '/') {
      url += '/';
    }
    return url;
  }
});
