import Ember from 'ember';
import FormMixin from 'client/mixins/form';

export default Ember.Controller.extend(FormMixin, {

  trip: {},

  doSubmit(trip) {
    return trip.save();
  },

  actions: {

    save(tripData) {
      let trip = this.get('store').createRecord('trip', tripData);
      this.submitForm(trip).then(() => {
        this.get('messages').success(this, 'Trip has been added');
        this.set('trip', {});  // clear form
        history.back();
      }).catch(() => {
        trip.deleteRecord();
      });
    },

  },

});
