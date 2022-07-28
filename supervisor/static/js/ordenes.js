var tblSale;
$(function () {
    
    tblSale = $('#ordenes').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        info: false,
        orderFixed: [ 0, 'dec' ],
        language: {
            "decimal": "",
            "emptyTable": "No hay información",
            "info": "Mostrando _START_ a _END_ de _TOTAL_ Entradas",
            "infoEmpty": "Mostrando 0 to 0 of 0 Entradas",
            "infoFiltered": "(Filtrado de _MAX_ total entradas)",
            "infoPostFix": "",
            "thousands": ",",
            "lengthMenu": "Mostrar _MENU_ Entradas",
            "loadingRecords": "Cargando...",
            "processing": "Procesando...",
            "search": "Buscar:",
            "zeroRecords": "Sin resultados encontrados",
            "paginate": {
                "first": "Primero",
                "last": "Ultimo",
                "next": "Siguiente",
                "previous": "Anterior"
            }
        },
        //data: data.det,
        ajax: { // preparo la peticion ajax
            url: window.location.pathname, // como se esta trabajando en la misma url se coloca window.location.pathname
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: "",
        },
        columns: [
            { "data": "id" },
            { "data": "user" },
            { "data": "date" },
            { "data": "chips_sale" },
            { "data": "chips_portability" },
        ],
        columnDefs: [
            {
                targets: [-1, -2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    if (data > 0){
                        return '<span class="badge bg-success"> + ' + data + ' </span>';
                    } else if (data < 0){
                        return '<span class="badge bg-danger"> ' + data + ' </span>';
                    } else {
                        return data;
                    }
                }
            },
            {
                targets: [0],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '';
                }
            },
        ],
    });
    
    
});