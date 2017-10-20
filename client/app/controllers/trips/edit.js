import Ember from 'ember';
import FormMixin from 'client/mixins/form';

export default Ember.Controller.extend(FormMixin, {

  doSubmit(trip) {
    return trip.save();
  },

  actions: {

    save(trip) {
      this.submitForm(trip).then(() => {
        this.get('messages').success(this, 'Trip has been saved');
        history.back();
      }).catch(() => {});
    },

  },

});
