$(document).ready(function () {
  initDeleteResource();
  // initQuillEditor();
  initTaskForm();
  toggleDisplayDiv();
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