$(document).ready(function() {

    $.fn.dataTable.moment(['DD/MM/YYYY', 'DD/MM/YYYY HH:mm']);

    var table = $('.records').DataTable({
        "colReorder": true,
        "scrollY": "520px",
        "scrollCollapse": true,
        "language": {
            "sEmptyTable": "Nenhum registro encontrado",
            "sInfo": "Mostrando de _START_ até _END_ de _TOTAL_ registros",
            "sInfoEmpty": "Mostrando 0 até 0 de 0 registros",
            "sInfoFiltered": "(Filtrados de _MAX_ registros)",
            "sInfoPostFix": "",
            "sInfoThousands": ".",
            "sLengthMenu": "_MENU_ resultados por página",
            "sLoadingRecords": "Carregando...",
            "sProcessing": "Processando...",
            "sZeroRecords": "Nenhum registro encontrado",
            "sSearch": "Pesquisar",
            "oPaginate": {
                "sNext": "Próximo",
                "sPrevious": "Anterior",
                "sFirst": "Primeiro",
                "sLast": "Último"
            },
            "oAria": {
                "sSortAscending": ": Ordenar colunas de forma ascendente",
                "sSortDescending": ": Ordenar colunas de forma descendente"
            },
            "select": {
                "rows": {
                    "_": "Selecionado %d linhas",
                    "0": "Nenhuma linha selecionada",
                    "1": "Selecionado 1 linha"
                }
            }
        },
        "dom": '<"top"f>rt<"bottom"Blp><"clear">i',
        "lengthMenu": [[25, 50, 100], [25, 50, 100]]
    });

    $('.dataTables_filter input').css('width', '400px'); // Defina a largura desejada

    // Evento para ajustar o tamanho do campo de pesquisa quando a janela é redimensionada
    $(window).resize(function() {
        $('.dataTables_filter input').css('width', '400px'); // Defina a largura desejada
    });

    $(window).resize(function() {
        table.columns.adjust().draw();
    });

    $(window).resize(function() {
        table.columns.adjust().draw();
      });
    
      // Display total records and rows
      var info = table.page.info();
      $('#totalRecords').text('Total Records: ' + info.recordsTotal);
      $('#totalRows').text('Total Rows: ' + info.recordsDisplay); 
    
      // Add the information display elements (adjust IDs as needed)
      $('div.bottom').append(
        '<div id="totalRecords"></div>' + 
        '<div id="totalRows"></div>'
      );
    
      $('.paginate_button').css('outline', 'none');

    $('.paginate_button').css('outline', 'none');
});


function toggleSelectAll(selectAllCheckbox) {
    const checkboxes = document.querySelectorAll('.selectItem');
    checkboxes.forEach(checkbox => {
        checkbox.checked = selectAllCheckbox.checked;
    });
    toggleBulkDeleteButton(); 
}

function toggleBulkDeleteButton() {
    const checkboxes = document.querySelectorAll('.selectItem');
    const bulkDeleteButton = document.getElementById('bulkDeleteButton');
    const anyChecked = Array.from(checkboxes).some(checkbox => checkbox.checked);
    bulkDeleteButton.style.display = anyChecked ? 'inline-block' : 'none';
}

function showConfirmationModalForSelected() {
    $('#confirmationModal').modal('show');

    // Ao clicar em "Excluir" no modal, enviar o formulário
    $('#confirmDeleteButton').off('click').on('click', function() {
        document.getElementById('deleteForm').submit();
    });
}