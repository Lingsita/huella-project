/**
 * Created by linglung on 12/14/15.
 */
$( document ).ready(function(){

    var app= angular.module('Documentos', ['ngRoute','ui.bootstrap'])
        .config(function($routeProvider, $locationProvider) {
            $routeProvider
                .when('/proceso', {
                    templateUrl: 'documento.html',
                    // controllerAs: 'documento',
                    controller: 'DocsCtrl'
                })
                .otherwise({
                    redirectTo: '/'
                })
            // $locationProvider.html5Mode(true).hashPrefix('!');
        })
        .controller('DocsCtrl', ['$scope', '$rootScope', '$http','$uibModal',  function($scope, $rootScope, $http, $uibModal) {
            $scope.documentos = []
            $scope.url='/api-empresas/documento/';
            $scope.url_procesos='/api-empresas/proceso/empleado';
            $scope.csrftoken = $("[name='csrfmiddlewaretoken']").val();
            $scope.id_proceso= $rootScope.proceso

            // Pagination Schema
            $scope.currentPage=1
            $scope.numPerPage=10
            $scope.totalItems=1
            $scope.filteredDocumentos = []
            //paginate with bootstrap
//            $scope.$watch('documentos.length', function(){
//                $scope.totalItems = $scope.documentos.length;
//                var begin = (($scope.currentPage - 1) * $scope.numPerPage)
//                var end = begin + $scope.numPerPage;
//
//                $scope.filteredDocumentos = $scope.documentos.slice(begin, end);
//
//            })
            //paginate with django rest

            $scope.$watch('currentPage', function() {

                if($scope.id_proceso=="" || $scope.id_proceso==null){

                }else {
                    if ($scope.currentPage<=1){
                        $http.get($scope.url + $scope.id_proceso + '/by_proceso/').success(function (response) {
                            $scope.filteredDocumentos = response.results;
                            console.log()
                        });
                    }else{
                        $http.get($scope.url + $scope.id_proceso + '/by_proceso/?page=' + $scope.currentPage).success(function (response) {
                            $scope.filteredDocumentos = response.results;
                        });
                    }

                }

            });

            $scope.pageChanged= function () {

                var begin = (($scope.currentPage - 1) * $scope.numPerPage)
                , end = begin + $scope.numPerPage;

                $scope.filteredTodos = $scope.documentos.slice(begin, end);
            }
            //-- End of Pagination

            $scope.getDocumentos= function () {

                if($scope.id_proceso=="" || $scope.id_proceso==null){
                    location.href="/"
                }else {
                    $http.get($scope.url+$scope.id_proceso+'/by_proceso/').success(function (response) {
                        $scope.documentos = response.results;
                        console.log($scope.documentos)
                        $scope.totalItems =response.count
                    });

                }

            }
            $scope.verDocumento= function (pk) {
                console.log(pk)
            }
            $scope.getDocumentos()
        }])
        .controller('DocumentoCtrl', ['$scope', '$rootScope', '$http','$uibModal', function($scope, $rootScope, $http, $uibModal) {
            $scope.documentos = []
            $scope.url_procesos='/api-empresas/proceso/';
            $scope.url='/api-empresas/documento/';

            $scope.animationsEnabled = true;

            $scope.csrftoken = $("[name='csrfmiddlewaretoken']").val();
            $scope.getDocumentos= function (id_proceso) {
                console.log(id_proceso)

                $rootScope.proceso = id_proceso;
                location.href = "#proceso"

            }

            $scope.getProcesos = function () {

                $http.get($scope.url_procesos+'empleado/').success(function (response) {
                    $scope.procesos = response.results;
                    console.log($scope.procesos)
                });
            }
            $scope.getProcesos();



        }])


        .controller('GenericModalInstanceCtrl', function ($scope, $uibModalInstance) {
            $scope.ok = function () {
                $uibModalInstance.close($scope.foto);
            };

            $scope.cancel = function () {

                $uibModalInstance.dismiss('cancel');
            };
        })

        .filter('dateString', ['$filter', function($filter) {
            return function(input) {
                var date = $filter('date')(input, "yyyy-MM-dd 'hora:' hh:mma");
                return date.toString()
            };
        }]);


    angular.bootstrap(document, ['Documentos'])
});