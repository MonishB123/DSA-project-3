const countrySearchButton = document.getElementById("search-button");

countrySearchButton.addEventListener('keyup', (event)=>{
    if(event.key == 'Enter'){
        var button = document.getElementById("country-value");
        const data = {
            country : button.value
        };
        fetch("http://127.0.0.1:5000/get-variants", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json; charset=UTF-8'
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            console.log(response);
            return response.json();
        })
        .then(variantData =>{
            var variantSelect = document.getElementById("variants");
            variantSelect.innerHTML = "";
            for(const variant of variantData['variants']){
                const variantElem = document.createElement("option");
                variantElem.textContent = variant;
                variantSelect.append(variantElem);
            }
            button.value = "";
        });

    }
});