/* 
  Basic tests for the application 
*/
var Application = require('spectron').Application
var assert = require('assert')

var app = new Application({
    path: '/Users/ambermirza/electron435/main.js'
})

app.start().then(function () {
  // Check if the window is visible
  return app.browserWindow.isVisible()
}).then(function (isVisible) {
  // Verify the window is visible
  assert.equal(isVisible, true)
  console.log("test one working");
}).then(function () {
  // Get the window's title
  return app.client.getTitle()
}).then(function (title) {
  // Verify the window's title
  assert.equal(title, 'Imitation')
  console.log("test two working");
}).then(function () {
  // Stop the application
  return app.stop()
}).catch(function (error) {
  // Log any failures
  console.error('Test failed', error.message)
})