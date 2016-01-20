/**
 * Created by linglung on 10/2/15.
 */
jQuery( document ).ready(function() {

    var app = angular.module('empresasApp', ['ngRoute','ui.bootstrap']);

    app.controller('EmpresaCtrl',['$scope', '$http','$uibModal', '$log' ,'postService',  function($scope, $http, $uibModal,  $log, postService) {
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
         $scope.animationsEnabled = true;
         $scope.state_message=""
         $scope.datos= {
             nombre : "",
             NIT : "",
             direccion : "",
             telefono1 : "",
             telefono2 : "",
             email : ""
         }
         var csrftoken = $("[name='csrfmiddlewaretoken']").val();
         $scope.e_empresa={
             nombre:null,
             nit:null,
             id:null
         }
        $scope.verEmpresa= function (id) {
            location.href="/detail/"+id
        }
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
            });
        }
        $scope.paginate = function(count,previous, next, url){
            $scope.pages = {}
            for (i=1; i<=count; i++){
                $scope.pages[i]=url+"?page="+String(i)
            }
        }

        $scope.searchEmpresa=function (){
            $scope.getEmpresas($scope.url+"?"+$scope.lookup_filter+"="+$scope.lookup_field);
        }
        $scope.submit= function () {
            console.log('entro a submit')
            var req = {
                url: $scope.url,
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: $scope.datos
            }
            $http(req).then(function (response) {
                console.log(response);
                if(response.statusText=="CREATED"){
                    $scope.state_message=""
                    $scope.getEmpresas($scope.url);
                    $('#creaEmpresa').modal('hide');
                    $scope.state_message="Empresa creada satisfactoriamente"
                    $('#bad_status_message').find('#message').html($scope.state_message);
                    $('#status_message').css('display', 'block')
                }
                console.log($scope.state_message)
            }, function(response){
                $scope.state_message="Ocurrió un error al ingresar sus datos, por favor verifique la información suministrada"
                $('#creaEmpresa').modal('hide');
                if(response.data.NIT){
                    $scope.state_message="Ya existe una empresa con esta identificación, por favor verifique la información suministrada.";

                    console.log($scope.state_message);
                    $('#bad_status_message').find('#message').html($scope.state_message);
                    $('#bad_status_message').css('display', 'block')
                }
            });
        }



        $scope.openModal = function () {
            var csrftoken = $("[name='csrfmiddlewaretoken']").val();
            var template = 'modal-creaEmpresa.html';
            var modalInstance = $uibModal.open({
                animation: $scope.animationsEnabled,
                templateUrl: template,
                controller: 'GenericModalInstanceCtrl',
                size: 'md',
                scope: $scope
            });
            modalInstance.result.then(function () {
                var req = {
                    url: $scope.url,
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                    data: $scope.datos
                }
                $http(req).then(function (response) {
                    if(response.statusText=="CREATED"){
                        $scope.state_message=""
                        $scope.state_message="Empresa creada satisfactoriamente"
                        $scope.getEmpresas($scope.url);
                        $('#status_message').find('#message').html($scope.state_message);
                        $('#status_message').css('display', 'block')
                        setTimeout(function(){
                            $('#status_message').css('display', 'none')
                        }, 3000);
                    }
                }, function(response){
                    $scope.state_message="Ocurrió un error al ingresar sus datos, por favor verifique la información suministrada"
                    if(response.data.NIT){
                        $scope.state_message="Ya existe una empresa con esta identificación, por favor verifique la información suministrada.";
                        $('#bad_status_message').find('#message').html($scope.state_message);
                        $('#bad_status_message').css('display', 'block')
                        setTimeout(function(){
                            $('#bad_status_message').css('display', 'none')
                        }, 3000);
                    }
                });
            }, function () {
                // console.log('dismiss modal')
            });
        }

        $scope.confirmaEliminaEmpresa= function (nombre, nit, id) {
            $scope.e_empresa={
                nombre:nombre,
                nit:nit,
                id:id
            }
            var modalInstance = $uibModal.open({
                animation: $scope.animationsEnabled,
                templateUrl: 'modal-eliminaEmpresa.html',
                controller: 'ModalInstanceCtrl',
                size: 'md',
                resolve: {
                    e_empresa: function () {
                        return $scope.e_empresa;
                    }
                }
            });
            modalInstance.result.then(function (e_empresa) {
                $scope.e_empresa = e_empresa;
                $scope.eliminaEmpresa()
            }, function () {

            });
        }

        $scope.eliminaEmpresa= function(){
            var id= $scope.e_empresa.id;
            var req = {
                url: $scope.url+id,
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: {}
            }
            $http(req).then(function (response) {
                $scope.state_message="Empresa eliminada satisfactoriamente"
                $scope.getEmpresas($scope.url);
            }, function(response){

            });
        }
        $scope.getEmpresas($scope.url);

    }])
        .controller('ModalInstanceCtrl', function ($scope, $uibModalInstance, e_empresa) {
            $scope.e_empresa=e_empresa;
            $scope.ok = function () {
                $uibModalInstance.close($scope.e_empresa);
            };
            $scope.cancel = function () {
                $uibModalInstance.dismiss('cancel');
            };
        })
        .controller('GenericModalInstanceCtrl', function ($scope, $uibModalInstance) {

            $scope.ok = function () {
                $uibModalInstance.close($scope.datos);
            };

            $scope.cancel = function () {
                $uibModalInstance.dismiss('cancel');
            };
        });

    app.config(function($routeProvider,  $locationProvider) {

    });

    app.factory('postService', [ '$http', function($http ) {
        return function($url, $data){
            $http.post($url, $data).then(function (response) {
                console.log(response)
            }, function(response){
                console.log(response)
            });
        }
    }]);

    angular.bootstrap(document, ['empresasApp'])
});