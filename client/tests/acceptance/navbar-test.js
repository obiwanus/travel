import { test } from 'qunit';
import moduleForAcceptance from 'client/tests/helpers/module-for-acceptance';

moduleForAcceptance('Acceptance | navbar');

test('admins can see admin links', function(assert) {
  loginAs('admin');

  andThen(function() {
    assert.equal(find('nav a:contains("All trips")').length, 1);
    assert.equal(find('nav a:contains("Users")').length, 1);
    assert.equal(find('nav a:contains("Logout")').length, 1);
  });
});

test('user managers can see users link', function(assert) {
  loginAs('user manager');

  andThen(function() {
    assert.equal(find('nav a:contains("All trips")').length, 0);
    assert.equal(find('nav a:contains("Users")').length, 1);
    assert.equal(find('nav a:contains("Logout")').length, 1);
  });
});

test('normal users cant see anything', function(assert) {
  loginAs('normal user');

  andThen(function() {
    assert.equal(find('nav a:contains("All trips")').length, 0);
    assert.equal(find('nav a:contains("Users")').length, 0);
    assert.equal(find('nav a:contains("Logout")').length, 1);
  });
});
