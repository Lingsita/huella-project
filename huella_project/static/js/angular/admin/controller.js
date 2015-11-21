/**
 * Created by linglung on 10/2/15.
 */
 $( document ).ready(function() {

     var app = angular.module('empresasApp', ['ngRoute']);

     app.controller('EmpresaCtrl', function($scope, $http) {
             $scope.empresas = [];
             $scope.next=null;
             $scope.previous=null;
             $scope.current_page=null;
             $scope.page_number=null;
             $scope.count= 0;
             $scope.url='/api-empresas/empresa/'
             $scope.pages={}
             $scope.lookup_field=null
             $scope.lookup_filter="nombre"
             $scope.getEmpresas = function (url) {
                 $http.get(url).success(function (response) {
                     var pages_number=0
                     $scope.previous=response.previous;
                     $scope.next=response.next;
                     $scope.count= parseInt(response.count)
                     $scope.empresas = response.results;
                     if($scope.previous==null) {
                         if ($scope.count != 0) {
                             $scope.pages_number = Math.ceil($scope.count / $scope.empresas.length);
                             $scope.paginate($scope.pages_number, $scope.previous, $scope.next, $scope.url);
                         } else {
                             $scope.getEmpresas($scope.url);
                         }
                     }

//                     $scope.paginate($scope.pages_number, $scope.previous, $scope.next, $scope.url);
                 });
             }
             $scope.paginate = function(count,previous, next, url){
                 $scope.pages = {}
                 for (i=1; i<=count; i++){
                    $scope.pages[i]=url+"?page="+String(i)
                 }
//                 console.log(("asdasd909dasdas90").match(/\d+$/)[0]);
             }

             $scope.searchEmpresa=function (){
                $scope.getEmpresas($scope.url+"?"+$scope.lookup_filter+"="+$scope.lookup_field);
             }

             $scope.createEmpresa = function(){
                 $('#crea_empresa')
                 $http.post($scope.url, data).success(function (response) {
                     var pages_number=0
                     $scope.previous=response.previous;
                     $scope.next=response.next;
//                     $scope.current_page=(response.next).match(/\d+$/)[0]
                     $scope.count= parseInt(response.count)
                     $scope.empresas = response.results;
                     if($scope.previous==null)
                        $scope.pages_number= Math.ceil($scope.count / $scope.empresas.length);
                     console.log($scope.pages_number+"-"+ $scope.count +"-"+ $scope.empresas.length )
                     $scope.paginate($scope.pages_number, $scope.previous, $scope.next, $scope.url);
                 });

             }

             $scope.getEmpresas($scope.url);
         });
        app.controller('CrearEmpresaCtrl', ['$scope', 'postService', function($scope, postService) {
            $scope.datos= {
                nombre : "",
                NIT : "",
                direccion : "",
                telefono1 : "",
                telefono2 : "",
                email : ""
            }
            $scope.url="/api-empresas/empresa/"
            $scope.submit= function () {
                  postService($scope.url, $scope.datos)
                  console.log($scope)
            }
         }]);
        app.config(function($routeProvider, $locationProvider) {
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

     app.factory('postService', [ '$http', function($http ) {
            return function($url, $data){
                console.log($url + $data)
                $http.post($url, $data).then(function (response) {
                     console.log(response)
                }, function(response){
                    console.log(response)
                });
            }
        }]);

     angular.bootstrap(document, ['empresasApp'])
 });