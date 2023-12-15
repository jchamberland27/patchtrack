document.addEventListener('DOMContentLoaded', function () {
    updatePatchTableBody();
    updatePortCount();
    
    setInterval(updatePatchTableBody, 5000);
});

function addConnection() {
    // Read values from form fields
    var portNumber = document.getElementById('portNumber').value;
    var connectedTo = document.getElementById('connectedTo').value;

    // Update the table (modify as needed)
    // For example, update the first row with the new values
    //document.getElementById('port1').innerText = portNumber;
    //document.getElementById('connectedTo1').innerText = connectedTo;

    // Make an API call to update the server-side database
    // You can use fetch or another method to make the API call
    // Example using fetch:
    fetch('/patch/'+portNumber+'/set?value='+encodeURIComponent(connectedTo), {
        method: 'GET'})
    .then(data => {
        // Handle the API response if needed
        console.log('API Response:', data);
    })
    .catch(error => {
        console.error('Error:', error);
    });

    // Close the modal
    $('#addModal').modal('hide');
}

function updatePatchTableBody() {
    // Make a GET request to the Flask API endpoint
    fetch('/ui/patch_table')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.text();
        })
        .then(data => {
            document.getElementById('patchTableBody').innerHTML = data;
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function updatePortCount() {
    fetch('/config/patch_ports/get')
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.text();
    })
    .then(data => {
        //add an option element with the value and text for 1 through data
        var select = document.getElementById('portNumber');
        select.innerHTML = '';
        for (var i = 1; i <= data; i++) {
            var opt = document.createElement('option');
            opt.value = i;
            opt.innerHTML = i;
            select.appendChild(opt);
        }
    })
}