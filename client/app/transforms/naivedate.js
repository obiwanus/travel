import DS from 'ember-data';
import moment from 'moment';

export default DS.Transform.extend({
  deserialize(serialized) {
    return serialized;
  },

  serialize(deserialized) {
    if (deserialized) {
      return moment.utc(deserialized).format("YYYY-MM-DD")
    } else {
      return deserialized;
    }
  }
});
