/* 
Mac OSX users will not run into notification errors after successful passing of growl tests
*/

var growl = require('./lib/growl')

var Application = require('spectron').Application
var assert = require('assert')

var app = new Application({
    path: '/Users/ambermirza/electron435/main.js'
})

app.start();

growl('New mail!')
growl('5 new messages', { title: 'Email Client', image: 'Safari', sticky: true })
growl('Message with no subject', { title: 'No Subject'})
growl('Set priority', { priority: 2 })
growl('Show icon', { image: 'Safari' })

growl('Allow notifiers', { exec: 'echo XXX %s' }, function(error, stdout, stderr) {
  console.log(stdout);
})
