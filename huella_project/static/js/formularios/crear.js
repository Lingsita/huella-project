$(function() {
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
            console.log(tipo)
            if(tipo=='number'){

                $('#insertaCampo').find('#ifNumber').css('display','block')
            }else{
                $('#insertaCampo').find('#ifNumber').css('display','none')
            }
            $('#insertaCampo').modal('show');


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

    appendDraggable= function (form){

        var contenedor=$('#campos');
        var tipo = form.find('#tipo').val();
        var nombre = form.find('#nombre').val();
        if(nombre==''){
            form.find('#nombre').focus();
            return
        }
        var id =formatString(form.find('#nombre').val());
        var val_min = form.find('#val_min').val();
        var val_max = form.find('#val_max').val();

        if(tipo=='textarea'){
            $( "<li></li>" ).html('<div id="item"><label class="span2" >'+nombre +':</label> <textarea class="span3" id="'+id+'"></textarea></div>').appendTo( contenedor );

        }else if(tipo=='file'){
            $( "<li></li>" ).html('<div id="item"><label class="span2" >'+nombre +':</label> <button class="btn" id="'+tipo +'" type="button">Subir Archivo</button><div class="hide" ><input id="'+id+'" type="'+tipo +'" /></div></div>').appendTo( contenedor );

        }else if(tipo=='radio' || tipo=='checkbox'){
            $( "<li></li>" ).html('<div id="item"><label class="span2" >'+nombre +':</label> <input id="'+id+'" type="'+tipo +'" /></div>').appendTo( contenedor );
        }else if (tipo=='number'){
            if(val_min == ''){
                form.find('#val_min').focus();
                return
            }else if(val_max == ''){
                form.find('#val_max').focus();
                return
            }else if(val_min > val_max ){
                form.find('#val_max').focus();
                return
            }

            $( "<li></li>" ).html('<div id="item"><label class="span2" >'+nombre +':</label> <input id="'+id+'" min="'+val_min+'" max="'+val_max+'" class="span3" type="'+tipo +'" /></div>').appendTo( contenedor );

        }else{
            $( "<li></li>" ).html('<div id="item"><label class="span2" >'+nombre +':</label> <input id="'+id+'" class="span3" type="'+tipo +'" /></div>').appendTo( contenedor );

        }

        $('#insertaCampo').modal('hide');
    }

    function formatString(cadena){
        var array = cadena.split(" ");

        return array.join("_");
    }
});