import Ember from 'ember';

export default Ember.Controller.extend({

  messages: Ember.inject.service(),

  user: {},

  actions: {

    signup(userData) {
      this.set('inProgress', true);
      this.set('formErrors', null);
      let user = this.get('store').createRecord('user', userData);
      user.save().then((response) => {
        this.get('messages').success(this, "Your account has been created. Please check your email");
        this.set('user', {});  // clear form
        this.transitionToRoute('login');
      }).catch((response) => {
        this.set('formErrors', response.errors);
        user.deleteRecord();
      }).finally(() => {
        this.set('inProgress', false);
      });
    },
  },

});
