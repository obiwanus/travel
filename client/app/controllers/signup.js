import Ember from 'ember';
import FormMixin from 'client/mixins/form';

export default Ember.Controller.extend(FormMixin, {

  user: {},

  doSubmit(user) {
    return user.save();
  },

  actions: {

    signup(userData) {
      let user = this.get('store').createRecord('user', userData);
      this.submitForm(user).then(() => {
        this.get('messages').success(this, "Your account has been created. Please check your email");
        this.set('user', {});  // clear form
        this.transitionToRoute('login');
      }).catch(() => {
        user.deleteRecord();
      });
    },
  },

});
