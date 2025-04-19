async function cite(fileName) {
    try {
        const params = new URLSearchParams({ fileName });
        const apiUrl = `http://localhost:8000/cite?${params}`;
        return fetch(apiUrl)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Citation API error: ' + response.statusText);
                }
                return response.json();
            })
            .then(data => {
                return data;
            })
            .catch(error => {
                console.error('Error:', error);
                return error;
            }); 
    } catch (err) {
        console.error(err);
        alert('Error: ' + err.message);
    }
}

cite("DNA_extraction_and_qPCR_protocol_for_sensitive_detection_of_Trypanosoma_cruzi_in_blood_119293.txt").then(data => console.log(data["citation"]));