var requestSent = false;
var currentRequest = null;

$(document).ready(function () {
  searchName = document.getElementById("searchName");
  searchDate = document.getElementById("searchDate");
  streets = document.getElementById("streets");
  // countStreets = document.getElementById("countStreets")

  districtSelect = document.getElementById("districtSelect");
  typeSelect = document.getElementById("typeSelect");

  if(!requestSent) {
      requestSent = true;
      function search_street() {
    currentRequest = $.ajax({
            type: 'GET',
            async: true,
            url: "search_ajax/",
            beforeSend : function()    {
                if(currentRequest != null) {
                  currentRequest.abort();
                }
              },
            data:  {
              'searchDate': searchDate.value,
              'searchName': searchName.value,
              'district': districtSelect.value,
              'type': typeSelect.value,
            },
            success: function(data) {
              createTable(data);
              // countStreets.innerHTML = data.street_list.length
              requestSent = false;
            },
            dataType: 'json',
        });
    }
    }
    search_street();

  $('#searchName').keyup(function(){
    search_street();
  });

  $('#searchDate').keyup(function(){
    search_street();
  });

  $('#districtSelect').change(function(){
    search_street();
  });

  $('#typeSelect').change(function(){
    search_street();
  });


  function createTable(data) {
  //   table = `
  //   <thead >
  //    <tr class="w3-teal" >
  //      <th>Номер у б/д</th>
  //      <th>Назва вулиці</th>
  //      <th>Тип вулиці</th>
  //      <th>Кількість сегментів</th>
  //    </tr>
  //  </thead>
  //   `
    table = `
    <thead >
     <tr class="w3-teal" >
       <th>Вулиця</th>
       <th>Кількість сегментів</th>
     </tr>
   </thead>
    `
    var i = 0;
    while(i < data.street_list.length && i < 100) {
      // table += `
      // <tr>
      //   <td>${data.street_list[i][0]}</td>
      //   <td><a href="/${data.street_list[i][0]}/">${data.street_list[i][1]}</a></td>
      //   <td>${data.street_list[i][2]}</td>
      //   <td>${data.count_of_segments[i]}</td>
      // </tr>
      // `
      // i++;
      table += `
      <tr>
        <td><a href="/${data.street_list[i][0]}/">${data.street_list[i][2]} ${data.street_list[i][1]}</a></td>
        <td>${data.count_of_segments[i]}</td>
      </tr>
      `
      i++;
    }

          streets.innerHTML = table;
  }
    });
