import Ember from 'ember';


export default Ember.Service.extend({

  ajax: Ember.inject.service(),

  token: null,

  refreshToken() {
    this.get('ajax').GET('/csrf/token/').then((data) => {
      this.set('token', data.csrfmiddlewaretoken);
    });
  },

});
