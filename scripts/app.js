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
        .directive('review', function () {
            return {
                templateUrl: 'scripts/home/review.html'
            }
        })
        .directive('xmlPage', function () {
            return {
                templateUrl: 'scripts/home/xmlPage.html'
            }
        })
        .directive('final', function () {
            return {
                templateUrl: 'scripts/home/final.html'
            }
        })
        .directive('builderReview', function () {
            return {
                templateUrl: 'scripts/home/builderReview.html'
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
                $scope.preview = false;
                $scope.review = false;
                $scope.finalPage = false;
                $scope.builderReview = false;

                $scope.knowledgeAdded = false;
                $scope.run = false
                $scope.recordings = []
                $scope.goClass = "ui green button"
                $scope.error = ""
                $scope.createXML = ""
                $scope.showCustom = false;
                $scope.customClass = "ui grey button"

                var reset = function () {
                    $scope.inputTask = false;
                    $scope.inputSmile = false;
                    $scope.inputCauses = false;
                    $scope.builder = false;
                    $scope.relationship = false;
                    $scope.actionParameters = false;
                    $scope.causalParameters = false;
                    $scope.preview = false;
                    $scope.review = false;
                    $scope.xmlPage = false;
                    $scope.finalPage = false;
                    $scope.builderReview = false;
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

                $scope.showPreview = function () {
                    reset()
                    $scope.preview = true;
                }

                $scope.showReview = function () {
                    reset()
                    $scope.goClass = "ui green button"
                    $scope.error = ""
                    $scope.review = true;
                }

                $scope.showXML = function () {
                    reset()
                    $scope.xmlPage = true
                }

                $scope.showFinal = function () {
                    reset()
                    $scope.finalPage = true;
                }

                $scope.showBuilderReview = function(){
                    reset()
                    $scope.builderReview = true;
                }

                $scope.startOver = function () {
                    window.location.reload(false)

                }

                $scope.openPreview = function () {
                    const { shell } = require('electron')
                    shell.openExternal('https://ambermirza.github.io/preview/')
                }

                $scope.inputtedTask = ""

                function unique(list) {
                    var result = [];
                    $.each(list, function (i, e) {
                        if ($.inArray(e, result) == -1) result.push(e);
                    });
                    return result;
                }

                $scope.buildPathString = function () {
                    $scope.pathString = ""
                    $scope.recordings.forEach(function (x) {
                        $scope.pathString = $scope.pathString + x.path + ","
                    });
                    $scope.pathString = $scope.pathString.slice(0, -1);
                }

                $scope.showCausalParameters = function () {
                    reset()
                    $scope.causalParameters = true;
                    $scope.createParamList();
                }

                $scope.toggleCustom = function(){
                    if($scope.showCustom){
                        $scope.showCustom = false;
                        $scope.customClass = "ui grey button"
                    }else{
                        $scope.showCustom = true;
                        $scope.customClass = "ui green button"
                    }
                }

                $scope.createParamList = function(){
                    $scope.paramList = [];
                    var temp = [];
                    $scope.causalParameters = true;
                    $scope.knowledge.forEach(function (item) {
                        temp = []
                        item.actions.forEach(function (action) {
                            action.params.forEach(function (param) {
                                temp.push(param.value)
                            })
                        })
                        $scope.customParams.forEach(function(param) {
                            temp.push(param.value)
                        });
                        temp = unique(temp)
                        $scope.paramList.push(temp)
                    });
                }

                // For Actions / Causes

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
                $scope.buildString = function () {
                    var final = "RULES { "
                    $scope.knowledge.forEach(function (cause) {
                        if (cause.relationship.type === "Conditional") {
                            final = final + "if(" + cause.relationship.condition + "):"
                        }
                        final = final + cause.cause + "("
                        cause.parameters.forEach(function (param) {
                            final = final + param.param + ","
                        });
                        final = final.slice(0, -1)
                        final = final + ") := "
                        cause.actions.forEach(function (action) {
                            final = final + action.action + "("
                            action.params.forEach(function (param) {
                                final = final + param.value + ","
                            });
                            final = final.slice(0, -1)
                            final = final + "),"
                        });
                        final = final.slice(0, -1)
                        final = final + ";"
                    });
                    final = final.slice(0, -1)
                    final = final + " }"
                    console.log(final)
                    return final;
                }

                $scope.downloadContent = function() {
                    var atag = document.createElement("a");
                    var content = $scope.buildString();
                    var file = new Blob([content], {type: 'text/plain'});
                    atag.href = URL.createObjectURL(file);
                    atag.download = $scope.inputtedTask + "_knowledge.txt";
                    atag.click();
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

                $scope.customParams = []

                $scope.addCustomParam = function(){
                    $scope.customParams.push({value: ""})
                }

                $scope.removeCustomParam = function(){
                    $scope.customParams.pop()
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


                $scope.smileRecordings = function (element) {
                    $scope.recordings = []
                    var myFiles = element.files
                    console.log(myFiles)
                    var i = 0;
                    for (i; i < myFiles.length; i++) {
                        $scope.recordings.push({ name: myFiles[i].name, path: myFiles[i].path })
                    }
                    $scope.$apply()

                }

                $scope.addKnowledge = function (element) {
                    $scope.knowledgeAdded = true
                    var file = element.files[0]
                    console.log(file)
                    $scope.knowledgeFile = { name: file.name, path: file.path }
					
                    $scope.$apply()
                }

                $scope.setParams = function (parentIndex, item) {
                    var actions = []
                    $scope.knowledge[parentIndex].actions.forEach(function (x) {
                        actions.push(x.action);
                    });
                    var index = actions.indexOf(item);
                    $scope.causalParamList = $scope.knowledge[parentIndex].actions[index].params
                }
            })

            $scope.smileRecordings = function (element) {
                $scope.recordings = []
                var myFiles = element.files
                console.log(myFiles)
                var i = 0;
                for (i; i < myFiles.length; i++) {
                    $scope.recordings.push({ name: myFiles[i].name, path: myFiles[i].path })
                }
                $scope.$apply()

            }

            $scope.XMLInput = function (element) {
                var file = element.files[0]
                console.log(file)
                $scope.inputXML = ""
                $scope.inputXML = file.path
                $scope.xml = { name: file.name, path: file.path }
                $scope.run = true
                $scope.$apply()
            }

            $scope.go = function () {
                $scope.goClass = "ui green button"
                $scope.error = ""
                if ($scope.recordings.length == 0) {
                    $scope.goClass = "ui red button"
                    $scope.error = "No SMILE Recordings"
                    return;
                }
                $scope.buildPathString();
                console.log($scope.pathString)
                console.log($scope.inputXML)
                var util = require("util");
                var spawn1 = require("child_process").spawn;
                //var process1 = spawn('python',["final_imitation.py",$scope.pathString,$scope.inputXML,test]);
                
                console.log("I am calling run.py");
                var process1 = spawn1('python', ["./python_causal_compiler/compiler/run.py",$scope.knowledgeFile.path, "Dummy"])
                process1.stderr.on('data',function(chunk){ //debugging info, prints out stuff python puts in stdout

                    var textChunk = chunk.toString('utf8');// buffer to string

                    util.log(textChunk);
                });
                
                setTimeout(function () {
					console.log("Calling imitation")
                    var process = spawn1('python', ["./python_causal_compiler/compiler/output/imitation.py", $scope.pathString, $scope.inputXML]);
					process.stderr.on('data',function(chunk){ //debugging info, prints out stuff python puts in stdout

						var textChunk = chunk.toString('utf8');// buffer to string

						util.log(textChunk);
					});
                    
                }, 5000);
				$scope.showFinal();
                //var spawn = require("child_process").spawn;
                //var test = "test.xml"

            }

            $scope.createXmlFile = function (element) {
                var file = element.files[0]
                $scope.createdXML = ""
                $scope.createdXML = file.path
                $scope.createXML = { name: file.name, path: file.path }
                $scope.$apply()
            }

            $scope.generateXML = function () {
                var util = require("util");
                var spawn = require("child_process").spawn;
                var process = spawn('python', ["./userinputToXML/createUserInputXML.py", $scope.createXML.path]);

                $scope.createXML = ""
            }
        }]);
})();