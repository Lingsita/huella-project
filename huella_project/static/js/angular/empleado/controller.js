/**
 * Created by linglung on 12/14/15.
 */
$( document ).ready(function(){

    var app= angular.module('Documentos', ['ngRoute','ui.bootstrap'])
        .config(function($routeProvider, $locationProvider) {
            $routeProvider
                .when('/proceso/:proceso_id', {
                    templateUrl: 'documento.html',
                    // controllerAs: 'documento',
                    controller: 'DocsCtrl'
                })
                .otherwise({
                    redirectTo: '/'
                })
            // $locationProvider.html5Mode(true).hashPrefix('!');
        })
        .controller('DocsCtrl', ['$scope', '$rootScope', '$http','$uibModal', '$routeParams',  function($scope, $rootScope, $http, $uibModal, $routeParams) {

            $scope.documentos = [];
            $scope.url='/api-empresas/documento/';
            $scope.url_procesos='/api-empresas/proceso/empleado';
            $scope.csrftoken = $("[name='csrfmiddlewaretoken']").val();
            $scope.id_proceso= $routeParams.proceso_id
            $scope.empty_text = true;

            // Pagination Schema
            $scope.currentPage=1;
            $scope.numPerPage=10;
            $scope.totalItems=1;
            $scope.filteredDocumentos = [];

            //paginate with django rest
            $scope.$watch('currentPage', function() {
                if($scope.id_proceso!="" && $scope.id_proceso!=null){
                    if ($scope.currentPage<=1){
                        $http.get($scope.url + $scope.id_proceso + '/by_proceso/').success(function (response) {
                            $scope.filteredDocumentos = response.results;
                        });
                    }else{
                        $http.get($scope.url + $scope.id_proceso + '/by_proceso/?page=' + $scope.currentPage).success(function (response) {
                            $scope.filteredDocumentos = response.results;
                        });
                    }
                }
            });
            //-- End of Pagination

            $scope.getDocumentos= function () {
                if($scope.id_proceso=="" || $scope.id_proceso==null){
                    location.href="/";
                }else {
                    $http.get($scope.url+$scope.id_proceso+'/by_proceso/').success(function (response) {

                        $scope.documentos = response.results;
                        $scope.totalItems =response.count;
                        if($scope.totalItems>0) {
                            $scope.nombre_proceso = response.results[0].proceso.nombre;
                            $scope.empty_text = false;
                        }else{
                            $scope.empty_text = true;
                        }
                    });
                }
            }

            $scope.verDocumento= function (pk) {
                location.href = window.mostrar_documento_url+pk;
            }
            
            $scope.nuevoDocumento = function () {
                location.href=window.nuevo_documento_url+$scope.id_proceso;
            }
            
            $scope.getDocumentos();
        }])
        .controller('DocumentoCtrl', ['$scope', '$rootScope', '$http','$uibModal', function($scope, $rootScope, $http, $uibModal) {
            $scope.documentos = []
            $scope.url_procesos='/api-empresas/proceso/';
            $scope.url='/api-empresas/documento/';
            $scope.nombre_proceso ='';
            $scope.animationsEnabled = true;

            $scope.csrftoken = $("[name='csrfmiddlewaretoken']").val();
            $scope.getDocumentos= function (id_proceso, nombre) {
                $rootScope.proceso = id_proceso;
                $scope.nombre_proceso=nombre;
                location.href = "#proceso/"+id_proceso;
            }

            $scope.getProcesos = function () {

                $http.get($scope.url_procesos+'empleado/').success(function (response) {
                    $scope.procesos = response.results;
                });
            }
            $scope.getProcesos();

            $scope.nuevoDocumentoByFormato = function (id) {
                location.href=window.nuevo_documento_by_formato_url+window.proceso+"/"+id;
            }

        }])
        .controller('NuevoDocumentoCtrl', ['$scope', '$rootScope', '$http','$uibModal', function($scope, $rootScope, $http, $uibModal) {
            $scope.documentos = []
            $scope.url_procesos='/api-empresas/proceso/';
            $scope.procesos=[];
            $scope.url='/api-empresas/documento/';
            $scope.fields={
                categoria:window.categoria,

                formato: '',
                formato_default: '',
                elaboro: '',
                proceso: '',
                codigo: '',
                tipo_documento: '',
                fecha_emision: '',
                paginas: '1',
                external_link: '',
                is_external:'',
                archivo: '',
                restringido: '0',
                ubicacion_original: '',
                version: '1'
            }
            $scope.proceso
            $scope.animationsEnabled = true;

            $scope.csrftoken = $("[name='csrfmiddlewaretoken']").val();

            $scope.getDocumentos= function (id_proceso) {
                $rootScope.proceso = id_proceso;
                location.href = "#proceso"

            }

            $scope.getProcesosByCategoria = function () {

                console.log($scope.fields.categoria)
                $http.get($scope.url_procesos+$scope.fields.categoria+'/procesos_by_category/').success(function (response) {

                    $scope.procesos = response.results;
                    console.log(response.results)
                    $('#id_proceso').empty()
                    console.log('current process:')
                    console.log($scope.fields.proceso)

                    $(response.results).each(function(i, v){
                        $('#id_proceso').append($("<option>", { value: v.pk, html: v.nombre }));

                    });
                });
            }
            $scope.enviar= function () {
                if($scope.fields.is_external==0){
                    if($('#id_archivo').get(0).files.length === 0){
                        return false;
                    }
                }
                $('#creaDocumento').submit()
            }
            $scope.abrirArchivo= function (field) {
                $('#id_'+field).click()
            }

            $scope.getProcesos = function () {
                $scope.fields.proceso=window.proceso
//                $http.get($scope.url_procesos+'empleado/').success(function (response) {
//                    $scope.procesos = response.results;
//
//                });
            }

            $scope.getProcesos();

            $scope.nuevoDocumentoByFormato = function (id) {
                location.href=window.nuevo_documento_by_formato_url+window.proceso+"/"+id;
            }
            $scope.openArchivoWindow = function () {

                $('#id_archivo').click()
            }
            $scope.tipoArchivo = function () {

                if($scope.fields.is_external=="1"){
                    $('.documento_archivo').css('display', 'none')
                    $('.documento_url').css('display', 'block')
                }else if($scope.fields.is_external=='0'){
                    $('.documento_url').css('display', 'none')
                    $('.documento_archivo').css('display', 'block')
                }
            }
        }])
        .controller('NuevaVersionDocumentoCtrl', ['$scope', '$rootScope', '$http','$uibModal', function($scope, $rootScope, $http, $uibModal) {
            $scope.fields={
                external_link: '',
                is_external:'',
                archivo: '',
            }
            $scope.animationsEnabled = true;

            $scope.csrftoken = $("[name='csrfmiddlewaretoken']").val();

            $scope.enviar= function () {
                if($scope.fields.is_external==0){
                    if($('#id_archivo').get(0).files.length === 0){
                        return false;
                    }
                }
                $('#creaDocumento').submit()
            }
            $scope.abrirArchivo= function (field) {
                $('#id_'+field).click()
            }

            $scope.openArchivoWindow = function () {

                $('#id_archivo').click()
            }
            $scope.tipoArchivo = function () {

                if($scope.fields.is_external=="1"){
                    $('.documento_archivo').css('display', 'none')
                    $('.documento_url').css('display', 'block')
                }else if($scope.fields.is_external=='0'){
                    $('.documento_url').css('display', 'none')
                    $('.documento_archivo').css('display', 'block')
                }
            }
        }])

        .controller('GenericModalInstanceCtrl', function ($scope, $uibModalInstance) {
            $scope.ok = function () {
                $uibModalInstance.close($scope.foto);
            };

            $scope.cancel = function () {

                $uibModalInstance.dismiss('cancel');
            };
        })
        .directive('validFile',function(){
          return {
            require:'ngModel',
            link:function(scope,el,attrs,ngModel){
              //change event is fired when file is selected
              el.bind('change',function(){
                scope.$apply(function(){
                  ngModel.$setViewValue(el.val());
                  ngModel.$render();
                })
              })
            }
          }
        })
        .directive("dateBefore", [function () {
            return {
                require: 'ngModel',
                link: function (scope, element, attributes, ctrl) {
                    ctrl.$validators.datebefore = function(modelValue, viewValue) {

                        if (ctrl.$isEmpty(modelValue)) {
                          // tratamos los modelos vacíos como correctos
                          return false;
                        }
                        if (viewValue) {
                          var letterValue = viewValue.substr(viewValue.length - 1);
                          var numberValue = viewValue.substr(viewValue.length - (viewValue.length - 1));
                          var controlLetter = "TRWAGMYFPDXBNJZSQVHLCKE".charAt(numberValue % 23);


                            if(letterValue === controlLetter ){
                              return true;
                            } else {
                              return false;
                            }
                        }
                      // NIF inválido
                      return false;
                      };
                }
            }
        }])
        .filter('dateString', ['$filter', function($filter) {
            return function(input) {
                var date = $filter('date')(input, "yyyy-MM-dd 'hora:' hh:mma");
                return date.toString()
            };
        }]);


    angular.bootstrap(document, ['Documentos'])
});