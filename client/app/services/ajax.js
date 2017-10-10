import Ember from 'ember';
import ENV from 'client/config/environment';

export default Ember.Service.extend({

  csrf: Ember.inject.service(),

  GET(url) {
    return new Ember.RSVP.Promise((resolve, reject) => {
      Ember.$.ajax({
        type: "GET",
        url: this.sanitized_url(url),
        crossDomain: true,
        xhrFields: {
          withCredentials: true
        }
      }).done((response) => {
        Ember.run(() => {
          resolve(response);
        });
      }).fail((xhr) => {
        Ember.run(() => {
          reject(xhr);
        });
      });
    });
  },

  POST(url, data) {
    return this.sendData(url, data, 'POST');
  },

  PUT(url, data) {
    return this.sendData(url, data, 'PUT');
  },

  sendData(url, data, type) {
    const csrfToken = this.get('csrf.token');
    return new Ember.RSVP.Promise((resolve, reject) => {
      Ember.$.ajax({
        type: type,
        url: this.sanitized_url(url),
        data: data,
        xhrFields: {
          withCredentials: true
        },
        crossDomain: true,
        headers: {
          'X-CSRFToken': csrfToken,
        }
      }).done((response) => {
        Ember.run(() => {
          resolve(response);
        });
      }).fail((xhr) => {
        Ember.run(() => {
          reject(xhr);
        });
      });
    });
  },

  sanitized_url(url) {
    if (url.indexOf('http') == 0) {
      return url;
    } else {
      return `${ENV.APP.API_HOST}/api/` + url;
    }
  },

});
