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
        .directive('builder', function () {
            return {
                templateUrl: 'scripts/home/builder.html'
            }
        })
        .directive('relationship', function () {
            return {
                templateUrl: 'scripts/home/relationship.html'
            }
        })
        .directive('parameters', function () {
            return {
                templateUrl: 'scripts/home/parameters.html'
            }
        })

        .controller('homeController', ['$scope', '$window', function ($scope, $window) {
            

            $scope.inputTask = true;
            $scope.inputSmile = false;
            $scope.inputCauses = false;
            $scope.builder = false;
            $scope.relationship = false;
            $scope.parameters = false;

            var reset = function () {
                $scope.inputTask = false;
                $scope.inputSmile = false;
                $scope.inputCauses = false;
                $scope.builder = false;
                $scope.relationship = false;
                $scope.parameters = false;
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

            $scope.showBuilder = function(){
                reset();
                $scope.builder = true;
            }

            $scope.showRelationship = function(){
                reset();
                $scope.relationship = true;
            }

            $scope.showParameters = function(){
                reset()
                $scope.parameters = true;
            }
            // For Actions / Causes
            
            $scope.knowledge = [
                {
                    action: "Enter Action", 
                    parameters: [
                        {
                            type: "", 
                            value: ""
                        }
                    ],
                    causes: [
                        {
                            cause: "Enter Cause", 
                            relationship: "Direct"
                        }
                    ]
                }
            ]

            $scope.addAction = function(){
                var item = {
                    action: "Enter Action", 
                    causes: [
                        {
                            cause: "Enter Cause", 
                            relationship: "Direct"
                        }
                    ]
                }
                $scope.knowledge.push(item);
            }

            $scope.addCause = function(index){
                $scope.knowledge[index].causes.push({cause:"Enter Cause", relationship: "Direct"})
            }
            $scope.addParameter = function(index){
                $scope.knowledge[index].parameters.push({type:"", value: ""})
            }
        }]);
})();