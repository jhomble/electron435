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
            $(document).ready(function () {
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

                $scope.showBuilder = function () {
                    reset();
                    $scope.builder = true;
                }

                $scope.showRelationship = function () {
                    reset();
                    $scope.relationship = true;
                }

                $scope.showParameters = function () {
                    reset()
                    $scope.parameters = true;
                }
                // For Actions / Causes

                $scope.knowledge = [
                    {
                        cause: "Enter Cause",
                        relationship: {},
                        parameters: [],
                        actions: []
                    }
                ]

                $scope.addCause = function () {
                    var item = {
                        cause: "Enter Cause",
                        relationship: {},                        
                        parameters: [],
                        actions: []
                    }
                    $scope.knowledge.push(item);
                }

                $scope.removeCause = function () {
                    $scope.knowledge.pop();
                }

                $scope.addAction = function (index) {
                    $scope.knowledge[index].actions.push({ action: "Enter Action", params: []})
                }

                $scope.removeAction = function (index) {
                    $scope.knowledge[index].actions.pop()
                }

                $scope.addActionParameter = function (parentIndex, index) {
                    $scope.knowledge[parentIndex].actions[index].params.push({ type: "", value: "" })
                    console.log($scope.knowledge)
                }

                $scope.removeActionParameter = function (parentIndex, index) {
                    $scope.knowledge[parentIndex].actions[index].params.pop()
                }
                
                $scope.defaultActions = ['release', 'grab', 'move']

            })

        }]);
})();