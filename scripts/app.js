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
    .directive('actionParameters', function () {
        return {
            templateUrl: 'scripts/home/actionParameters.html'
        }
    })
    .directive('causalParameters', function () {
        return {
            templateUrl: 'scripts/home/causalParameters.html'
        }
    })
    .directive('preview', function () {
        return {
            templateUrl: 'scripts/home/preview.html'
        }
    })

    .controller('homeController', ['$scope', '$window', function ($scope, $window) {
        $(document).ready(function () {
            $scope.inputTask = true;
            $scope.inputSmile = false;
            $scope.inputCauses = false;
            $scope.builder = false;
            $scope.relationship = false;
            $scope.actionParameters = false;
            $scope.causalParameters = false;


            $scope.knowledgeAdded = false;

            var reset = function () {
                $scope.inputTask = false;
                $scope.inputSmile = false;
                $scope.inputCauses = false;
                $scope.builder = false;
                $scope.relationship = false;
                $scope.actionParameters = false;
                $scope.causalParameters = false;
                $scope.preview = false;
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

            $scope.showActionParameters = function () {
                reset()
                $scope.actionParameters = true;
            }

            $scope.showPreview = function(){
                reset()
                $scope.preview = true;
            }

            function unique(list) {
                var result = [];
                $.each(list, function(i, e) {
                    if ($.inArray(e, result) == -1) result.push(e);
                });
                return result;
            }

            $scope.showCausalParameters = function () {
                reset()
                $scope.paramList = [];
                var temp = [];
                $scope.causalParameters = true;
                $scope.knowledge.forEach(function(item) {
                    temp = []
                    item.actions.forEach(function(action){
                        action.params.forEach(function(param){
                            //temp.push(action.action + " - " + param.value)
                            temp.push(param.value)    
                        })                        
                    })
                    temp = unique(temp)
                    $scope.paramList.push(temp)
                });
            }

            // For Actions / Causes

            //ex
            // knowledge = [
            //     {
            //         cause: "moveTo", 
            //         relationship: {
            //             type: "Direct",
            //             condition: ""
            //         },
            //         parameters: ["obj", "dest", "dx", "dy", "dz", "da"], 
            //         actions: [
            //             {
            //                 action: "grasp", 
            //                 params: ["obj"]
            //             },
            //             {
            //                 action: "release",
            //                 params: ["obj", "dest", "dx", "dy", "dz", "da"]
            //             }
            //         ]
                    
            //     },
            //     {
            //         cause: "stack", 
            //         relationship: {
            //             type: "Conditional",
            //             condition: "TYPE(obj1) = block"
            //         },
            //         parameters: ["dest", "dx", "dy", "dz", "da", "obj"], 
            //         actions: [
            //             {
            //                 action: "moveTo", 
            //                 params: ["obj", "dest", "dx", "dy", "dz", "da"]
            //             },
            //         ]
            //     },
            // ]

            $scope.knowledge = [
                {
                    cause: "Enter Cause",
                    relationship: {
                        type: "",
                        condition: ""
                    },
                    parameters: [],
                    actions: []
                }
            ]

            $scope.buildString = function(){
                var final = "RULES { "
                $scope.knowledge.forEach(function(cause) {
                    if(cause.relationship.type === "Conditional"){
                        final = final + "if(" + cause.relationship.condition + "):"
                    }
                    final = final + cause.cause + "("
                    cause.parameters.forEach(function(param) {
                       final = final + param.param + "," 
                    });
                    final = final.slice(0,-1)
                    final = final + ") := "
                    cause.actions.forEach(function(action) {
                        final = final + action.action + "("
                        action.params.forEach(function(param) {
                            final = final +  param.value + ","
                        });
                        final = final.slice(0,-1)
                        final = final + "),"
                    });
                    final = final.slice(0,-1)
                    final = final + ";"
                });
                final = final + " }"
                console.log(final)
            }

            $scope.addCause = function () {
                var item = {
                     cause: "Enter Cause",
                    relationship: { type: "", condition: "" },
                    parameters: [],
                    actions: []
                }
                $scope.knowledge.push(item);
            }

            $scope.removeCause = function () {
                $scope.knowledge.pop();
            }

            $scope.addAction = function (index) {
                $scope.knowledge[index].actions.push({ action: "Enter Action", params: [] })
            }

            $scope.removeAction = function (index) {
                $scope.knowledge[index].actions.pop()
            }

            $scope.addCausalParameter = function (index) {
                $scope.knowledge[index].parameters.push({ action: "", param: "" })
            }

            $scope.removeCausalParameter = function (index) {
                $scope.knowledge[index].parameters.pop()
            }

            $scope.addActionParameter = function (parentIndex, index) {
                $scope.knowledge[parentIndex].actions[index].params.push({ type: "", value: "" })
            }

            $scope.removeActionParameter = function (parentIndex, index) {
                $scope.knowledge[parentIndex].actions[index].params.pop()
            }

            $scope.defaultActions = ['release', 'grab', 'move']

            $scope.setParams = function (parentIndex, item) {
                var actions = []
                $scope.knowledge[parentIndex].actions.forEach(function (x) {
                    actions.push(x.action);
                });
                var index = actions.indexOf(item);
                $scope.causalParamList = $scope.knowledge[parentIndex].actions[index].params
            }
        })
        
        $scope.smileRecordings = function(element){
            $scope.recordings = []
            var myFiles = element.files
            var i = 0;
            for(i; i < myFiles.length; i++){
                $scope.recordings.push(myFiles[i].name)
            }
            console.log($scope.recordings)
            $scope.$apply()

        }

        $scope.addKnowledge = function(element){
            console.log("asd")
            console.log(element)
            console.log('files:', element.files);
            $scope.knowledgeAdded = true
            var file = element.files[0]
            $scope.knowledgeFileName = file.name
            console.log($scope.knowledgeFileName)
            $scope.$apply()

        }

        $scope.thingsYouCanDo = [
            {
                name: "grasp",
                params: ["obj"]
            },
            {
                name: "release",
                params: ["obj", "dest", "dx", "dy", "dz", "da"]
            }
        ]

    }]);
})();