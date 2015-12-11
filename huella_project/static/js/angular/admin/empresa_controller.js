/**
 * Created by linglung on 12/2/15.
 */
$( document ).ready(function(){

    var app= angular.module('Empleados', ['ngRoute','ui.bootstrap'])
        .config(function($routeProvider, $locationProvider) {
            $routeProvider
            .when('/empleados', {
                 templateUrl: 'empleados.html',
                 controllerAs: 'empleados',
                 controller: 'EmpleadosCtrl'
            })
            .when('/procesos', {
                 templateUrl: 'procesos.html',
                 controllerAs: 'step',
                 controller: 'EmpleadosCtrl'
            })
            .when('/perfiles', {
                 templateUrl: 'perfiles.html',
                 controller: 'EmpleadosCtrl'
            })
            .when('/tareas', {
                 templateUrl: 'tareas.html',
                 controller: 'EmpleadosCtrl'
            })
                .otherwise({
                redirectTo: '/empleados'
              })
        // $locationProvider.html5Mode(true).hashPrefix('!');
        })
        .controller('EmpleadosCtrl', ['$scope', '$http','$uibModal', 'fileUpload', function($scope, $http, $uibModal, fileUpload) {
            $scope.empleados = []
            $scope.datos = {
                nombre : "",
                apellido : "",
                direccion : "",
                identificacion : "",
                email : "",
                telefono1 : "",
                telefono2 : "",
                perfil : null,
                is_admin : 0
            }

            $scope.url='/api-empresas/empleado/';
            $scope.next=null;
            $scope.previous=null;
            $scope.current_page=null;
            $scope.page_number=null;
            $scope.animationsEnabled = true;
            $scope.count= 0;
            $scope.getEmpleados = function () {

                $http.get($scope.url+window.empresa+'/get_empleados/').success(function (response) {
                    var pages_number=0
                    $scope.previous=response.previous;
                    $scope.next=response.next;
                    $scope.count= parseInt(response.count)
                    $scope.empleados = response.results;
                    if($scope.previous==null) {
                        if ($scope.count != 0) {
                            $scope.pages_number = Math.ceil($scope.count / $scope.empleados.length);
                            $scope.paginate($scope.pages_number, $scope.previous, $scope.next, $scope.url);
                        } else {
                            $scope.getEmpleados($scope.url);
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
            var csrftoken = $("[name='csrfmiddlewaretoken']").val();
            $scope.creaEmpleado = function () {


                var template = 'modal-creaEmpleado.html';
                var modalInstance = $uibModal.open({
                    animation: $scope.animationsEnabled,
                    templateUrl: template,
                    controller: 'GenericModalInstanceCtrl',
                    size: 'lg',
                    scope: $scope
                });
                modalInstance.result.then(function (foto) {

                    $scope.foto=foto
                    var file = $scope.foto;
                    if($scope.datos.is_admin==true){
                        $scope.datos.is_admin==1
                    }else{
                        $scope.datos.is_admin==0
                    }
                    var req = {
                        url: $scope.url,
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': csrftoken
                        },
                        data: $scope.datos
                    }
                    $http(req).then(function (response) {
                        $scope.getEmpleados()
                        var file = $scope.foto;
//                        console.log('file is ' );
//                        console.dir(file);
                        var uploadUrl = $scope.url+response.data.pk+"/upload_foto/";
                        fileUpload.uploadFileToUrl(file, uploadUrl, csrftoken);

                    }, function(response){
                        console.log(response)

                    });
                }, function () {
                    // console.log('dismiss modal')
                });
            }

            $scope.subirImagen= function (id_empresa) {
                var file = $scope.foto;
                console.log('file is ' );
                console.dir(file);
                var uploadUrl = $scope.url+id_empresa+"/upload_foto/";
                fileUpload.uploadFileToUrl(file, uploadUrl, csrftoken);
            }

            $scope.getEmpleados()

        }])
        .controller('ProcesosCtrl', ['$scope', '$http','$uibModal', function($scope, $http, $uibModal) {
            $scope.procesos = []
            $scope.datos = {
                nombre : "",
                categoria:"",
                codigo:"",
                descripcion:"",
                formatos_asignados:[]
            }
            $scope.url='/api-empresas/proceso/';
            $scope.next=null;
            $scope.previous=null;
            $scope.current_page=null;
            $scope.page_number=null;
            $scope.animationsEnabled = true;
            $scope.count= 0;
            $scope.getProcesos = function () {

                $http.get($scope.url+window.empresa+'/get_procesos/').success(function (response) {
                    var pages_number=0
                    $scope.previous=response.previous;
                    $scope.next=response.next;
                    $scope.count= parseInt(response.count)
                    $scope.procesos = response.results;
                    if($scope.previous==null) {
                        if ($scope.count != 0) {
                            $scope.pages_number = Math.ceil($scope.count / $scope.procesos.length);
                            $scope.paginate($scope.pages_number, $scope.previous, $scope.next, $scope.url);
                        } else {
                            $scope.getProcesos($scope.url);
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
            var csrftoken = $("[name='csrfmiddlewaretoken']").val();
            $scope.creaProceso = function () {
                var template = 'modal-creaProceso.html';
                var modalInstance = $uibModal.open({
                    animation: $scope.animationsEnabled,
                    templateUrl: template,
                    controller: 'GenericModalInstanceCtrl',
                    size: 'lg',
                    scope: $scope
                });
                modalInstance.result.then(function () {
                    console.log($scope.datos)
                    $scope.datos.formatos_asignados=[]
                    $scope.datos.formatos_asignados=$('input[name=formatos_asignados]:checked').map(function(_, el) {
                        return $(el).val();
                    }).get();
                    console.log($scope.datos)
                    var req = {
                        url: $scope.url,
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': csrftoken
                        },
                        data: $scope.datos
                    }
                    $http(req).then(function (response) {
                        console.log(response)
                        $scope.getProcesos()

                    }, function(response){
                        console.log(response)

                    });
                }, function () {
                    // console.log('dismiss modal')
                });
            }
            $scope.getProcesos()

        }])
        .controller('PerfilesCtrl', ['$scope', '$http','$uibModal', function($scope, $http, $uibModal) {
            $scope.procesos = []
            $scope.datos = {
                nombre : "",
                categoria:"",
                codigo:"",
                descripcion:"",
                formatos_asignados:[]
            }
            $scope.url='/api-empresas/proceso/';
            $scope.next=null;
            $scope.previous=null;
            $scope.current_page=null;
            $scope.page_number=null;
            $scope.animationsEnabled = true;
            $scope.count= 0;
            $scope.getProcesos = function () {

                $http.get($scope.url+window.empresa+'/get_procesos/').success(function (response) {
                    var pages_number=0
                    $scope.previous=response.previous;
                    $scope.next=response.next;
                    $scope.count= parseInt(response.count)
                    $scope.procesos = response.results;
                    if($scope.previous==null) {
                        if ($scope.count != 0) {
                            $scope.pages_number = Math.ceil($scope.count / $scope.procesos.length);
                            $scope.paginate($scope.pages_number, $scope.previous, $scope.next, $scope.url);
                        } else {
                            $scope.getProcesos($scope.url);
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
            var csrftoken = $("[name='csrfmiddlewaretoken']").val();
            $scope.creaProceso = function () {
                var template = 'modal-creaProceso.html';
                var modalInstance = $uibModal.open({
                    animation: $scope.animationsEnabled,
                    templateUrl: template,
                    controller: 'GenericModalInstanceCtrl',
                    size: 'lg',
                    scope: $scope
                });
                modalInstance.result.then(function () {
                    console.log($scope.datos)
                    $scope.datos.formatos_asignados=[]
                    $scope.datos.formatos_asignados=$('input[name=formatos_asignados]:checked').map(function(_, el) {
                        return $(el).val();
                    }).get();
                    console.log($scope.datos)
                    var req = {
                        url: $scope.url,
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': csrftoken
                        },
                        data: $scope.datos
                    }
                    $http(req).then(function (response) {
                        console.log(response)
                        $scope.getProcesos()

                    }, function(response){
                        console.log(response)

                    });
                }, function () {
                    // console.log('dismiss modal')
                });
            }
            $scope.getProcesos()

        }])
        .controller('TareasCtrl', ['$scope', '$http','$uibModal', function($scope, $http, $uibModal) {
            $scope.procesos = []
            $scope.datos = {
                nombre : "",
                categoria:"",
                codigo:"",
                descripcion:"",
                formatos_asignados:[]
            }
            $scope.url='/api-empresas/proceso/';
            $scope.next=null;
            $scope.previous=null;
            $scope.current_page=null;
            $scope.page_number=null;
            $scope.animationsEnabled = true;
            $scope.count= 0;
            $scope.getProcesos = function () {

                $http.get($scope.url+window.empresa+'/get_procesos/').success(function (response) {
                    var pages_number=0
                    $scope.previous=response.previous;
                    $scope.next=response.next;
                    $scope.count= parseInt(response.count)
                    $scope.procesos = response.results;
                    if($scope.previous==null) {
                        if ($scope.count != 0) {
                            $scope.pages_number = Math.ceil($scope.count / $scope.procesos.length);
                            $scope.paginate($scope.pages_number, $scope.previous, $scope.next, $scope.url);
                        } else {
                            $scope.getProcesos($scope.url);
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
            var csrftoken = $("[name='csrfmiddlewaretoken']").val();
            $scope.creaProceso = function () {
                var template = 'modal-creaProceso.html';
                var modalInstance = $uibModal.open({
                    animation: $scope.animationsEnabled,
                    templateUrl: template,
                    controller: 'GenericModalInstanceCtrl',
                    size: 'lg',
                    scope: $scope
                });
                modalInstance.result.then(function () {
                    console.log($scope.datos)
                    $scope.datos.formatos_asignados=[]
                    $scope.datos.formatos_asignados=$('input[name=formatos_asignados]:checked').map(function(_, el) {
                        return $(el).val();
                    }).get();
                    console.log($scope.datos)
                    var req = {
                        url: $scope.url,
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': csrftoken
                        },
                        data: $scope.datos
                    }
                    $http(req).then(function (response) {
                        console.log(response)
                        $scope.getProcesos()

                    }, function(response){
                        console.log(response)

                    });
                }, function () {
                    // console.log('dismiss modal')
                });
            }
            $scope.getProcesos()

        }])
        .controller('GenericModalInstanceCtrl', function ($scope, $uibModalInstance) {
            $scope.ok = function () {
                $uibModalInstance.close($scope.foto);
            };

            $scope.cancel = function () {

                $uibModalInstance.dismiss('cancel');
            };
        });
    app.directive('fileInput', ['$parse', function ($parse) {
        return {
            restrict: 'A',
            link: function(scope, element, attrs) {
                var model = $parse(attrs.fileInput);
                var modelSetter = model.assign;
                console.log(element)
                element.bind('change', function(){
                    scope.$apply(function(){
                        modelSetter(scope, element[0].files[0]);
                    });
                });
            }
        };
    }])
    .service('fileUpload', ['$http', function ($http) {
        this.uploadFileToUrl = function(file, uploadUrl, csrftoken){
            var fd = new FormData();
            fd.append('file', file);
            $http.post(uploadUrl, fd, {
                transformRequest: angular.identity,
                headers: {
                    'Content-Type': undefined,
                    'X-CSRFToken': csrftoken
                }
            })
            .success(function(){
            })
            .error(function(){
            });
        }
    }]);


    angular.bootstrap(document, ['Empleados'])
});