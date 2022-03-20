var TableController = function () {
    const init = function () {
        $("#ContentTable").DataTable({
            orderCellsTop: true,
            dom: "Blftipr",
            paging: false,
            buttons: ["excelHtml5", "print"],
            initComplete: function () {
                this.api().columns().every(function () {
                    var column = this;
                    var select = $('<select><option value=""></option></select>')
                        .appendTo($("#ContentTable thead tr:eq(1) th").eq(column.index()).empty())
                        .on("change",
                            function () {
                                const val = $.fn.dataTable.util.escapeRegex($(this).val());
                                column.search(val ? `^${val}$` : "", true, false).draw();
                            });
 
                    column.data().unique().sort().each(function (d, j) {
                        select.append(`<option value="${d}">${d}</option>`);
                    });
                });
            }
        });
    };
 
    return {
        init: init
    }
}();