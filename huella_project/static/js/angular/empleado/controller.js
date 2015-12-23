/**
 * Created by linglung on 12/14/15.
 */
$( document ).ready(function(){

    var app= angular.module('Documentos', ['ngRoute','ui.bootstrap'])
        .config(function($routeProvider, $locationProvider) {
            $routeProvider
//            .when('/', {
//                 templateUrl: 'procesos.html',
//                 controllerAs: 'step',
//                 controller: 'EmpleadosCtrl'
//            })
            .when('/proceso', {
                 templateUrl: 'documento.html',
                 controllerAs: 'documento',
                 controller: 'DocumentoCtrl'
            })
            .otherwise({
                redirectTo: '/'
              })
        // $locationProvider.html5Mode(true).hashPrefix('!');
        })
        .controller('DocumentoCtrl', ['$scope', '$http','$uibModal', 'fileUpload', function($scope, $http, $uibModal, fileUpload) {
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
            $scope.getDocumentos = function () {
                console.log('va a buscar documentos')
//                $http.get($scope.url+window.empresa+'/get_empleados/').success(function (response) {
//                    var pages_number=0
//                    $scope.previous=response.previous;
//                    $scope.next=response.next;
//                    $scope.count= parseInt(response.count)
//                    $scope.empleados = response.results;
//                    if($scope.previous==null) {
//                        if ($scope.count != 0) {
//                            $scope.pages_number = Math.ceil($scope.count / $scope.empleados.length);
//                            $scope.paginate($scope.pages_number, $scope.previous, $scope.next, $scope.url);
//                        } else {
////                            $scope.getEmpleados($scope.url);
//                        }
//                    }
//                });
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
                        console.log(response)
                        var uploadUrl = $scope.url+response.data.pk+"/upload_foto/?id="+response.data.pk;
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



        }])

        .controller('PerfilesCtrl', ['$scope', '$http','$uibModal', function($scope, $http, $uibModal) {
            $scope.perfiles = []
            $scope.current_perfil = {
                nombre : "",
                codigo:"",
                descripcion:"",
                empresa: "",
                procesos:[],
                formatos_asignados:[]
            }
            $scope.datos = {
                nombre : "",
                codigo:"",
                descripcion:"",
                empresa: "",
                procesos:[],
                formatos_asignados:[]
            }
            $scope.e_perfil={
                nombre:"",
                id:""
            }
            $scope.hay_perfiles=false
            $scope.url='/api-empresas/perfil/';
            $scope.next=null;
            $scope.previous=null;
            $scope.current_page=null;
            $scope.page_number=null;
            $scope.animationsEnabled = true;
            $scope.count= 0;

            $scope.getPerfiles = function () {
                $http.get($scope.url+window.empresa+'/get_perfiles/').success(function (response) {
                    var pages_number=0
                    $scope.previous=response.previous;
                    $scope.next=response.next;
                    $scope.count= parseInt(response.count)
                    $scope.perfiles = response.results;

                    if($scope.previous==null) {
                        if ($scope.count != 0) {
                            $scope.hay_perfiles=true
                            $scope.pages_number = Math.ceil($scope.count / $scope.perfiles.length);
                            $scope.paginate($scope.pages_number, $scope.previous, $scope.next, $scope.url);
                        } else {
                            $scope.hay_perfiles=false
                        /*TODO: empy state*/
//                            $scope.getPerfiles($scope.url);
                        }
                    }
                });
            }
            $scope.getPerfil = function (id) {
                $http.get($scope.url+id).success(function (response) {
                    $scope.current_perfil=response
                    console.log(response)
                    var procesos=$scope.current_perfil.procesos
                    var formatos_asignados=$scope.current_perfil.formatos_asignados
                    var selected_procesos=[]
                    var selected_formatos=[]
                    $.each(procesos, function(i,e){
                        selected_procesos.push(''+ e.id +'')
                    });
                    $.each(formatos_asignados, function(i,e){
                        selected_formatos.push(''+ e.id +'')
                    });
                    $scope.current_perfil.procesos=selected_procesos
                    $scope.current_perfil.formatos_asignados=selected_formatos
                    var template = 'modal-modificaPerfil.html';
                    var modalInstance = $uibModal.open({
                        animation: $scope.animationsEnabled,
                        templateUrl: template,
                        controller: 'GenericModalInstanceCtrl',
                        size: 'lg',
                        scope: $scope,
                        resolve:
                            function () {
                                var procesos=$scope.current_perfil.procesos
                                $.each(procesos, function(i,e){
                                    $("#id_current_perfil_procesos option[value='" + e.id + "']").prop("selected", true);

                                    console.log(e.id+"dsd")
                                });
                            }

                    });
                    modalInstance.result.then(function () {
                        $scope.current_perfil.empresa=$('#id_current_perfil_empresa').val()
                        var req = {
                            url: $scope.url+$scope.current_perfil.pk+"/",
                            method: 'PUT',
                            headers: {
                                'X-CSRFToken': csrftoken
                            },
                            data: $scope.current_perfil
                        }
                        $http(req).then(function (response) {
                            console.log(response)

                                $('#status_message').find('#message').html('El perfil fue actualizado correctamente');
                                $('#status_message').css('display', 'block')
                                setTimeout(function(){
                                    $('#status_message').css('display', 'none')
                                }, 3000);


                            $scope.getPerfiles()

                        }, function(response){
                            console.log(response)
                            $('#bad_status_message').find('#message').html('Algo sali\u00f3 mal, por favor revisa la informaci\u00f3n y vuelve a intentarlo');
                            $('#bad_status_message').css('display', 'block')
                            setTimeout(function(){
                                $('#bad_status_message').css('display', 'none')
                            }, 4000);

                        });
                    }, function () {
                        // console.log('dismiss modal')
                    });
                });
            }
            $scope.paginate = function(count,previous, next, url){
                $scope.pages = {}
                for (i=1; i<=count; i++){
                    $scope.pages[i]=url+"?page="+String(i)
                }
            }
            var csrftoken = $("[name='csrfmiddlewaretoken']").val();

            $scope.creaPerfil = function () {
                var template = 'modal-creaPerfil.html';
                var modalInstance = $uibModal.open({
                    animation: $scope.animationsEnabled,
                    templateUrl: template,
                    controller: 'GenericModalInstanceCtrl',
                    size: 'lg',
                    scope: $scope
                });
                modalInstance.result.then(function () {

                    $scope.datos.formatos_asignados=[]
                    $scope.datos.procesos=[]
                    $scope.datos.empresa=$('#id_empresa').val()
                    $scope.datos.formatos_asignados=$('#id_formatos_asignados_perfil :selected').map(function(i, el) {
                        return $(el).val();
                    }).get();
                    $scope.datos.procesos=$('#id_procesos :selected').map(function(i, el) {
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
                        if(response.data.perfil_exists){
                            $('#bad_status_message').find('#message').html('Ya existe un perfil con este codigo');
                            $('#bad_status_message').css('display', 'block')
                            setTimeout(function(){
                                $('#bad_status_message').css('display', 'none')
                            }, 3000);
                        }
                        else{
                            $('#status_message').find('#message').html('El perfil fue creado correctamente');
                            $('#status_message').css('display', 'block')
                            setTimeout(function(){
                                $('#status_message').css('display', 'none')
                            }, 3000);
                        }

                        $scope.getPerfiles()

                    }, function(response){
                        console.log(response)
                        $('#bad_status_message').find('#message').html('Algo sali\u00f3 mal, por favor revisa la informaci\u00f3n y vuelve a intentarlo');
                        $('#bad_status_message').css('display', 'block')
                        setTimeout(function(){
                            $('#bad_status_message').css('display', 'none')
                        }, 4000);

                    });
                }, function () {
                    // console.log('dismiss modal')
                });
            }
            $scope.eliminaPerfil= function(nombre, id){
                $scope.e_perfil={
                    nombre:nombre,
                    id:id
                }

                var template = 'modal-eliminaPerfil.html';
                var modalInstance = $uibModal.open({
                    animation: $scope.animationsEnabled,
                    templateUrl: template,
                    controller: 'GenericModalInstanceCtrl',
                    size: 'lg',
                    scope: $scope
                });
                modalInstance.result.then(function () {
                    var req = {
                        url: $scope.url+$scope.e_perfil.id,
                        method: 'DELETE',
                        headers: {
                            'X-CSRFToken': csrftoken
                        },
                        data: {}
                    }
                    $http(req).then(function (response) {

                        $('#status_message').find('#message').html('Perfil eliminado satisfactoriamente');
                        $('#status_message').css('display', 'block')
                        setTimeout(function(){
                            $('#status_message').css('display', 'none')
                        }, 3000);
                        $scope.getPerfiles($scope.url);
                    }, function(response){
                        $('#bad_status_message').find('#message').html('No se ha podido eliminar este perfil, por favor vuelve a intentarlo');
                        $('#bad_status_message').css('display', 'block')
                        setTimeout(function(){
                            $('#bad_status_message').css('display', 'none')
                        }, 4000);
                    });
                }, function () {
                    // console.log('dismiss modal')
                });
            }
            $scope.getPerfiles()

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


    angular.bootstrap(document, ['Documentos'])
});