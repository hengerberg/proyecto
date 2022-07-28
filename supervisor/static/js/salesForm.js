var tblProducts;
var vents = {
    items: {
        date: '',
        subtotal: 0.00,
        commission_paid: 0.00,
        commission_receivable: 0.00,
        disc: 0.00,
        total: 0.00,
        products: []
    },

    get_ids: function () {
        var ids = [];
        $.each(this.items.products, function (key, value) {
            ids.push(value.id);
        });
        return ids;
    },
    calculate_report: function () {
        var subtotal = 0.00;
        var commission_paid = 0.00;
        var commission_receivable = 0.00;
       
        var discount = $('input[name="discount"]').val();

        $.each(this.items.products, function (pos, dict) {
            // imput del form subtotal
            subtotal += parseFloat(dict.total);
        });
        this.items.subtotal = subtotal;
        this.items.commission_paid = commission_paid;
        this.items.commission_receivable = commission_receivable;
       
        this.items.discount = discount
        this.items.total = this.items.subtotal - this.items.discount;

        $('input[name="subtotal"]').val(this.items.subtotal.toFixed(2));
        $('input[name="total"]').val(this.items.total.toFixed(2));
    },
    add: function (item) {
        this.items.products.push(item);
        this.list();
    },
    list: function () {
        this.calculate_report();

        tblProducts = $('#tblProducts').DataTable({
            responsive: true,
            searching: false,
            paging: false,
            info: false,
            autoWidth: false,
            destroy: true,
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
            data: this.items.products,
            columns: [
                { "data": "id" },
                { "data": "user" },
                { "data": "date" },
                { "data": "total" },
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var buttons = '<a rel="remove" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a> ';

                        return buttons;
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
            ],
            initComplete: function (settings, json) {
            }
        });
        console.clear();
        console.log(this.items);
        //console.log(this.get_ids());
    },
};

$(function () {
    $("input[name='discount']").TouchSpin({
        min: 0,
        max: 100,
        step: 0.25,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '$'
    }).on('change', function () {
        vents.calculate_report();
    }).val(0.00);

    $('#date').datetimepicker({
        locale: 'es',
        format: 'YYYY-MM-DD',
        date: moment().format('YYYY-MM-DD'),
        maxDate: moment().format('YYYY-MM-DD'),
    });

    $('#details').on('click', function () {
        vents.items.products = [];
        vents.list();
    });
    
    // event eliminar
    $('#tblProducts tbody')
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            alert_action('Notificación', '¿Estas seguro de eliminar el producto de tu detalle?',
                function () {
                    vents.items.products.splice(tr.row, 1);
                    vents.list();
                }, function () {
                });
        })

    $(function () {
        tblSearchProducts = $('#tblSearchProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
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
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_products',
                    'ids': JSON.stringify(vents.get_ids()),
                    'term': $('select[name="search"]').val()
                },
                dataSrc: ""
            },
            columns: [
                { "data": "user" },
                { "data": "date" },
                { "data": "total" },
                { "data": "id" },
            ],
            columnDefs: [
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var buttons = '<a rel="add" class="btn btn-success btn-xs btn-flat"><i class="fas fa-plus"></i></a> ';
                        buttons += ' <a rel="details" class="btn btn-info btn-xs btn-flat"><i class="fas fa-eye"></i></a> ';
                        return buttons;
                    }
                },
            ],
            initComplete: function (settings, json) {
            }
        });
    });

    $('#tblSearchProducts tbody')
        .on('click', 'a[rel="add"]', function () {
            var tr = tblSearchProducts.cell($(this).closest('td, li')).index();
            var product = tblSearchProducts.row(tr.row).data(); // guardo el producto en la variable product
            vents.add(product); // inserto el producto en la tabla tblProducts
            //console.log(product);
            tblSearchProducts.row($(this).parents('tr')).remove().draw(); // elimino el producto

        })
        .on('click', 'a[rel="details"]', function () {
            var tr = tblSearchProducts.cell($(this).closest('td, li')).index();
            var data = tblSearchProducts.row(tr.row).data();
            //console.log(data);
            tblDetProducts = $('#Det').DataTable({
                responsive: true,
                autoWidth: false,
                destroy: true,
                deferRender: true,
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
                ajax: {
                    url: window.location.pathname,
                    type: 'POST',
                    data: {
                        'action': 'search_details_prod',
                        'ids': JSON.stringify(vents.get_ids()),
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
                        targets: [-3],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return '<span class="badge badge-secondary">' + data + '</span>';
                        }
                    },
                    {
                        targets: [-2, -1],
                        class: 'text-center',
                        orderable: false,
                        render: function (data, type, row) {
                            return '$' + parseFloat(data).toFixed(2);
                        }
                    },
                ],
                initComplete: function (settings, json) {
                }
            });
            $('#ModelDet').modal('show');
        });

    // event submit
    $('form').on('submit', function (e) {
        e.preventDefault();

        if (vents.items.products.length === 0) {
            message_error('Debe al menos tener un item en su detalle de venta');
            return false;
        }

        vents.items.date = $('input[name="date"]').val();

        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('vents', JSON.stringify(vents.items));
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            location.href = '/supervisor/ventas/add';
        });
    });

    vents.list();

});