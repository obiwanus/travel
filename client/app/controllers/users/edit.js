import Ember from 'ember';
import FormMixin from 'client/mixins/form';


export default Ember.Controller.extend(FormMixin, {

  doSubmit(user) {
    return user.save();
  },

  actions: {
    selectRole(role) {
      this.set('user.role', role);
    },

    save(user) {
      this.submitForm(user).then(() => {
        this.get('messages').success(this, 'User saved');
        this.transitionToRoute('users');
      });
    },
  },

});
