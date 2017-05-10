/* 
GUI will adjust to addition and removals of constraints by the user.
*/

var Application = require('..').Application
var assert = require('assert')
var fs = require('fs')
var helpers = require('./global-setup')
var path = require('path')
var temp = require('temp').track()

var describe = global.describe
var it = global.it
var expect = require('chai').expect

describe('application loading', function () {
  helpers.setupTimeout(this)

  var app = null
  var tempPath = null


  /****************** START() *********************/
  describe('start()', function () {
    it('rejects with an error if the application does not exist', function () {
      return new Application({
      		path: path.join(__dirname, 'invalid')}).start().should.be.rejectedWith(Error)
    })

    it('rejects with an error if ChromeDriver doesnt start within the given time', function () {
      return new Application({
      		path: helpers.getElectronPath(), host: 'bad.host', startTimeout: 150}).start().should.be.rejectedWith(Error, 'Chrome Driver didnt start within given time')
    })
  })

  /****************** STOP() *********************/
  describe('stop()', function () {
    it('quits the application', function () {
      var qPath = path.join(tempPath, 'quit.txt')
      assert.equal(fs.existsSync(qPath), false)
      
      return app.stop().then(function (stoppedApp) {
        assert.equal(stoppedApp, app)
        assert.equal(fs.existsSync(qPath), true)
        assert.equal(app.isRunning(), false)
      })
    })

    it('rejects with an error if the application is not running', function () {
      return app.stop().should.be.fulfilled.then(function () {
        return app.stop().should.be.rejectedWith(Error)
      })
    })
  })

  /****************** GETSETTINGS() *********************/
  describe('getSettings()', function () {
    it('returns an object with all the configured options', function () {
      expect(app.getSettings().port).to.equal(9515)
      expect(app.getSettings().quitTimeout).to.equal(1000)
      expect(app.getSettings().env.SPECTRON_TEMP_DIR).to.equal(tempPath)
    })
  })

})