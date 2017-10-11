import Ember from 'ember';
import Base from 'ember-simple-auth/authenticators/base';


export default Base.extend({

  ajax: Ember.inject.service(),

  // This method is required by ember-simple-auth
  // http://ember-simple-auth.com/api/classes/BaseAuthenticator.html#method_restore
  restore(data) {
    return new Ember.RSVP.Promise(function(resolve, reject) {
      if (!Ember.isEmpty(data)) {
        resolve(data);
      } else {
        reject();
      }
    });
  },

  authenticate(email, password) {
    let data = {
      email: email,
      password: password,
    };
    let ajax = this.get('ajax');
    return new Ember.RSVP.Promise(function(resolve, reject) {
      ajax.POST('/login/', data).then((response) => {
        resolve(response.user);
      }, (xhr) => {
        reject(xhr);
      });
    });
  },

  invalidate() {
    return this.get('ajax').POST('/logout/', {});
  },

});
