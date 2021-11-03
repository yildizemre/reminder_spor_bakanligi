// pager--------------------


$(document).ready(function(){
  $('#data').after('<div id="nav"></div>');
  var rowsShown = 8;
  var rowsTotal = $('#data tbody tr').length;
  var numPages = rowsTotal/rowsShown;
  for(i = 0;i < numPages;i++) {
      var pageNum = i + 1;
      $('#nav').append('<a class="pagination-link" rel="'+i+'">'+pageNum+'</a> ');
  }
  $('#data tbody tr').hide();
  $('#data tbody tr').slice(0, rowsShown).show();
  $('#nav a:first').addClass('active');
  $('#nav a').bind('click', function(){

      $('#nav a').removeClass('active');
      $(this).addClass('active');
      var currPage = $(this).attr('rel');
      var startItem = currPage * rowsShown;
      var endItem = startItem + rowsShown;
      $('#data tbody tr').css('opacity','0.0').hide().slice(startItem, endItem).
      css('display','table-row').animate({opacity:1}, 300);
  });
});

//pager ---------------------

$("#myInput").keyup(function() {
  var searchTerm = $("#myInput").val();
  var bulunan = 0
  $('#myTable tr').each(function(e) {
      var table = $(this)
      if (table.text().toLowerCase().includes(searchTerm.toLowerCase())) {
          bulunan += 1
          table.show()
          $(".counter").text(bulunan + " kayıt bulundu")
      } else {
          table.hide()
          $(".counter").text(bulunan + " kayıt bulundu")
      }
  })
});

