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
                    controller: 'ProcesosCtrl'
                })
                .when('/perfiles', {
                    templateUrl: 'perfiles.html',
                    controller: 'PerfilesCtrl'
                })
                .when('/tareas', {
                    templateUrl: 'tareas.html',
                    controller: 'TareasCtrl'
                })
                .otherwise({
                    redirectTo: '/procesos'
                })
            // $locationProvider.html5Mode(true).hashPrefix('!');
        })
        .controller('EmpleadosCtrl', ['$scope', '$http','$uibModal', 'fileUpload', 'ShowMessage', function($scope, $http, $uibModal, fileUpload, ShowMessage) {
            $scope.empleados = []
            $scope.datos = {
                nombre : "",
                apellido : "",
                direccion : "",
                tipo_documento:"",
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
//                            $scope.getEmpleados($scope.url);
                        }
                    }
                });
            }

            $scope.getEmpleado = function (id) {
                $http.get($scope.url+id).success(function (response) {

                    $scope.current_empleado=response

                    $scope.current_empleado.email=response.usuario.user.email

                    console.log(response)

                    var template = 'modal-verEmpleado.html';
                    var modalInstance = $uibModal.open({
                        animation: $scope.animationsEnabled,
                        templateUrl: template,
                        controller: 'GenericFotoModalInstanceCtrl',
                        size: 'lg',
                        scope: $scope
                    });
                    modalInstance.result.then(function () {
                            $scope.current_empleado.perfil=$scope.current_empleado.perfil.id.toString()
                            var modalInstance = $uibModal.open({
                                animation: $scope.animationsEnabled,
                                templateUrl: 'modal-modificaEmpleado.html',
                                controller: 'GenericFotoModalInstanceCtrl',
                                size: 'lg',
                                scope: $scope
                            });
                            modalInstance.result.then(function (foto) {
                                $scope.mfoto=foto

                                console.log($scope.current_empleado)
                                var file = $scope.mfoto;
                                var req = {
                                    url: $scope.url+$scope.current_empleado.pk+"/",
                                    method: 'PUT',
                                    headers: {
                                        'X-CSRFToken': csrftoken
                                    },
                                    data: $scope.current_empleado
                                }

                                $http(req).then(function (response) {

                                    $('#status_message').find('#message').html('El Empleado fue actualizado correctamente');
                                    $('#status_message').css('display', 'block')
                                    setTimeout(function(){
                                        $('#status_message').css('display', 'none')
                                    }, 3000);
                                    $scope.getEmpleados()

                                    var file = $scope.mfoto;
                                    var uploadUrl = $scope.url + response.data.pk + "/upload_foto/?id=" + response.data.pk;
                                    fileUpload.uploadFileToUrl(file, uploadUrl, csrftoken);

                                }, function(response){
                                    var message=""
                                    $.each(response.data, function (i, e) {
                                        message+=e
                                    })
                                    $('#bad_status_message').find('#message').html(message+'. Algo sali\u00f3 mal, por favor revisa la informaci\u00f3n y vuelve a intentarlo');
                                    $('#bad_status_message').css('display', 'block')
                                    setTimeout(function(){
                                        $('#bad_status_message').css('display', 'none')
                                    }, 5000);

                                });
                            }, function () {
                                // console.log('dismiss modal')
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
                        ShowMessage.successMessage('Usuario Creado Satisfactoriamente');
                        var uploadUrl = $scope.url+response.data.pk+"/upload_foto/?id="+response.data.pk;
                        fileUpload.uploadFileToUrl(file, uploadUrl, csrftoken);

                    }, function(response){
                        ShowMessage.errorMessage(response.data.message);
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

            $scope.eliminaEmpleado= function(nombre,perfil, id){
                $scope.e_empleado={
                    nombre:nombre,
                    perfil:perfil,
                    id:id
                }
                console.log($scope.e_empleado)
                var template = 'modal-eliminaEmpleado.html';
                var modalInstance = $uibModal.open({
                    animation: $scope.animationsEnabled,
                    templateUrl: template,
                    controller: 'GenericModalInstanceCtrl',
                    size: 'lg',
                    scope: $scope
                });
                modalInstance.result.then(function () {
                    var req = {
                        url: $scope.url+$scope.e_empleado.id,
                        method: 'DELETE',
                        headers: {
                            'X-CSRFToken': csrftoken
                        },
                        data: {}
                    }
                    $http(req).then(function (response) {

                        $('#status_message').find('#message').html('Empleado eliminado satisfactoriamente');
                        $('#status_message').css('display', 'block')
                        setTimeout(function(){
                            $('#status_message').css('display', 'none')
                        }, 3000);
                        $scope.getEmpleados();
                    }, function(response){
                        $('#bad_status_message').find('#message').html('No se ha podido eliminar al Empleado, por favor vuelve a intentarlo');
                        $('#bad_status_message').css('display', 'block')
                        setTimeout(function(){
                            $('#bad_status_message').css('display', 'none')
                        }, 4000);
                    });
                }, function () {
                    // console.log('dismiss modal')
                });
            }
            $scope.getEmpleados()

        }])
        .controller('ProcesosCtrl', ['$scope', '$http','$uibModal', function($scope, $http, $uibModal) {
            $scope.procesos = []
            $scope.current_proceso = {
                nombre : "",
                categoria:[],
                codigo:"",
                descripcion:"",
                formatos_asignados:[]
            }
            $scope.datos = {
                nombre : "",
                categoria:"",
                codigo:"",
                descripcion:"",
                formatos_asignados:[]
            }
            $scope.e_proceso={
                nombre:"",
                id:""
            }
            $scope.categoria={
                nombre:'',
                descripcion:'',
                empresa:''
            }

            $scope.url='/api-empresas/proceso/';
            $scope.url_categoria='/api-empresas/categoria/';
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
//                            $scope.getProcesos($scope.url);
                        }
                    }
                });
            }
            $scope.getProceso = function (id) {
                $http.get($scope.url+id).success(function (response) {

                    $scope.current_proceso=response

                    var formatos_asignados=$scope.current_proceso.formatos_asignados
                    var selected_formatos=[]
                    $.each(formatos_asignados, function(i,e){
                        selected_formatos.push(''+ e.id +'')
                    });
                    $scope.current_proceso.categoria=$scope.current_proceso.categoria.id.toString()
                    $scope.current_proceso.formatos_asignados=selected_formatos
                    var template = 'modal-modificaProceso.html';
                    var modalInstance = $uibModal.open({
                        animation: $scope.animationsEnabled,
                        templateUrl: template,
                        controller: 'GenericModalInstanceCtrl',
                        size: 'lg',
                        scope: $scope
                    });
                    modalInstance.result.then(function () {

                        console.log($scope.current_proceso)
                        var req = {
                            url: $scope.url+$scope.current_proceso.pk+"/",
                            method: 'PUT',
                            headers: {
                                'X-CSRFToken': csrftoken
                            },
                            data: $scope.current_proceso
                        }

                        $http(req).then(function (response) {

                            $('#status_message').find('#message').html('El Proceso fue actualizado correctamente');
                            $('#status_message').css('display', 'block')
                            setTimeout(function(){
                                $('#status_message').css('display', 'none')
                            }, 3000);

                            $scope.getProcesos()

                        }, function(response){
                            var message=""
                            $.each(response.data, function (i, e) {
                                message+=e
                            })
                            $('#bad_status_message').find('#message').html(message+'. Algo sali\u00f3 mal, por favor revisa la informaci\u00f3n y vuelve a intentarlo');
                            $('#bad_status_message').css('display', 'block')
                            setTimeout(function(){
                                $('#bad_status_message').css('display', 'none')
                            }, 5000);

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

                    $scope.datos.formatos_asignados=[]
                    $scope.datos.formatos_asignados=$('input[name=formatos_asignados]:checked').map(function(_, el) {
                        return $(el).val();
                    }).get();

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
                        $('#status_message').find('#message').html('Proceso creado exitosamente');
                        $('#status_message').css('display', 'block')

                        setTimeout(function(){
                            $('#status_message').css('display', 'none')
                        }, 3000);

                        $scope.getProcesos();
                    }, function(response){

                        var message=""
                        $.each(response.data, function (i, e) {
                            message+=e
                        })
                        $('#bad_status_message').find('#message').html(message+'. No se ha podido crear este proceso, por favor vuelve a intentarlo.');
                        $('#bad_status_message').css('display', 'block')
                        setTimeout(function(){
                            $('#bad_status_message').css('display', 'none')
                        }, 5000);
                    });
                }, function () {
                    // console.log('dismiss modal')
                });
            }
            $scope.creaCategoria = function () {
                var template = 'modal-creaCategoria.html';
                var modalInstance = $uibModal.open({
                    animation: $scope.animationsEnabled,
                    templateUrl: template,
                    controller: 'GenericModalInstanceCtrl',
                    size: 'lg',
                    scope: $scope
                });

                modalInstance.result.then(function () {
                    $scope.categoria.empresa=$('#id_categoria_empresa').val()
                    var req = {
                        url: $scope.url_categoria,
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': csrftoken
                        },
                        data: $scope.categoria
                    }
                     console.log($scope.categoria)
                    $http(req).then(function (response) {

                        $('#status_message').find('#message').html('Categoria creada exitosamente');
                        $('#status_message').css('display', 'block')
                        setTimeout(function(){
                            $('#status_message').css('display', 'none')
                        }, 3000);
                        location.reload();
                        $scope.getProcesos();
                    }, function(response){

                        var message=""
                        $.each(response.data, function (i, e) {
                            message+=e
                        })
                        $('#bad_status_message').find('#message').html(message+'. No se ha podido crear esta categoria, por favor vuelve a intentarlo.');
                        $('#bad_status_message').css('display', 'block')
                        setTimeout(function(){
                            $('#bad_status_message').css('display', 'none')
                        }, 5000);
                    });
                }, function () {
                    // console.log('dismiss modal')
                });
            }
            $scope.eliminaProceso= function(nombre, id){
                $scope.e_proceso={
                    nombre:nombre,
                    id:id
                }
                var template = 'modal-eliminaProceso.html';
                var modalInstance = $uibModal.open({
                    animation: $scope.animationsEnabled,
                    templateUrl: template,
                    controller: 'GenericModalInstanceCtrl',
                    size: 'lg',
                    scope: $scope
                });
                modalInstance.result.then(function () {
                    var req = {
                        url: $scope.url+$scope.e_proceso.id,
                        method: 'DELETE',
                        headers: {
                            'X-CSRFToken': csrftoken
                        },
                        data: {}
                    }
                    $http(req).then(function (response) {
                        $('#status_message').find('#message').html('Proceso eliminado satisfactoriamente');
                        $('#status_message').css('display', 'block')
                        setTimeout(function(){
                            $('#status_message').css('display', 'none')
                        }, 3000);
                        $scope.getProcesos();
                    }, function(response){
                        $('#bad_status_message').find('#message').html('No se ha podido eliminar este proceso, por favor vuelve a intentarlo');
                        $('#bad_status_message').css('display', 'block')
                        setTimeout(function(){
                            $('#bad_status_message').css('display', 'none')
                        }, 4000);
                    });
                }, function () {
                    // console.log('dismiss modal')
                });
            }
            $scope.getProcesos()

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
        .controller('TareasCtrl', ['$scope', '$http','$uibModal', function($scope, $http, $uibModal) {
            $scope.tareas = []
            $scope.tarea = {
                nombre : "",
                descripcion:"",
                fecha_fin:""
            }
            $scope.json_empleados=[]
            $scope.empleados=[]
            $scope.url='/api-empresas/tarea/';
            $scope.next=null;
            $scope.previous=null;
            $scope.current_page=null;
            $scope.page_number=null;
            $scope.animationsEnabled = true;
            $scope.count= 0;
            $scope.e_tarea={}
            $scope.getTareasAutocomplete= function () {

                var tareas = [
                  {
                    value: "jquery",
                    label: "jQuery",
                    desc: "the write less, do more, JavaScript library",
                    icon: "jquery_32x32.png"
                  },
                  {
                    value: "jquery-ui",
                    label: "jQuery UI",
                    desc: "the official user interface library for jQuery",
                    icon: "jqueryui_32x32.png"
                  },
                  {
                    value: "sizzlejs",
                    label: "Sizzle JS",
                    desc: "a pure-JavaScript CSS selector engine",
                    icon: "sizzlejs_32x32.png"
                  }
                ];

                $( "#tarea" ).autocomplete({
                    minLength: 0,
                    source: tareas,
                    focus: function( event, ui ) {
                        $( "#tarea" ).val( ui.item.label );
                        return false;
                    },
                    select: function( event, ui ) {
                        $( "#tarea" ).val( ui.item.label );
                        $( "#project-id" ).val( ui.item.value );
                        return false;
                    }
                })
                    .autocomplete( "instance" )._renderItem = function( ul, item ) {
                    return $( "<li>" )
                        .append( "<a>" + item.label + "<br></a>" )
                        .appendTo( ul );
                };
            }
            $scope.getEmpleadoAutocomplete= function () {
                var empleados = []
                $scope.empleadosService($scope.tarea.perfil, function () {

                    $.each($scope.empleados, function(i,e){

                        empleados.push({
                            value: e.pk,
                            label: e.nombre +" "+ e.apellido
                        })
                    });

                    $scope.json_empleados=empleados
                    console.log("json_empleados")
                    console.log($scope.json_empleados)
                    console.log("empleados")
                    console.log(empleados)

                     $( "#empleado_tarea" ).autocomplete({
                        minLength: 0,
                        source: $scope.json_empleados
                     });
                })
            }
            $scope.getEmpleadoAutocompleteM= function () {
                var empleados = []
                $scope.empleadosService($scope.current_tarea.perfil, function () {

                    $.each($scope.empleados, function(i,e){

                        empleados.push({
                            value: e.pk,
                            label: e.nombre +" "+ e.apellido
                        })
                    });

                    $scope.json_empleados=empleados
                    console.log("json_empleados")
                    console.log($scope.json_empleados)
                    console.log("empleados")
                    console.log(empleados)

                     $( "#current_empleado_tarea" ).autocomplete({
                        minLength: 0,
                        source: $scope.json_empleados
                     });
                })
            }
            $scope.empleadosService= function (perfil, callback) {
                if(perfil==""|| perfil==null){

                }else{
                    $http.get('/api-empresas/empleado/'+perfil+'/get_empleados_by_perfil/').success(function (response) {

                        if(response.count>0){
                            $('#empleado_tarea').css('display', 'inline-block')
                        }else{
                             $('#empleado_tarea').css('display', 'none')
                        }

                        $scope.empleados =response.results;

                        callback();

                    });
                }
            }
            $scope.empleadosServiceM= function (perfil, callback) {
                if(perfil==""|| perfil==null){

                }else{
                    $http.get('/api-empresas/empleado/'+perfil+'/get_empleados_by_perfil/').success(function (response) {

                        if(response.count>0){
                            $('#current_empleado_tarea').css('display', 'inline-block')
                        }else{
                             $('#current_empleado_tarea').css('display', 'none')
                        }

                        $scope.empleados =response.results;

                        callback();

                    });
                }
            }

            $scope.buscarTareas = function () {

                $http.get($scope.url+window.empresa+'/get_tareas/').success(function (response) {
                    var pages_number=0
                    $scope.previous=response.previous;
                    $scope.next=response.next;
                    $scope.count= parseInt(response.count)
                    $scope.tareas = response.results;
                    if($scope.previous==null) {
                        if ($scope.count != 0) {
                            $scope.pages_number = Math.ceil($scope.count / $scope.tareas.length);
                            $scope.paginate($scope.pages_number, $scope.previous, $scope.next, $scope.url);

                        } else {

                        }
                    }

                });
            }
            $scope.getTareas = function () {

                $http.get($scope.url+window.empresa+'/get_tareas/').success(function (response) {
                    var pages_number=0
                    $scope.previous=response.previous;
                    $scope.next=response.next;
                    $scope.count= parseInt(response.count)
                    $scope.tareas = response.results;
                    if($scope.previous==null) {
                        if ($scope.count != 0) {
                            $scope.pages_number = Math.ceil($scope.count / $scope.tareas.length);
                            $scope.paginate($scope.pages_number, $scope.previous, $scope.next, $scope.url);

                        } else {

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

            $scope.creaTarea = function () {
                $scope.getEmpleadoAutocomplete()
                var template = 'modal-creaTarea.html';
                var modalInstance = $uibModal.open({
                    animation: $scope.animationsEnabled,
                    templateUrl: template,
                    controller: 'GenericModalInstanceCtrl',
                    size: 'lg',
                    scope: $scope

                });
                modalInstance.rendered.then(function(){

                    $( "#empleado_tarea" ).autocomplete({
                        minLength: 0,
                        source: $scope.json_empleados,
                        focus: function( event, ui ) {
                            $( "#empleado_tarea" ).val( ui.item.label );
                            return false;
                        },
                        select: function( event, ui ) {
                            $( "#empleado_tarea" ).val( ui.item.label );
                            $scope.tarea.empleado= ui.item.value;
                            return false;
                        }
                    })
                        .autocomplete( "instance" )._renderItem = function( ul, item ) {
                        return $( "<li>" )
                            .append( "<a>" + item.label + "<br></a>" )
                            .appendTo( ul );
                    };

                    jQuery.datetimepicker.setLocale('es');

                    jQuery('#id_fecha_fin').datetimepicker({
                        format:'Y-m-d H:i',
                        minDate:0
                    });
                    var myDate = new Date();
                    var prettyDate =myDate.getFullYear()+'-'+(myDate.getMonth()+1) + '-' + myDate.getDate()+' '+myDate.getHours()+':'+myDate.getMinutes();
                    $("#id_fecha_fin").val(prettyDate);
                });

                modalInstance.result.then(function () {

                    if($scope.tarea.fecha_fin==""){
                        $scope.tarea.fecha_fin=$("#id_fecha_fin").val()
                    }
                    console.log($scope.tarea)
                    var req = {
                        url: $scope.url,
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': csrftoken
                        },
                        data: $scope.tarea
                    }
                    $http(req).then(function (response) {
                        $scope.getTareas()
                        $('#status_message').find('#message').html('La tarea fue creada correctamente');
                        $('#status_message').css('display', 'block')
                        setTimeout(function(){
                            $('#status_message').css('display', 'none')
                        }, 3000);

                    }, function(response){
                        $('#bad_status_message').find('#message').html('No se ha podido crear esta tarea, por favor vuelve a intentarlo');
                        $('#bad_status_message').css('display', 'block')
                        setTimeout(function(){
                            $('#bad_status_message').css('display', 'none')
                        }, 4000);

                    });
                }, function () {
                    // console.log('dismiss modal')
                });
            }
            $scope.getTarea = function (id) {
                $http.get($scope.url+id).success(function (response) {
                    $scope.current_tarea = response
                    $scope.current_tarea.perfil = response.empleado.perfil.toString()
                    $scope.getEmpleadoAutocompleteM()

                    var template = 'modal-modificaTarea.html';
                    var modalInstance = $uibModal.open({
                        animation: $scope.animationsEnabled,
                        templateUrl: template,
                        controller: 'GenericModalInstanceCtrl',
                        size: 'lg',
                        scope: $scope

                    });
                    modalInstance.rendered.then(function () {

                        $("#current_empleado_tarea").autocomplete({
                            minLength: 0,
                            source: $scope.json_empleados,
                            focus: function (event, ui) {
                                $("#current_empleado_tarea").val(ui.item.label);
                                return false;
                            },
                            select: function (event, ui) {
                                $("#current_empleado_tarea").val(ui.item.label);
                                $scope.current_tarea.empleado = ui.item.value;
                                return false;
                            }
                        })
                            .autocomplete("instance")._renderItem = function (ul, item) {
                            return $("<li>")
                                .append("<a>" + item.label + "<br></a>")
                                .appendTo(ul);
                        };

                        jQuery.datetimepicker.setLocale('es');

                        jQuery('#id_fecha_fin').datetimepicker({
                            format: 'Y-m-d H:i',
                            minDate: 0
                        });
                    });

                    modalInstance.result.then(function () {

                        if ($scope.current_tarea.fecha_fin == "") {
                            $scope.current_tarea.fecha_fin = $("#id_current_fecha_fin").val()
                        }
                        console.log($scope.current_tarea)
                        var req = {
                            url: $scope.url+$scope.current_tarea.pk+"/",
                            method: 'PUT',
                            headers: {
                                'X-CSRFToken': csrftoken
                            },
                            data: $scope.current_tarea
                        }
                        $http(req).then(function (response) {
                            $scope.getTareas()
                            $('#status_message').find('#message').html('La tarea fue modificada correctamente');
                            $('#status_message').css('display', 'block')
                            setTimeout(function () {
                                $('#status_message').css('display', 'none')
                            }, 3000);

                        }, function (response) {
                            $('#bad_status_message').find('#message').html('No se ha podido modificar esta tarea, por favor revisa los datos ingresados y vuelve a intentarlo');
                            $('#bad_status_message').css('display', 'block')
                            setTimeout(function () {
                                $('#bad_status_message').css('display', 'none')
                            }, 4000);

                        });
                    }, function () {
                        // console.log('dismiss modal')
                    });
                });
            }
            $scope.eliminaTarea= function(nombre, id){
                $scope.e_tarea={
                    nombre:nombre,
                    id:id
                }

                var template = 'modal-eliminaTarea.html';
                var modalInstance = $uibModal.open({
                    animation: $scope.animationsEnabled,
                    templateUrl: template,
                    controller: 'GenericModalInstanceCtrl',
                    size: 'lg',
                    scope: $scope
                });
                modalInstance.result.then(function () {
                    var req = {
                        url: $scope.url+$scope.e_tarea.id,
                        method: 'DELETE',
                        headers: {
                            'X-CSRFToken': csrftoken
                        },
                        data: {}
                    }
                    $http(req).then(function (response) {

                        $('#status_message').find('#message').html('Tarea eliminada satisfactoriamente');
                        $('#status_message').css('display', 'block')
                        setTimeout(function(){
                            $('#status_message').css('display', 'none')
                        }, 3000);
                        $scope.getTareas($scope.url);
                    }, function(response){
                        $('#bad_status_message').find('#message').html('No se ha podido eliminar esta tarea, por favor vuelve a intentarlo');
                        $('#bad_status_message').css('display', 'block')
                        setTimeout(function(){
                            $('#bad_status_message').css('display', 'none')
                        }, 4000);
                    });
                }, function () {
                    // console.log('dismiss modal')
                });
            }
            $scope.getTareas()

        }])
        .controller('GenericModalInstanceCtrl', function ($scope, $uibModalInstance) {
            $scope.ok = function () {
                $uibModalInstance.close($scope.foto);
            };

            $scope.cancel = function () {

                $uibModalInstance.dismiss('cancel');
            };
        })
        .controller('GenericFotoModalInstanceCtrl', function ($scope, $uibModalInstance) {
            $scope.ok = function () {
                console.log($scope.mfoto)
                $uibModalInstance.close($scope.mfoto);
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
    }])
    .factory('ShowMessage', [function(){
        return {
            errorMessage : function(message){
                $('#bad_status_message').find('#message').html(message);
                $('#bad_status_message').css('display', 'block')
                setTimeout(function(){
                    $('#bad_status_message').css('display', 'none')
                }, 3000);
            },
            successMessage : function(message){
                $('#status_message').find('#message').html(message);
                $('#status_message').css('display', 'block')
                setTimeout(function(){
                    $('#status_message').css('display', 'none')
                }, 3000);
            }
        }
    }]);

    angular.bootstrap(document, ['Empleados'])


});