$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-question").modal("show");
      },
      success: function (data) {
        $("#modal-question .modal-content").html(data.html_code);
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#question-list div").html(data.html_code);  // <-- Replace the table body
          $("#modal-question").modal("hide");
        }
        else {
          $("#modal-question .modal-content").html(data.html_code);
        }
      }
    });
    return false;
  };


  /* Binding */

  // Create book
  $(".js-create-question").click(loadForm);
  $("#modal-question").on("submit", ".js-question-create-form", saveForm);

  // Update book
  $("#question-list").on("click", ".js-update-question", loadForm);
  $("#modal-question").on("submit", ".js-question-update-form", saveForm);

  // Delete book
  $("#question-list").on("click", ".js-delete-question", loadForm);
  $("#modal-question").on("submit", ".js-question-delete-form", saveForm);

});
