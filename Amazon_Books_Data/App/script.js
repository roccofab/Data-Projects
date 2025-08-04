//This function is called when the users click on the button(id: "butt")
document.getElementById('butt').onclick = function() {
    //Retrieve the input asin code from the input type field
    const asin = document.getElementById('asinInp').value;

    const spinner = document.getElementById('spinner');
    const resultDiv = document.getElementById('result'); //select the container where to show response result
    spinner.style.display = 'block';
    resultDiv.innerHTML = '';

    //Make a GET request to the Flask server endpoint passing the ASIN code
    fetch(`/recommend?asin=${asin}`)
    //cast server response to json
        .then(response => {
        console.log("Raw response:", response);  // 👈 Debug della risposta
        return response.json(); // tenta di convertirla in JSON
        })
        .then(data => {
            console.log("Parsed JSON:", data);
            spinner.style.display = 'none';  //hide the spinner
            //if the response is not empty show an html list containing the books reccomandations details into the container(id: "result")
            if (data.recommendation) {
                let html = '<h3>Recommended Books:</h3><ul>';
                data.recommendation.forEach(book => {
                    html += `<li>
                              <strong><a href="https://www.amazon.com/dp/${book.asin}" target="_blank">${book.title}</a></strong><br> 
                              Price: ${book.final_price}<br>
                              Rating: ${book.rating}<br>
                              Reviews: ${book.reviews_count}<br>
                              Category: ${book.main_category}</li><br>`;
                });
                html += '</ul>';
                resultDiv.innerHTML = html;
                //if the response contains an error(e.g. ASIN not found) show the message error
            } else if (data.error) {
                resultDiv.innerText = data.error;
            }
        })
        .catch(err => {
            spinner.style.display = 'none';
            console.error("Fetch error:", err);
            document.getElementById('result').innerText = 'Error Request';
        });
};