Dropzone.autoDiscover = false;
$(document).ready(function() {
    $(".dropzone").dropzone({
      acceptedFiles: "image/*",
      maxFilesize: 1,
      url: "/upload",
      init: function() {
        this.on("success", function(file, response) {
          // $("#results").text("Face Embedding: " + response.embedding);
          // $("#results").text("Face Embedding: " + response);
          $('#results').empty()
          $.each(response, function (key, value) {
            // $('#results').append("<tr>\
            //       <td>"+value.name+"</td>\
            //       <td><img src=http://localhost:8000/static/images/" + value.filename + " width='150px' height='150px'></td>\
            //       <td>"+value.score+"</td>\
            //       </tr>");
            $('#results').append("<div class='row pb-2'>\
              <div class='col-md-4'>\
                <img src=static/movie_star/" + encodeURI(value.filename) + " width='150px' height='150px' alt='Image'>\
              </div>\
              <div class='col-md-8 flex-column'>\
                <div class='flex-grow-1'>\
                  <h4>" + value.name + "</h4>\
                </div>\
                <div class='flex-grow-1'>\
                  <p>Score:"+ value.score + "</p>\
                </div>\
              </div>\
            </div>")
          })
        });
        this.on("error", function(file, response) {
          console.log(response);
        });
      }
    });

    $("#search" ).click(function() {
        $('#spinner').show();
        $('#original').empty();
        $('#chatgpt').empty();
        question = $('input[name="question"]').val();
        type = $('input[name="type"]:checked').val();
        lang = $('input[name="lang"]:checked').val();
        enable_gpt = $("#enable_gpt").prop("checked")
        
        var params = {
          question: question,
          type: type,
          lang: lang,
          enable_gpt: enable_gpt
        };
        
        $.ajax({
          type: "POST",
          url: "/faq/search",
          data: JSON.stringify(params),
          dataType: "json",
          contentType : 'application/json; charset=utf-8', 
          success: function(response) {
            // console.log(response.original_answer);
            $('#spinner').hide();
            search_response = response.original_answer
            search_response = search_response.replace(/\n/g, "<br/>");
            $('#original').html(search_response);
            gpt_response = response.gpt_response 
            gpt_response = gpt_response.replace(/\n/g, "<br/>");
            $('#chatgpt').html(gpt_response);
          },
          error: function(xhr, status, error) {
            $('#spinner').hide();
            console.log("AJAX Error: " + status + " - " + error);
          }
        });
    });

    $("#movie_search" ).click(function() {
      $('#spinner').show();
      $('#movie_result').empty();
      // $('#chatgpt').empty();
      question = $('input[name="question"]').val();
      // type = $('input[name="type"]:checked').val();
      // lang = $('input[name="lang"]:checked').val();
      // enable_gpt = $("#enable_gpt").prop("checked")
      
      var params = {
        question: question
      };
      
      $.ajax({
        type: "POST",
        url: "/movie/search",
        data: JSON.stringify(params),
        dataType: "json",
        contentType : 'application/json; charset=utf-8', 
        success: function(response) {
          // console.log(response.original_answer);
          $('#spinner').hide();
          
          search_response = response.search_result
          // search_response = search_response.replace(/\n/g, "<br/>");
          $.each(response, function (key, value) {
            // $('#results').append("<tr>\
            //       <td>"+value.name+"</td>\
            //       <td><img src=http://localhost:8000/static/images/" + value.filename + " width='150px' height='150px'></td>\
            //       <td>"+value.score+"</td>\
            //       </tr>");
            $('#movie_result').append("<div class='row pb-2'>\
              <div class='col-md-8 flex-column'>\
                <div class='flex-grow-1'>\
                  <h4>" + value.title + "</h4>\
                </div>\
                <div class='flex-grow-1'>\
                  <p>"+ value.description + "</p>\
                </div>\
              </div>\
            </div>")
          })
          //$('#movie_result').html(search_response);
          // gpt_response = response.gpt_response 
          // gpt_response = gpt_response.replace(/\n/g, "<br/>");
          // $('#chatgpt').html(gpt_response);
        },
        error: function(xhr, status, error) {
          $('#spinner').hide();
          console.log("AJAX Error: " + status + " - " + error);
        }
      });
    });
    
    $("#pokemon_search" ).click(function() {
      query = $('input[name="query"]').val();
      var params = {
        query: query
      };
      
      $.ajax({
        type: "POST",
        url: "/pokemon/search",
        data: JSON.stringify(params),
        dataType: "json",
        contentType : 'application/json; charset=utf-8', 
        success: function(response) {
          search_response = response.search_result
          $('#results').empty()
          $.each(response, function (key, value) {
            $('#results').append("<div class='row pb-2'>\
              <div class='col-md-4'>\
                <img src=static/pokemon/" + value.filename + " width='150px' height='150px' alt='Image'>\
              </div>\
              <div class='col-md-8 flex-column pokemon_right'>\
                <div class='flex-grow-1'>\
                  <h4>" + value.name + "</h4>\
                </div>\
                <div class='flex-grow-1'>\
                  <p>Score:"+ value.score + "</p>\
                </div>\
              </div>\
            </div>")
          })
        },
        error: function(xhr, status, error) {
          console.log("AJAX Error: " + status + " - " + error);
        }
      });
    });

    $("#image_search" ).click(function() {
      query = $('input[name="query"]').val();
      var params = {
        query: query
      };
      
      $.ajax({
        type: "POST",
        url: "/food/search",
        data: JSON.stringify(params),
        dataType: "json",
        contentType : 'application/json; charset=utf-8', 
        success: function(response) {
          search_response = response.search_result
          $('#results').empty()
          $.each(response, function (key, value) {
            $('#results').append("<div class='row pb-2'>\
              <div class='col-md-4'>\
                <img src=static/food/" + encodeURI(value.filename) + " width='130px' height='73px' alt='Image'>\
              </div>\
              <div class='col-md-8 flex-column pokemon_right'>\
                <div class='flex-grow-1'>\
                  <h4>" + value.title + "</h4>\
                </div>\
              </div>\
            </div>")
          })
        },
        error: function(xhr, status, error) {
          console.log("AJAX Error: " + status + " - " + error);
        }
      });
    });
  });