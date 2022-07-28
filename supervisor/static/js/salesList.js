var tblSale;

$(function () {

    tblSale = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        info: false,
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
            { "data": "id" },
            { "data": "date" },
            { "data": "state" },
            { "data": "subtotal" },
            { "data": "discount" },
            { "data": "total" },
        ],
        columnDefs: [
            {
                targets: [-1, -2, -3],
                class: 'text-center',
                //orderable: false,
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(2);
                }
            },
            {
                targets: [-6],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a rel="details" class="btn btn-info btn-xs btn-flat"><i class="fas fa-eye"></i></a> ';
                    //var buttons = '<a href="#' + row.id + '/" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a> ';
                   
                    //var buttons = '<a href="/erp/sale/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    return buttons;
                }
            },
            {
                targets: [-4],
                class: 'text-center',
                render: function (data, type, row) {
                   
                    if (data === 'aprobado'){
                        return '<span class="badge bg-success">' + data + '</span>';
                    } else if (data === 'cancelado'){
                        return '<span class="badge bg-danger">' + data + '</span>';
                    } else if (data === 'finalizado'){
                        return '<span class="badge bg-info">' + data + '</span>';
                    } else {
                        return '<span class="badge bg-warning">' + data + '</span>';
                    }

                }
            },
        ],

    });

    $('#data tbody')
        .on('click', 'a[rel="details"]', function () {
            var tr = tblSale.cell($(this).closest('td, li')).index();
            var data = tblSale.row(tr.row).data();
            //console.log(data);

            $('#tblDet').DataTable({
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
                    { "data": "commission_paid" },
                    { "data": "commission_receivable" },
                    { "data": "total" },
                ],
                columnDefs: [
                    {
                        targets: [-1, -2, -3, -4],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return '$' + parseFloat(data).toFixed(2);
                        }
                    },
                    {
                        targets: [-5],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return data;
                        }
                    },
                ],
                initComplete: function (settings, json) {

                }
            });

            $('#myModelDet').modal('show');
        });

});