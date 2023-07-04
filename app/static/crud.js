$(document).ready(function () {
  initDeleteResource();
  initTaskForm();
  toggleDisplayDiv();
  objectives_search();
  trunk_content_search();
});

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

function initQuillEditor() {
  const quill = new Quill('#quill-editor', { theme: 'snow' });

  quill.on('text-change', function () {
    document.getElementById('content').value = quill.root.innerHTML;
  });

  return quill;
}

function initTaskForm() {
  const quill = initQuillEditor();

  $("#task-form").on("submit", function (event) {
    const actionUrl = $(this).data('action-url');
    submitForm(event, actionUrl);
  });
}

function submitForm(event, resourceURL) {
  event.preventDefault();

  const formData = new FormData(event.target);

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
              return { id: trunk_content.id, text: trunk_content.name };
            })
          };
        },
        cache: true
      },
      minimumInputLength: 1,
    });
  });
}
