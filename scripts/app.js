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
                $routeProvider.otherwise({ redirectTo: '/' });
            }
        ]
    )

        .directive('inputTask', function () {
            return {
                templateUrl: 'scripts/home/inputTask.html'
            }
        })
        .directive('inputSmile', function () {
            return {
                templateUrl: 'scripts/home/inputSmile.html'
            }
        })
        .directive('inputCauses', function () {
            return {
                templateUrl: 'scripts/home/inputCauses.html'
            }
        })

        .controller('homeController', ['$scope', '$window', function ($scope, $window) {
            $scope.inputTask = true;
            $scope.inputSmile = false;
            $scope.inputCauses = false;

            var reset = function () {
                $scope.inputTask = false;
                $scope.inputSmile = false;
                $scope.inputCauses = false;
            }
            $scope.showInputTask = function () {
                reset();
                $scope.inputTask = true;
            }

            $scope.showInputSmile = function () {
                reset();
                $scope.inputSmile = true;
            }

            $scope.showInputCauses = function () {
                reset();
                $scope.inputCauses = true;
            }

        }]);
})();