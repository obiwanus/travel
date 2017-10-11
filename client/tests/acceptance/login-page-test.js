import { test } from 'qunit';
import moduleForAcceptance from 'client/tests/helpers/module-for-acceptance';

moduleForAcceptance('Acceptance | login page');

test('if not authenticated then redirects to login', function(assert) {
  visit('/');

  andThen(function() {
    assert.equal(currentURL(), '/login');
  });
});

test('Can login as normal user', function(assert) {
  loginAs('normal user');

  andThen(function() {
    assert.equal(currentURL(), '/');
  });
});
