  $(document).ready(function() {
    $('.delete-resource').on('click', function(event) {
        console.log("Link was clicked!");
        event.preventDefault();
        const url = $(this).data('url');  // get URL from data-url attribute
        $.ajax({
            url: url,
            type: 'DELETE',
            success: function() {
                location.reload();
            },
            error: function(err) {
                console.error("AJAX request failed:", err);
            }
        });
    });
});


  function submitForm(event, resourceURL) {
    event.preventDefault();

    let formData = {};
    $.each($(event.target).serializeArray(), function(i, field) {
      formData[field.name] = field.value;
    });

    $.ajax({
      url: resourceURL,
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify(formData),
      success: function() {
        console.log("Data sent successfully");
      },
      error: function() {
        console.log("Error in sending data");
      }
    });
  }

//   TASKS
  $("#trunk-content-form").on("submit", function(event) {
    submitForm(event, "{{ url_for('task_api.create_trunk_content') }}");
  });

var quill = new Quill('#quill-editor', {
    theme: 'snow'
});

// Update the hidden input whenever the Quill editor changes
quill.on('text-change', function() {
    document.getElementById('content').value = quill.root.innerHTML;
});


  