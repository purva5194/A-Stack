var app = angular.module('app',[]);

//dashboard
app.controller('DashboardController', ['$scope', '$http', '$window', function($scope, $http, $window) {
    console.log("Hello World from DashboardController");

    $http({
                method: 'POST',
			    url: '/sessioncheck'
	        }).then(function(response) {
			        console.log(response.data);
			        //$window.alert("purva");
			        $scope.name = response.data;
				});


				$scope.info = {};

				$scope.showAdd = true;

				$scope.showlist = function(){
                    $http({
                        method: 'POST',
                        url: '/getMachineList',

                    }).then(function(response) {
                        $scope.machines = response.data;
                        console.log('mm',$scope.machines);
                    }, function(error) {
                        console.log(error);
                    });
                }
				$scope.shownetwork = function(){
                    $http({
                        method: 'POST',
                        url: '/getNetworkList',

                    }).then(function(response) {
                        $scope.networks = response.data;
                        console.log('mm',$scope.networks);
                    }, function(error) {
                        console.log(error);
                    });
                }
				$scope.showImage = function(){
                    $http({
                        method: 'POST',
                        url: '/getImageList',

                    }).then(function(response) {
                        $scope.images = response.data;
                        console.log('mm',$scope.images);
                    }, function(error) {
                        console.log(error);
                    });
                }
				$scope.showFlavor = function(){
                    $http({
                        method: 'POST',
                        url: '/getFlavorList',

                    }).then(function(response) {
                        $scope.flavors = response.data;
                        console.log('mm',$scope.flavors);
                    }, function(error) {
                        console.log(error);
                    });
                }
				
							$scope.showUsage = function(){
                    $http({
                        method: 'POST',
                        url: '/getServerUsage',

                    }).then(function(response) {
                        $scope.billing = response.data;
                        console.log('mm',$scope.billing);
                    }, function(error) {
                        console.log(error);
                    });
                }

                $scope.addMachine = function(){
                    $http({
                        method: 'POST',
                        url: '/addMachine',
                        data: {info:$scope.info}
                    }).then(function(response) {                       
                        $('#addPopUp').modal('hide')
						$scope.showlist();
                        $scope.info = {}
                    }, function(error) {
                        console.log(error);
                    });
                }

                $scope.editMachine = function(id){
                    $scope.info.id = id;

                    $scope.showAdd = false;

                    $http({
                        method: 'POST',
                        url: '/getMachine',
                        data: {id:$scope.info.id}
                    }).then(function(response) {
                        console.log(response);
                        $scope.info = response.data;
                        $('#addPopUp').modal('show')
                    }, function(error) {
                        console.log(error);
                    });
                }

                $scope.updateMachine = function(id){

                    $http({
                        method: 'POST',
                        url: '/updateMachine',
                        data: {info:$scope.info}
                    }).then(function(response) {
                        console.log(response.data);
                        $scope.showlist();
                        $('#addPopUp').modal('hide')
                    }, function(error) {
                        console.log(error);
                    });
                }


                $scope.showAddPopUp = function(){
                    $scope.showAdd = true;
                    $scope.info = {};
                    $('#addPopUp').modal('show')
                }

                $scope.showRunPopUp = function(id){

                    $scope.info.id = id;
                    $scope.run = {};
                    $http({
                        method: 'POST',
                        url: '/getMachine',
                        data: {id:$scope.info.id}
                    }).then(function(response) {
                        console.log(response);
                        $scope.run = response.data;
                        $scope.run.isRoot = false;
                        $('#runPopUp').modal('show');
                    }, function(error) {
                        console.log(error);
                    });
                }



                $scope.deleteMachine = function(){

                    $http({
                        method: 'POST',
                        url: '/deleteMachine',
                        data: {id:$scope.deleteMachineId}
                    }).then(function(response) {
                        console.log(response.data);
                        $scope.deleteMachineId = '';
						$('#deleteConfirm').modal('hide')
                        $scope.showlist();                        
                    }, function(error) {
                        console.log(error);
                    });
                }


				$scope.executeCommand = function(){


					console.log($scope.run);

					$http({
						method: 'POST',
						url: '/execute',
						data: {info:$scope.run}
					}).then(function(response) {
						console.log(response);
						$scope.run.response = response.data.message;
					}, function(error) {
						console.log(error);
					});
				}

				$scope.startServer = function(id){
                    $scope.serverId = id;
					console.log(id)
                    $http({
                        method: 'POST',
                        url: '/startMachine',
                        data: {id:$scope.serverId}
                    }).then(function(response) {
                        console.log(response.data);
                        $scope.serverId = '';
                        $scope.showlist();
                    }, function(error) {
                        console.log(error);
                    });
                }


                $scope.stopServer = function(id){
                    $scope.serverId = id;
					console.log(id)
                    $http({
                        method: 'POST',
                        url: '/stopMachine',
                        data: {id:$scope.serverId}
                    }).then(function(response) {
                        console.log(response.data);
                        $scope.serverId = '';
                        $scope.showlist();
                    }, function(error) {
                        console.log(error);
                    });
                }


                $scope.pauseServer = function(id){
                    $scope.serverId = id;
					console.log(id)
                    $http({
                        method: 'POST',
                        url: '/pauseMachine',
                        data: {id:$scope.serverId}
                    }).then(function(response) {
                        console.log(response.data);
                        $scope.serverId = '';
                        $scope.showlist();
                    }, function(error) {
                        console.log(error);
                    });
                }


                /*$scope.curlss = function(id){
                    $scope.serverId = id;
                    $http({
                        method: 'POST',
                        url: '/curls',
                        data: {id:$scope.serverId}
                    }).then(function(response) {
                        console.log(response.data);
                        $scope.serverId = '';
                        $scope.showlist();
                    }, function(error) {
                        console.log(error);
                    });
                }*/

                $scope.refreshServer = function(id){
                    $scope.serverId = id;
                    $http({
                        method: 'POST',
                        url: '/unpauseMachine',
                        data: {id:$scope.serverId}
                    }).then(function(response) {
                        console.log(response.data);
                        $scope.serverId = '';
                        $scope.showlist();
                    }, function(error) {
                        console.log(error);
                    });
                }

                $scope.confirmDelete = function(id){
                    $scope.deleteServerId = id;
                    $('#deleteConfirm').modal('show');
                }

                
                
                $scope.deleteServer = function(){
                    $http({
                        method: 'POST',
                        url: '/deleteMachine',
                        data: {id:$scope.deleteServerId}
                    }).then(function(response) {
                        console.log(response.data);
                        $scope.deleteServerId = '';
						$('#deleteConfirm').modal('hide')
                        $scope.showlist();
                    }, function(error) {
                        console.log(error);
                    });
                }

                $scope.showlist();
            }

]);

//machine
app.controller('MachineController', ['$scope', '$http', function($scope, $http) {
    console.log("Hello World from MachineController");

    $http({
                method: 'POST',
			    url: '/sessioncheck'
	        }).then(function(response) {
			        console.log(response.data);
			        $scope.name = response.data;
				});
}]);

//Instance
app.controller('InstanceController', ['$scope', '$http', function($scope, $http) {
    console.log("Hello World from InstanceController");

    $http({
                method: 'POST',
			    url: '/sessioncheck'
	        }).then(function(response) {
			        console.log(response.data);
			        $scope.name = response.data;
				});
}]);



//Flavors
app.controller('FlavorListController', ['$scope', '$http', function($scope, $http) {
    console.log("Hello World from FlavorListController");

    $http({
                method: 'POST',
			    url: '/sessioncheck'
	        }).then(function(response) {
			        console.log(response.data);
			        	        $scope.name = response.data;
				});


				$scope.info = {};


				
			
				$scope.showFlavor = function(){
                    $http({
                        method: 'POST',
                        url: '/getFlavorList',

                    }).then(function(response) {
                        $scope.flavors = response.data;
                        console.log('mm',$scope.flavors);
                    }, function(error) {
                        console.log(error);
                    });
                }
                $scope.showFlavor();

            }

]);


//Images
app.controller('ImageListController', ['$scope', '$http', function($scope, $http) {
    console.log("Hello World from ImageListController");

    $http({
                method: 'POST',
			    url: '/sessioncheck'
	        }).then(function(response) {
			        console.log(response.data);
			        	        $scope.name = response.data;
				});


				$scope.info = {};


				
							$scope.showImage = function(){
                    $http({
                        method: 'POST',
                        url: '/getImageList',

                    }).then(function(response) {
                        $scope.images = response.data;
                        console.log('mm',$scope.images);
                    }, function(error) {
                        console.log(error);
                    });
                }
				
                $scope.showImage();

            }

]);



//Network
app.controller('NetworkListController', ['$scope', '$http', function($scope, $http) {
    console.log("Hello World from NetworkListController");

    $http({
        method: 'POST',
        url: '/sessioncheck'
    }).then(function (response) {
        console.log(response.data);
        $scope.name = response.data;
    });


    $scope.info = {};


    $scope.showNetwork = function () {
        $http({
            method: 'POST',
            url: '/getNetworkList',

        }).then(function (response) {
            $scope.networks = response.data;
            console.log('mm', $scope.networks);
        }, function (error) {
            console.log(error);
        });
    }

    $scope.showNetwork();
}
					
]);


//Usage
app.controller('InstanceUsageController', ['$scope', '$http', function($scope, $http) {
    console.log("Hello World from InstanceUsageController");

    $http({
                method: 'POST',
			    url: '/sessioncheck'
	        }).then(function(response) {
			        console.log(response.data);
			        	        $scope.name = response.data;
				});


				$scope.info = {};


				
			$scope.showUsage = function(){
                    $http({
                        method: 'POST',
                        url: '/getServerUsage',

                    }).then(function(response) {
                        $scope.billing = response.data;
                        console.log('mm',$scope.billing);
                    }, function(error) {
                        console.log(error);
                    });
                }
				
                $scope.showUsage();

            }

]);





//profile
app.controller('ProfileController', ['$scope', '$http', function($scope, $http) {
    console.log("Hello World from ProfileController");
    var name =" ";

    $http({
                method: 'POST',
			    url: '/sessioncheck'
	        }).then(function(response) {
	                name = response.data;
			        console.log(response.data);

			        //test
			        $http({
                method: 'POST',
                url: '/getUserProfile',
                data: {profile:response.data}
            }).then(function(response) {
                console.log(response.data);
                $scope.domain = response.data[2];
                $scope.username = response.data[0];
                $scope.password = response.data[1];

                }, function(error) {
                console.log(error);
                });


				});


}]);