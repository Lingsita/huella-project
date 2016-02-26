/**
 * Created by linglung on 10/2/15.
 */
jQuery( document ).ready(function() {
    window.campos=[]
    var app = angular.module('formulariosApp', ['ngRoute','ui.bootstrap']);

    app.controller('formulariosCtrl',['$scope', '$http','$uibModal', function($scope, $http, $uibModal) {
         $scope.formularios = [];
         $scope.next=null;
         $scope.previous=null;
         $scope.current_page=null;
         $scope.page_number=null;
         $scope.count= 0;
         $scope.url='/api/formularios/formulario/'
         $scope.formatos_url='/api-empresas/formato/'
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
        $scope.empresa={
            id: "",
            name:""
        }

         var csrftoken = $("[name='csrfmiddlewaretoken']").val();
         $scope.e_form={
             nombre:null,
             id:null
         }

        $scope.verFormulario= function (id) {
            location.href=window.URL_VER_FORM+id
        }
        $scope.getFormularios = function () {
            $http.get($scope.url).success(function (response) {
                var pages_number=0
                $scope.previous=response.previous;
                $scope.next=response.next;
                $scope.count= parseInt(response.count)
                $scope.formularios = response.results;
                if($scope.previous==null) {
                    if ($scope.count != 0) {
                        $scope.pages_number = Math.ceil($scope.count / $scope.formularios.length);
                        $scope.paginate($scope.pages_number, $scope.previous, $scope.next, $scope.url);
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

        $scope.eliminaFormulario= function (form) {
            $scope.e_form=form
            var modalInstance = $uibModal.open({
                animation: $scope.animationsEnabled,
                templateUrl: 'modal-eliminaFormulario.html',
                controller: 'ModalInstanceCtrl',
                size: 'lg',
                scope:$scope
            });
            modalInstance.result.then(function (e_form) {
                var id= $scope.e_form.pk;
                var req = {
                    url: $scope.url+id,
                    method: 'DELETE',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                    data: {}
                }
                $http(req).then(function (response) {
                    $('#status_message').find('#message').html('Formulario eliminado satisfactoriamente');
                    $('#status_message').css('display', 'block')
                    setTimeout(function(){
                        $('#status_message').css('display', 'none')
                    }, 3000);
                    $scope.getFormularios($scope.url);
                }, function(response){
                    $('#bad_status_message').find('#message').html('No se pudo eliminar el formulario, por favor vuelve a intentarlo');
                    $('#bad_status_message').css('display', 'block')
                    setTimeout(function(){
                        $('#bad_status_message').css('display', 'none')
                    }, 4000);
                });

            }, function () {

            });
        }
        $scope.getFormularios();

    }])
    .controller('formatosCtrl',['$scope', '$http','$uibModal', function($scope, $http, $uibModal) {
         $scope.formularios = [];
         $scope.next=null;
         $scope.previous=null;
         $scope.current_page=null;
         $scope.page_number=null;
         $scope.count= 0;
         $scope.url='/api-empresas/formato/'
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
        $scope.empresa={
            id: "",
            name:""
        }

         var csrftoken = $("[name='csrfmiddlewaretoken']").val();
         $scope.e_form={
             nombre:null,
             id:null
         }

        $scope.verFormulario= function (id) {
            location.href=window.URL_VER_FORM+id
        }
        $scope.getFormularios = function () {
            $http.get($scope.url).success(function (response) {
                var pages_number=0
                $scope.previous=response.previous;
                $scope.next=response.next;
                $scope.count= parseInt(response.count)
                $scope.formularios = response.results;
                if($scope.previous==null) {
                    if ($scope.count != 0) {
                        $scope.pages_number = Math.ceil($scope.count / $scope.formularios.length);
                        $scope.paginate($scope.pages_number, $scope.previous, $scope.next, $scope.url);
                    }
                }
                console.log($scope.formularios)
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

        $scope.eliminaFormulario= function (form) {
            $scope.e_form=form
            var modalInstance = $uibModal.open({
                animation: $scope.animationsEnabled,
                templateUrl: 'modal-eliminaFormulario.html',
                controller: 'ModalInstanceCtrl',
                size: 'lg',
                scope:$scope
            });
            modalInstance.result.then(function (e_form) {
                var id= $scope.e_form.pk;
                var req = {
                    url: $scope.url+id,
                    method: 'DELETE',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                    data: {}
                }
                $http(req).then(function (response) {
                    $('#status_message').find('#message').html('Formulario eliminado satisfactoriamente');
                    $('#status_message').css('display', 'block')
                    setTimeout(function(){
                        $('#status_message').css('display', 'none')
                    }, 3000);
                    $scope.getFormularios($scope.url);
                }, function(response){
                    $('#bad_status_message').find('#message').html('No se pudo eliminar el formulario, por favor vuelve a intentarlo');
                    $('#bad_status_message').css('display', 'block')
                    setTimeout(function(){
                        $('#bad_status_message').css('display', 'none')
                    }, 4000);
                });

            }, function () {

            });
        }
        $scope.getFormularios();

    }])
    .controller('NuevoformatoCtrl',['$scope', '$http','$uibModal', '$log', '$filter',  function($scope, $http, $uibModal,  $log, $filter) {
            $scope.url='/api-empresas/formato/'
            $scope.formulario={
                nombre:"",
                descripcion:"",
                campos:[]
            }
            $scope.campos=[]
            $scope.campo={
                id_campo:'',
                nombre:'',
                tipo:'',
                descripcion:"",
                min:0,
                max:0
            }
            var csrftoken = $("[name='csrfmiddlewaretoken']").val();
            $scope.dropping= function () {
                $( "#tipos li" ).draggable({
                    appendTo: "body",
                    helper: "clone"
                });
                $( "#campos" ).droppable({
                    activeClass: "ui-state-default",
                    hoverClass: "ui-state-hover",
                    accept: ":not(.ui-sortable-helper)",
                    drop: function( event, ui ) {
                        $( this ).find( ".placeholder" ).remove();
                        var tipo=ui.draggable.attr('id');
                        $('#insertaCampo').find('#tipo').val(tipo)

                        if(tipo=='number'){
                            $('#insertaCampo').find('#ifNumber').css('display','block')
                        }else{
                            $('#insertaCampo').find('#ifNumber').css('display','none')
                        }
                        $scope.insertaCampo(tipo);

                        //                $( "<li></li>" ).text( ui.draggable.text() ).appendTo( this );
                    }
                }).sortable({
                    items: "li:not(.placeholder)",
                    sort: function() {
                        // gets added unintentionally by droppable interacting with sortable
                        // using connectWithSortable fixes this, but doesn't allow you to customize active/hoverClass options
                        $( this ).removeClass( "ui-state-default" );
                    }
                });
            }
            $scope.insertaCampo= function(tipo){
                var self = this
                var campos=[]

                $scope.campo.tipo=tipo;
                var template = 'modal-insertaCampo.html';
                var modalInstance = $uibModal.open({
                    animation: $scope.animationsEnabled,
                    templateUrl: template,
                    controller: 'CreaCampoModalCtrl',
                    size: 'lg',
                    scope: $scope
                });
                modalInstance.rendered.then(function () {

                    if($scope.campo.tipo=='number'){
                       $('#ifNumber').css('display','block')
                    }else{
                       $('#ifNumber').css('display','none')
                    }
                });
                modalInstance.result.then(function (campos) {
                      window.campos=campos
                }, function () {
                    // console.log('dismiss modal')
                });
            }

            $scope.guardarFormulario= function () {
                $scope.campos=window.campos
                $scope.formulario.campos=$scope.campos
                console.log($scope.formulario)
                var req = {
                    url: $scope.url,
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                    data: $scope.formulario
                }
                $http(req).then(function (response) {

                    $('#status_message').find('#message').html('Formulario creado satisfactoriamente');
                    $('#status_message').css('display', 'block')
                    setTimeout(function(){
                        $('#status_message').css('display', 'none')
                    }, 3000);
                }, function(response){
                    $('#bad_status_message').find('#message').html('No se pudo crear el formulario, por favor vuelve a intentarlo');
                    $('#bad_status_message').css('display', 'block')
                    setTimeout(function(){
                        $('#bad_status_message').css('display', 'none')
                    }, 4000);
                });
            }
            $scope.formatString= function (cadena){
                var array = cadena.split(" ");
                return array.join("_");
            }

            $scope.dropping();
        }])
        .controller('NuevoformularioCtrl',['$scope', '$http','$uibModal', '$log', '$filter',  function($scope, $http, $uibModal,  $log, $filter) {
            $scope.url='/api/formularios/formulario/'
            $scope.formulario={
                nombre:"",
                descripcion:"",
                campos:[]
            }
            $scope.campos=[]
            $scope.campo={
                id_campo:'',
                nombre:'',
                tipo:'',
                descripcion:"",
                min:0,
                max:0
            }
            var csrftoken = $("[name='csrfmiddlewaretoken']").val();
            $scope.dropping= function () {
                $( "#tipos li" ).draggable({
                    appendTo: "body",
                    helper: "clone"
                });
                $( "#campos" ).droppable({
                    activeClass: "ui-state-default",
                    hoverClass: "ui-state-hover",
                    accept: ":not(.ui-sortable-helper)",
                    drop: function( event, ui ) {
                        $( this ).find( ".placeholder" ).remove();
                        var tipo=ui.draggable.attr('id');
                        $('#insertaCampo').find('#tipo').val(tipo)

                        if(tipo=='number'){
                            $('#insertaCampo').find('#ifNumber').css('display','block')
                        }else{
                            $('#insertaCampo').find('#ifNumber').css('display','none')
                        }
                        $scope.insertaCampo(tipo);

                        //                $( "<li></li>" ).text( ui.draggable.text() ).appendTo( this );
                    }
                }).sortable({
                    items: "li:not(.placeholder)",
                    sort: function() {
                        // gets added unintentionally by droppable interacting with sortable
                        // using connectWithSortable fixes this, but doesn't allow you to customize active/hoverClass options
                        $( this ).removeClass( "ui-state-default" );
                    }
                });
            }
            $scope.insertaCampo= function(tipo){
                var self = this
                var campos=[]

                $scope.campo.tipo=tipo;
                var template = 'modal-insertaCampo.html';
                var modalInstance = $uibModal.open({
                    animation: $scope.animationsEnabled,
                    templateUrl: template,
                    controller: 'CreaCampoModalCtrl',
                    size: 'lg',
                    scope: $scope
                });
                modalInstance.rendered.then(function () {

                    if($scope.campo.tipo=='number'){
                       $('#ifNumber').css('display','block')
                    }else{
                       $('#ifNumber').css('display','none')
                    }
                });
                modalInstance.result.then(function (campos) {
                      window.campos=campos
                }, function () {
                    // console.log('dismiss modal')
                });
            }

            $scope.guardarFormulario= function () {
                $scope.campos=window.campos
                $scope.formulario.campos=$scope.campos
                console.log($scope.formulario)
                var req = {
                    url: $scope.url,
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                    data: $scope.formulario
                }
                $http(req).then(function (response) {

                    $('#status_message').find('#message').html('Formulario creado satisfactoriamente');
                    $('#status_message').css('display', 'block')
                    setTimeout(function(){
                        $('#status_message').css('display', 'none')
                    }, 3000);
                }, function(response){
                    $('#bad_status_message').find('#message').html('No se pudo crear el formulario, por favor vuelve a intentarlo');
                    $('#bad_status_message').css('display', 'block')
                    setTimeout(function(){
                        $('#bad_status_message').css('display', 'none')
                    }, 4000);
                });
            }
            $scope.formatString= function (cadena){
                var array = cadena.split(" ");
                return array.join("_");
            }

            $scope.dropping();
        }])

        .controller('ModalInstanceCtrl', function ($scope, $uibModalInstance) {

            $scope.ok = function () {
                $uibModalInstance.close($scope.e_form);
            };
            $scope.cancel = function () {
                $uibModalInstance.dismiss('cancel');
            };
        })
        .controller('CreaCampoModalCtrl', function ($scope, $uibModalInstance, $filter, $compile) {

            $scope.ok = function () {

                var contenedor=$('#campos');
                var tipo = $scope.campo.tipo;
                var nombre = $scope.campo.nombre;
                $('#nombre_error').html('')
                if(nombre==''){
                    $('#nombre').focus();
                    $('#nombre_error').html('*Ingrese un nombre')
                    return
                }

                var id =$scope.formatString($scope.campo.nombre);
                var val_min = $scope.campo.min
                var val_max = $scope.campo.max
                var filtro=$filter('filter')($scope.campos, id)
                if(filtro.length>0){
                    $('#nombre_error').html('*Ya existe un campo con este nombre')
                    return
                }
                if(tipo=='textarea'){
                    contenedor.append($compile('<li><div id="item"><label class="span2" >'+nombre +':</label> <textarea class="span3" id="'+id+'"></textarea><button class="pull-right" eliminacampo="'+id+'">Eliminar</button></div></li>')($scope))
//                    $( "<li></li>" ).html('<div id="item"><label class="span2" >'+nombre +':</label> <textarea class="span3" id="'+id+'"></textarea><button class="pull-right" ng-click="eliminarCampo()">Eliminar</button></div>').appendTo( contenedor );

                }else if(tipo=='file'){
                    contenedor.append($compile('<li><div id="item"><label class="span2" >'+nombre +':</label> <button class="btn" id="'+tipo +'" type="button">Subir Archivo</button><button class="pull-right" eliminacampo="'+id+'">Eliminar</button></div></li>')($scope))
//                    $( "<li></li>" ).html('<div id="item"><label class="span2" >'+nombre +':</label> <button class="btn" id="'+tipo +'" type="button">Subir Archivo</button><div class="hide" ><input id="'+id+'" type="'+tipo +'" /></div><button class="pull-right" ng-click="eliminarCampo()">Eliminar</button></div>').appendTo( contenedor );

                }else if(tipo=='radio' || tipo=='checkbox'){
                    contenedor.append($compile('<li><div id="item"><label class="span2" >'+nombre +':</label> <input id="'+id+'" type="'+tipo +'" /><button class="pull-right" eliminacampo="'+id+'">Eliminar</button></div></li>')($scope))
//                    $( "<li></li>" ).html('<div id="item"><label class="span2" >'+nombre +':</label> <input id="'+id+'" type="'+tipo +'" /><button class="pull-right" ng-click="eliminarCampo()">Eliminar</button></div>').appendTo( contenedor );

                }else if (tipo=='number'){
                    $('#val_min_error').html('')
                    $('#val_max_error').html('')
                    if(val_min == null){
                        $('#val_min').focus();
                        $('#val_min_error').html('*Ingrese un valor minimo')
                        return
                    }else if(val_max == null){
                        $('#val_max').focus();
                        $('#val_max_error').html('*Ingrese un valor máximo')
                        return
                    }else if(val_min >= val_max ){
                        $('#val_max').focus();
                        $('#val_max_error').html('*Este valor debe ser mayor al minimo')
                        return
                    }
                    else{
                        $('#val_min_error').html('')
                        $('#val_max_error').html('')
                        contenedor.append($compile('<li><div id="item"><label class="span2" >'+nombre +':</label> <input id="'+id+'" min="'+val_min+'" max="'+val_max+'" class="span3" type="'+tipo +'" /><button class="pull-right" eliminacampo="'+id+'">Eliminar</button></div></li>')($scope))
//                      $( "<li></li>" ).html('<div id="item"><label class="span2" >'+nombre +':</label> <input id="'+id+'" min="'+val_min+'" max="'+val_max+'" class="span3" type="'+tipo +'" /><button class="pull-right" ng-click="eliminarCampo()">Eliminar</button></div>').appendTo( contenedor );
                    }
                }else{
                    contenedor.append($compile('<li><div id="item"><label class="span2" >'+nombre +':</label> <input id="'+id+'" class="span3" type="'+tipo +'" /><button class="pull-right" eliminacampo="'+id+'">Eliminar</button></div></li>')($scope))
//                    $( "<li></li>" ).html($compile('<div id="item"><label class="span2" >'+nombre +':</label> <input id="'+id+'" class="span3" type="'+tipo +'" /><button class="pull-right" ng-click="eliminarCampo()">Eliminar</button></div>')($scope)).appendTo( contenedor );

                }
                $scope.campos.push(
                    {
                        id_campo:id,
                        nombre:$scope.campo.nombre,
                        tipo:$scope.campo.tipo,
                        descripcion:$scope.campo.descripcion,
                        min:$scope.campo.min,
                        max:$scope.campo.max
                    }
                )

                $uibModalInstance.close($scope.campos);
            };

            $scope.cancel = function () {
                $uibModalInstance.dismiss('cancel');
            };
        })
        .controller('GenericModalInstanceCtrl', function ($scope, $uibModalInstance) {

            $scope.ok = function () {
                $uibModalInstance.close();
            };

            $scope.cancel = function () {
                $uibModalInstance.dismiss('cancel');
            };
        })
        //Directive for deleting campo on click
        .directive("eliminacampo", function(){
            return function(scope, element, attrs){
                element.bind("click", function(){
                    
                    $.each( scope.campos, function( key, value ) {
                      alert( key + ": " + value );
                        $.each( value, function( key2, value2 ) {
                            if(key2=='id_campo'){
                                if(value2==attrs.eliminacampo){
//
                                    scope.campos.splice(key, 1);
                                    element.parent().parent().remove();
                                }
                            }
//                         console.log( key2 + ": " + value2 );
//                            console.log("IndexOf:" )
                        });
                    });
                });
            };
        });




    angular.bootstrap(document, ['formulariosApp'])
});