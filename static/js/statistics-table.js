$(document).ready(function() {
    $('#statisticsTable').DataTable({
        paging: true,
        searching: true,
        order: [[7, 'desc']],
        drawCallback: function() {
            var api = this.api();

            var intVal = function(i) {
                return typeof i === 'string' ?
                    i.replace(/[\$,]/g, '')*1 :
                    typeof i === 'number' ?
                    i : 0;
            };

            var totalWhistle = api
                .column(2)
                .data()
                .reduce(function(a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            var totalActive = api
                .column(3)
                .data()
                .reduce(function(a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            var totalTotal = api
                .column(4)
                .data()
                .reduce(function(a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            var pageTotalWhistle = api
                .column(2, { page: 'current' })
                .data()
                .reduce(function(a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            var pageTotalActive = api
                .column(3, { page: 'current' })
                .data()
                .reduce(function(a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            var pageTotalTotal = api
                .column(4, { page: 'current' })
                .data()
                .reduce(function(a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            $('#totalWhistle').html(totalWhistle + ' (' + pageTotalWhistle + ')');
            $('#totalActive').html(totalActive + ' (' + pageTotalActive + ')');
            $('#totalTotal').html(totalTotal + ' (' + pageTotalTotal + ')');
        }
    });
});