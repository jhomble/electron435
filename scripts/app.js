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

        // All .directives are the html segments. 
        // directives were made so each segment could have its own html

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

        // Controller for the entire application
        .controller('homeController', ['$scope', '$window', function ($scope, $window) {
            $(document).ready(function () {
                // these $scope variables are for hiding and showing each segment
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

                // these $scope variables are flags or ng-class options
                $scope.knowledgeAdded = false;
                $scope.run = false
                $scope.recordings = []
                $scope.goClass = "ui green button"
                $scope.error = ""
                $scope.createXML = ""
                $scope.showCustom = false;
                $scope.customClass = "ui grey button"

                // Called when switching directives. Set all directive show flags to false
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

                // function to eliminate duplicates in an array. (ng-repeat doesnt allow dups)
                function unique(list) {
                    var result = [];
                    $.each(list, function (i, e) {
                        if ($.inArray(e, result) == -1) result.push(e);
                    });
                    return result;
                }


                // All show functions are switching from one directive to another
                // All show functions reset all flags to false and set its flag to true
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
                // The goClass is a ng-class variable
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

                $scope.showBuilderReview = function () {
                    reset()
                    $scope.builderReview = true;
                }

                $scope.showCausalParameters = function () {
                    reset()
                    $scope.causalParameters = true;
                    $scope.createParamList();
                }

                // Resets the application on click - equivalent to refreshing the page
                $scope.startOver = function () {
                    window.location.reload(false)
                }

                // Not used currently, but would open an external web page for a preview
                $scope.openPreview = function () {
                    const { shell } = require('electron')
                    shell.openExternal('https://ambermirza.github.io/preview/')
                }

                $scope.inputtedTask = ""

                // Given the SMILE text recordings. This function iterates through all, 
                // and creates a CSV string of the paths and puts them into the pathString variable
                $scope.buildPathString = function () {
                    $scope.pathString = ""
                    $scope.recordings.forEach(function (x) {
                        $scope.pathString = $scope.pathString + x.path + ","
                    });
                    $scope.pathString = $scope.pathString.slice(0, -1);
                }

                // this functions purpose is to toggle the custom parameter button css
                $scope.toggleCustom = function () {
                    if ($scope.showCustom) {
                        $scope.showCustom = false;
                        $scope.customClass = "ui grey button"
                    } else {
                        $scope.showCustom = true;
                        $scope.customClass = "ui green button"
                    }
                }

                // This function generates an array for each cause.
                // the array will contain all parameters its actions had as well as the custom parameter list
                // the paramList variable will be used to make the drop down boxes for the causalParameter page
                $scope.createParamList = function () {
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
                        $scope.customParams.forEach(function (param) {
                            temp.push(param.value)
                        });
                        temp = unique(temp)
                        $scope.paramList.push(temp)
                    });
                }

                // knowledge is a variable containing the knowledge base of the new task
                // it is whats being update with new actions/causes/parameters/relationships
                $scope.knowledge = [
                    {
                        cause: "",
                        relationship: {
                            type: "",
                            condition: ""
                        },
                        parameters: [],
                        actions: []
                    }
                ]

                // adds a new cause to knowledge
                $scope.addCause = function () {
                    var item = {
                        cause: "",
                        relationship: { type: "", condition: "" },
                        parameters: [],
                        actions: []
                    }
                    $scope.knowledge.push(item);
                }

                // removes a cause from knowledge
                $scope.removeCause = function () {
                    $scope.knowledge.pop();
                }

                // adds a new action to the associated cause at index
                $scope.addAction = function (index) {
                    $scope.knowledge[index].actions.push({ action: "", params: [] })
                }

                // removes a action to the associates cause at index
                $scope.removeAction = function (index) {
                    $scope.knowledge[index].actions.pop()
                }

                // adds a new causal parameter at the associated cause at index
                $scope.addCausalParameter = function (index) {
                    $scope.knowledge[index].parameters.push({ action: "", param: "" })
                }

                // removes a causal parameter at the associated cause at index
                $scope.removeCausalParameter = function (index) {
                    $scope.knowledge[index].parameters.pop()
                }

                // adds a new action parameter at the cause at parentIndex and action at index
                $scope.addActionParameter = function (parentIndex, index) {
                    $scope.knowledge[parentIndex].actions[index].params.push({ type: "", value: "" })
                }

                // removes a action parameter at the cause at parentIndex and action at index
                $scope.removeActionParameter = function (parentIndex, index) {
                    $scope.knowledge[parentIndex].actions[index].params.pop()
                }

                // variable holding all custom parameters
                $scope.customParams = []

                // adds a new custom parameter 
                $scope.addCustomParam = function () {
                    $scope.customParams.push({ value: "" })
                }

                // removes a custom parameter
                $scope.removeCustomParam = function () {
                    $scope.customParams.pop()
                }

                // This function parses through the knowledge variable and returns
                // the string that is formatted to our language
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

                // This function calls buildString to create the text
                // it then opens a browser for the user to save the string in a text file
                $scope.downloadContent = function () {
                    var atag = document.createElement("a");
                    var content = $scope.buildString();
                    var file = new Blob([content], { type: 'text/plain' });
                    atag.href = URL.createObjectURL(file);
                    atag.download = $scope.inputtedTask + "_knowledge.txt";
                    atag.click();
                }

                // Opens a file browser for input of smile recordings
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

                // Opens a browser for the user to load the knowledge base file
                $scope.addKnowledge = function (element) {
                    $scope.knowledgeAdded = true
                    var file = element.files[0]
                    console.log(file)
                    $scope.knowledgeFile = { name: file.name, path: file.path }
                    $scope.$apply()
                }

                // Opens a browser for the user to load the initial XML state 
                $scope.XMLInput = function (element) {
                    var file = element.files[0]
                    console.log(file)
                    $scope.inputXML = ""
                    $scope.inputXML = file.path
                    $scope.xml = { name: file.name, path: file.path }
                    $scope.run = true
                    $scope.$apply()
                }

                // this function takes all inputs and runs the python scripts to compile the 
                // knowledge base, parse the smile recordings, and run the imitiation algorithm
                $scope.go = function () {
                    // Initial ng-class and error checking
                    $scope.goClass = "ui green button"
                    $scope.error = ""
                    if ($scope.recordings.length == 0) {
                        $scope.goClass = "ui red button"
                        $scope.error = "No SMILE Recordings"
                        return;
                    }
                    $scope.buildPathString();
                    $scope.error1 = ""
                    $scope.error2 = ""
                    //console.log($scope.pathString)
                    //console.log($scope.inputXML)
                    // Run python scripts
                    var util = require("util");
                    var spawn1 = require("child_process").spawn;
                    //var process1 = spawn('python',["final_imitation.py",$scope.pathString,$scope.inputXML,test]);

                    var process1 = spawn1('python', ["./python_causal_compiler/compiler/run.py", $scope.knowledgeFile.path, "Dummy"])
                    process1.stdout.on('data', function (chunk) { //debugging info, prints out stuff python puts in stdout
                        console.log("asd")
                        $scope.error1 = chunk.toString('utf8');// buffer to string
                        console.log($scope.error1.length)
                        console.log($scope.error1);
                        $scope.$apply()
                    });

                    setTimeout(function () {
                        console.log("asdasdasd")
                        var process = spawn1('python', ["./python_causal_compiler/compiler/output/imitation.py", $scope.pathString, $scope.inputXML]);
                        process.stdout.on('data', function (chunk) { //debugging info, prints out stuff python puts in stdout
                            console.log("123")
                            $scope.error2 = chunk.toString('utf8');// buffer to string
                            console.log($scope.error2.length)
                            console.log($scope.error2);
                            $scope.$apply()
                        });

                    }, 5000);
                    $scope.showFinal();
                    //var spawn = require("child_process").spawn;
                    //var test = "test.xml"

                }

                // Opens a file browser for user to load in XML text file
                $scope.createXmlFile = function (element) {
                    var file = element.files[0]
                    $scope.createdXML = ""
                    $scope.createdXML = file.path
                    $scope.createXML = { name: file.name, path: file.path }
                    $scope.$apply()
                }

                // Takes the file chosen in createXmlFile and generates the xml
                $scope.generateXML = function () {
                    var util = require("util");
                    var spawn = require("child_process").spawn;
                    var process = spawn('python', ["./userinputToXML/createUserInputXML.py", $scope.createXML.path]);

                    $scope.createXML = ""
                }
            })
        }]);
})();