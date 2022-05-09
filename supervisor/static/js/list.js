var tblSale;

$(function () {
    
    tblSale = $('#liquidaciones').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        info: true,
        orderFixed: [ 1, 'dec' ],
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
            dataSrc: ""
        },
        columns: [
            { "data": "user" },
            { "data": "date" },
            { "data": "state" },
            { "data": "total" },
            { "data": "id" },
        ],
        columnDefs: [
            {
                targets: [-2],
                class: 'text-center',
                //orderable: false,
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(2);
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a rel="details" class="btn btn-info btn-xs btn-flat"><i class="fas fa-eye"></i></a> ';
                    if (row.state === 'pendiente') {
                        buttons += '<a rel="cancel" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-times"></i></a> ';
                        buttons += '<a rel="aproba" class="btn btn-success btn-xs btn-flat"><i class="fas fa-check"></i></a> ';
                    }
                    //var buttons = '<a href="/erp/sale/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    return buttons;
                }
            },
            {
                targets: [-3],
                class: 'text-center',
                render: function (data, type, row) {
                    if (data === 'aprobado') {
                        return '<span class="badge bg-success">' + data + '</span>';
                    } else if (data === 'cancelado') {
                        return '<span class="badge bg-danger">' + data + '</span>';
                    } else {
                        return '<span class="badge bg-warning">' + data + '</span>';
                    }

                }
            },
        ],

    });
    $('#liquidaciones tbody')
        .on('click', 'a[rel="details"]', function () {
            var tr = tblSale.cell($(this).closest('td, li')).index();
            var data = tblSale.row(tr.row).data();
            //console.log(data);

            $('#Det').DataTable({
                responsive: true,
                autoWidth: false,
                destroy: true,
                deferRender: true,
                searching: false,
                paging: false,
                info: false,
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
                ajax: {
                    url: window.location.pathname,
                    type: 'POST',
                    data: {
                        'action': 'search_details_prod',
                        'id': data.id
                    },
                    dataSrc: ""
                },
                columns: [
                    { "data": "product.name" },
                    { "data": "quantity" },
                    { "data": "price" },
                    { "data": "total" },
                ],
                columnDefs: [
                    {
                        targets: [-1, -2],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return '$' + parseFloat(data).toFixed(2);
                        }
                    },
                    {
                        targets: [-3],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return data;
                        }
                    },
                ],
                initComplete: function (settings, json) {

                }
            });

            $('#ModelDet').modal('show');
        });
    $('#liquidaciones tbody').on('click', 'a[rel="cancel"]', function () {
        var tr = tblSale.cell($(this).closest('td, li')).index();
        var data = tblSale.row(tr.row).data();
        //console.log(data);
        
        var parameters = new FormData(); // creo un nuevo formulario
        parameters.append('action', 'cancel_liquidations'); // envio el action para que pueda hacer las correspondientes operaciones
        parameters.append('id', data.id); // le paso el id del reporte a modificar
        
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            location.href = '/supervisor/liquidaciones';
        });
    });
    $('#liquidaciones tbody').on('click', 'a[rel="aproba"]', function () {
        var tr = tblSale.cell($(this).closest('td, li')).index();
        var data = tblSale.row(tr.row).data();
        console.log(data);
        var parameters = new FormData();
        parameters.append('action', 'aprobado_liquidations');
        parameters.append('vents', JSON.stringify(data));
        
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            location.href = '/supervisor/liquidaciones';
        });
       
    });
});

