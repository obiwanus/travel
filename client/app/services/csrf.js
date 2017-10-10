import Ember from 'ember';
import ENV from 'client/config/environment';

export default Ember.Service.extend({

  ajax: Ember.inject.service(),

  token: null,

  refreshToken() {
    this.get('ajax').GET('/csrf/token/').then((data) => {
      this.set('token', data.csrfmiddlewaretoken);
    }, (xhr) => {
      console.log("Failed to obtain CSRF token: ", xhr);
    });
  },

});
