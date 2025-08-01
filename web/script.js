
var currCountry;

const countrySearchButton = document.getElementById("search-button");
countrySearchButton.addEventListener('keyup', (event)=>{
    if(event.key == 'Enter'){
        var button = document.getElementById("country-value");
        currCountry = button.value;
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

            const variantElem = document.createElement("option");
            variantSelect.innerHTML = "";
            variantElem.textContent = "";
            variantSelect.append(variantElem);
            for(const variant of variantData['variants']){
                const variantElem = document.createElement("option");
                variantElem.textContent = variant;
                variantSelect.append(variantElem);
            }
            button.value = "";
        });

    }
});

const variantSelector = document.getElementById("variants");
variantSelector.addEventListener('change', function(){
    const currVariant = this.value;
    data = {country : currCountry, variant : currVariant};
    fetch("http://127.0.0.1:5000/get-day-stats", {
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
        .then(data =>{
            dateData = data['info']
            var dailyTable = document.getElementById("daily-table")
            for(const date of Object.keys(dateData)){
                const row = document.createElement("tr");

                const dateElem = document.createElement("td");
                dateElem.textContent = date;
                const infectionNum = document.createElement("td");
                infectionNum.textContent = dateData[date];
                row.append(dateElem);
                row.append(infectionNum)

                dailyTable.append(row);
            }
        });
});

