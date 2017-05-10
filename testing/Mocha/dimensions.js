/* 
GUI is able to adapt to different screen dimensions and user’s prefered window position.
*/
var should = require('should');

module.exports = function(win, view) {

    describe('main.js', function() {

        describe('#myView', function() {

            it('exists', function(){
                should.exist(view);
                view.id.should.equal('myView');
            });

            it('has Ti.UI.View functions', function() {
                should(view.add).be.a.Function;
            });

            it('is a child of window', function() {
                win.children.length.should.equal(1);
                should.exist(win.children[0]);
                win.children[0].id.should.equal('myView');
            });

            it('view has same dimensions as window', function(){
                view.size.height.should.equal(win.size.height);
                view.size.width.should.equal(win.size.width);
            });

        });
    });
    
    // run the tests
    mocha.run();
};