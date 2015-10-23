/**
 * Created by linglung on 10/2/15.
 */

 $( document ).ready(function() {

     app = angular.module('empresasApp', ['ngRoute'])
         .controller('EmpresaCtrl', function($scope, $http) {
             $scope.empresas = [];
             $scope.getEmpresas = function () {
                 $http.get('/empresas/list').success(function (response) {
                     $scope.empresas = response;
                 })
             }
             $scope.createEmpresa = function(){

             }
             $scope.getEmpresas();
         })
        .config(function($routeProvider, $locationProvider) {
             $routeProvider
//                 .when('/', {
//                     templateUrl: 'employee',
//                     controller: 'PruebaCtrl'
//                 })
//                .when('/perfil', {
//                     templateUrl: 'prueba/perfil',
//                     controller: 'PruebaCtrl'
//                 })

         });

     app.factory('postService', ['$scope', '$http', function($scope,  $http) {
            return function($url, $data){
                $http.post($url).success(function (response) {
                     $scope.empresas = response;
                })
            }
        }]);

     angular.bootstrap(document, ['empresasApp'])
 });