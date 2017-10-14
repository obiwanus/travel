import Ember from 'ember';
import FormMixin from 'client/mixins/form';

export default Ember.Controller.extend(FormMixin, {

  actions: {

    reset(email) {
      this.submitForm('/password/reset/', {email: email}).then(() => {
        this.transitionToRoute('login');
      });
    },
  },

});
