import Ember from 'ember';

export default Ember.Controller.extend({
  user: Ember.inject.service(),

  email: null,
  first_name: null,
  last_name: null,
  role: null,

  availableRoles: Ember.computed('user.isAdmin', function () {
    let roles = ['Normal user', 'User manager'];
    if (this.get('user.isAdmin')) {
      roles.push('Administrator');
    }
    return roles;
  }),

  clearForm() {
    this.set('email', null);
    this.set('first_name', null);
    this.set('last_name', null);
    this.set('role', null);
  },

  actions: {
    selectRole(role) {
      this.set('role', role);
    },

    save() {
      this.set('formErrors', null);
      let newUser = this.get('store').createRecord('user', {
        email: this.get('email'),
        first_name: this.get('first_name'),
        last_name: this.get('last_name'),
        role: this.get('role'),
      });
      newUser.save().then(() => {
        this.clearForm();
        this.transitionToRoute('users');
      }).catch((response) => {
        this.set('formErrors', response.errors);
        newUser.deleteRecord();
      });
    },
  },

});
