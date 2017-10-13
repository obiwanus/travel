import Ember from 'ember';

export default Ember.Controller.extend({

  messages: Ember.inject.service(),

  user: {},

  actions: {
    selectRole(role) {
      this.set('user.role', role);
    },

    save(user) {
      this.set('inProgress', true);
      this.set('formErrors', null);
      user.save().then(() => {
        this.get('messages').success(this, 'User saved');
        this.transitionToRoute('users');
      }).catch((response) => {
        this.set('formErrors', response.errors);
      }).finally(() => {
        this.set('inProgress', false);
      });
    },
  },

});
