var loginapp = angular.module('loginapp', []);

loginapp.controller('LoginController', ['$scope', '$http', '$window', '$location', function ($scope, $http, $window, $location) {
    console.log("Hello from LoginController");

     $http({
                method: 'POST',
			    url: '/sessiondestroy'
	        }).then(function(response) {
			        console.log('session destroyed..!!');
				});

    $scope.addUser = function (domain, username, password){
        $http({
				method: 'POST',
				url: '/addUser',
				data: {domainame:domain, user:username, pass:password}
			   }).then(function(response) {
			        //console.log(response);
			        $window.alert('registration done successfully..!!');
				}, function(error) {
				console.log(error);
				});
    };

    $scope.checkUser = function (username, password) {

        $http({
                method: 'POST',
                url: '/getUserlist',
                data: {user:username, pass:password}
            }).then(function(response) {
                console.log(response.data);
                if(response.data == 'unsuccessful'){
                    //console.log("status");
                    $scope.flag = "Wrong username or Password. Try Again!!";
                    //$window.alert("Wrong username or Password. Try Again!!");
                }
                else{
                    //console.log("purva");
                    $window.location.href='dashboard';
                }
                }, function(error) {
                console.log(error);
                });
    };
}]);