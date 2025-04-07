function handleOdRequest(odId, action) {
    console.log('Handling OD request:', odId, action);
    // Hide the row from the table
    document.getElementById('od-' + odId).style.display = 'none';

    // Send AJAX request to the server
    fetch("{% url 'process_od' 0 'approve' %}".replace("0", odId).replace("approve", action), {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify({ id: odId, action: action })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Request processed successfully');
        } else {
            console.error('Error processing request:', data.error);
        }
    })
    .catch(error => console.error('Error:', error));
}