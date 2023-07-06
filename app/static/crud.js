$(document).ready(function () {
  initResizable();
  // initDataTables();
  initDeleteResource();
  initTaskForm();
  // toggleDisplayDiv();
  objectives_search();
  toggleForm();
  toggleContent();
  trunk_content_search();
});

function initResizable() {
  $(function () {
    $(".table").colResizable();
  });
}

// function initDataTables() {
//   $(document).ready(function () {
//     $('.table').DataTable();
//   });
// }

function initDeleteResource() {
  $('.delete-resource').on('click', function (event) {
    console.log("Link was clicked!");
    event.preventDefault();
    const url = $(this).data('url');
    $.ajax({
      url: url,
      type: 'DELETE',
      success: function () {
        location.reload();
      },
      error: function (err) {
        console.error("AJAX request failed:", err);
      }
    });
  });
}

function toggleForm() {
  $(document).ready(function () {
    $('#openTaskFormButton').click(function () {
      $('#taskFormModal').modal('show');
    });
  });
}

function initQuillEditor() {
  const quill = new Quill('#quill-editor', { theme: 'snow' });

  quill.on('text-change', function () {
    document.getElementById('content').value = quill.root.innerHTML;
  });

  return quill;
}

function initTaskForm() {
  const quill = initQuillEditor();

  $("#submitForm").on("click", function () {
    const actionUrl = $('#task-form').data('action-url');
    submitForm($('#task-form'), actionUrl);
  });

  $("#clearForm").on("click", function () {
    $("#task-form").trigger('reset');
  });
}

function submitForm(form, resourceURL) {
  const formData = new FormData(form[0]);

  fetch(resourceURL, {
    method: 'POST',
    body: formData
  })
    .then(response => {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error('Network response was not ok.');
      }
    })
    .then(data => {
      console.log("Data sent successfully");
      showAlert('success', 'Task created successfully!');
      $('#taskFormModal').modal('hide');
    })
    .catch(error => {
      console.log("Error in sending data", error);
      showAlert('danger', 'Failed to create task. Please try again.');
    });
}


function showAlert(type, message) {
  const alert = `<div class="alert alert-${type} alert-dismissible fade show" role="alert">
    ${message}
    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
      <span aria-hidden="true">&times;</span>
    </button>
  </div>`;

  // Get the alert container and add the alert to it
  const alertContainer = document.getElementById('alert-container');
  alertContainer.insertAdjacentHTML('beforeend', alert);
}

function toggleDisplayDiv() {
  $(document).ready(function () {
    $('.toggle-button').click(function () {
      $(this).next('.display-div').toggle();
      console.log('algo');
    });
  });
}

function toggleContent() {
  $(document).ready(function () {
    $('.toggle-button').click(function () {
      var taskId = $(this).data('task-id');
      var content = $(this).next('#contentModal' + taskId + ' .modal-body').html();
      $('#contentModal' + taskId + ' .modal-body').html(content);
      $('#contentModal' + taskId).modal('show');
    });
  });
}


function objectives_search() {
  $(document).ready(function () {
    var url = $('#objectives').data('url');  // Get URL from data-url attribute

    $('#objectives').select2({
      width: '100%',
      tags: true,
      tokenSeparators: [','],
      ajax: {
        url: url,
        dataType: 'json',
        delay: 250,
        data: function (params) {
          return {
            q: params.term
          };
        },
        processResults: function (data) {
          return {
            results: data.objectives.map(function (objective) {
              return { id: objective.name, text: objective.name };
            })
          };
        },
        cache: true
      },
      minimumInputLength: 1,
    });
  });
}


function trunk_content_search() {
  $(document).ready(function () {
    var url = $('#trunk_contents').data('url');  // Get URL from data-url attribute

    $('#trunk_contents').select2({
      width: '100%',
      tags: true,
      tokenSeparators: [','],
      ajax: {
        url: url,
        dataType: 'json',
        delay: 250,
        data: function (params) {
          return {
            q: params.term
          };
        },
        processResults: function (data) {
          return {
            results: data.trunk_contents.map(function (trunk_content) {
              return { id: trunk_content.name, text: trunk_content.name };
            })
          };
        },
        cache: true
      },
      minimumInputLength: 1,
    });
  });
}
