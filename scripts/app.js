(function () {
    'use strict';

    var app = angular.module(
        'app',
        [
            'ngRoute',
            'ngMaterial',
            'ngAnimate'
        ]
    );
    app.config(
        [
            '$routeProvider',
            function ($routeProvider) {
                $routeProvider.when(
                    '/', {
                        templateUrl: './scripts/home/home.html',
                        controller: 'homeController'
                    }
                );
                $routeProvider.otherwise({redirectTo: '/'});
            }
        ]
    )
    
    .controller('homeController', ['$scope', '$window', function($scope, $window) {
        $scope.first = true;
        $scope.second = false;

        var reset = function(){
            $scope.first = false;
            $scope.second = false;
        }
        $scope.showFirst = function(){
            reset();
            $scope.first = true;
        }

        $scope.showSecond = function(){
            reset();
            $scope.second = true;
        }
    }])
    
    ;
})();