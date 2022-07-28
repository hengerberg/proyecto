var tblProducts;
var vents = {
    items: {
        date: '',
        cant: 0,
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
            // input del form comision
            if (dict.pay_commission === true){ // si el vendedor puede cobrar su comision de la venta
                dict.commission_paid = dict.cant * parseFloat(dict.seller_commission); // calculamos la comision por la cantidad vendida
                commission_paid += dict.commission_paid; // agregamos al diccionario el valor de la comision pagada
                dict.commission_receivable = 0.00;
                commission_receivable += dict.commission_receivable; // agregamos tambien la comision por cobrar igual a 0 para que no de error
            }else{
                dict.commission_receivable = dict.cant * parseFloat(dict.seller_commission);
                commission_receivable += dict.commission_receivable;
                dict.commission_paid = 0.00;
                commission_paid += dict.commission_paid;
            }
        });
        $.each(this.items.products, function (pos, dict) {
            // imput del form subtotal
            if (dict.pay_commission === true) {
                dict.subtotal = dict.cant * parseFloat(dict.price_in);
                subtotal += dict.subtotal;
            } else {
                if (parseFloat(dict.price_in) === 0){
                    dict.subtotal = 0;
                    subtotal += dict.subtotal;
                }else{
                    dict.subtotal = dict.cant * (parseFloat(dict.price_in) + parseFloat(dict.seller_commission));
                    subtotal += dict.subtotal;
                }
            }
        });
        this.items.subtotal = subtotal;
        this.items.commission_paid = commission_paid;
        this.items.commission_receivable = commission_receivable;
        this.items.discount = discount
        this.items.total = this.items.subtotal - this.items.discount;

        $('input[name="subtotal"]').val(this.items.subtotal.toFixed(2));
        $('input[name="commission_paid"]').val(this.items.commission_paid.toFixed(2));
        $('input[name="commission_receivable"]').val(this.items.commission_receivable.toFixed(2));
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
                { "data": "name" },
                { "data": "cant" },
                { "data": "price_in" },
                { "data": "seller_commission" },
                { "data": "subtotal" },
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    }
                },
                {
                    targets: [-4],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="cant" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.cant + '">';
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
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
            rowCallback(row, data, displayNum, displayIndex, dataIndex) { // permite devolver el tr de la tabla
                $(row).find('input[name="cant"]').TouchSpin({ // con jquery, busca el componente llamado cant y agregale el touchspin
                    min: 1,
                    max: 50,
                    step: 1,

                });
            },
            initComplete: function (settings, json) {

            }
        });
        console.clear();
        //console.log(this.items);
        //console.log(this.get_ids());
    },
};
$(function () {

    $('input[name="search"]').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_products',
                    'term': request.term,
                    'ids': JSON.stringify(vents.get_ids()) // enviamos los ids a la vista los datos de los productos agregados
                },
                dataType: "json",
            }).done(function (data) {
                response(data);
            }).fail(function (jqXHR, textStatus, errorThrown) {
                //alert(textStatus + ": " + errorThrown);
            }).always(function (data) {

            });
        },
        delay: 200,
        minLength: 0,
        select: function (event, ui) {
            event.preventDefault();
            console.clear();
            ui.item.cant = 1;
            ui.item.subtotal = 0.00;
            //console.log(vents.items);

            vents.add(ui.item);

            $(this).val('');
        }
    });

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

    $('.btnRemoveAll').on('click', function () {
        vents.items.products = [];
        vents.list();
    })
    // event eliminar
    $('#tblProducts tbody')
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            vents.items.products.splice(tr.row, 1);
            vents.list();
        }) // event cantidad
        .on('change', 'input[name="cant"]', function () {
            console.clear(); // limpio la consola
            var cant = parseInt($(this).val()); // guardo en la variable cant lo que tenga el input
            // console.log(cant);
            var tr = tblProducts.cell($(this).closest('td, li')).index(); // obtenemos el indice el array que esta el producto
            //console.log(tr)
            vents.items.products[tr.row].cant = cant; // modifico la variable de cantidad del producto asignandole cant
            vents.calculate_report();
            $('td:eq(5)', tblProducts.row(tr.row).node()).html('$' + vents.items.products[tr.row].subtotal.toFixed(2));
        });

    $('.btnClearSearch').on('click', function () {
        $('input[name="search"]').val('').focus();
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
            location.href = '/vendedor/reporte/list';
        });
    });

    vents.list();

});