
var currCountry;

//Fetch Countries
const countrySelector = document.getElementById("country");
fetch("http://127.0.0.1:5000/get-countries", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json; charset=UTF-8'
            },
            body: JSON.stringify()
        })
        .then(response => {
            console.log(response);
            return response.json();
        })
        .then(data =>{
            countryList = data['countries'];
            
            for(const country of countryList){
                const countryElem = document.createElement("option");
                countryElem.textContent = country;
                countrySelector.append(countryElem);
            }
            //Add sorting button
            const sortButton = document.createElement("button");
            sortButton.textContent = "Sort Countries by Total Growth";
            sortButton.id = "sort-button";
            const selectArea = document.getElementById("search-button");
            selectArea.append(sortButton);
        });

countrySelector.addEventListener('change', function(){
    currCountry = this.value;
    data = {country : currCountry};
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
        .then(data =>{
            variants = data['variants']
            var variantSelect = document.getElementById("variants")
            for(const variant of variants){
                const variantElem = document.createElement("option");
                variantElem.textContent = variant;
                variantSelect.append(variantElem);
            }
        });
})

//Fetch date data given country and variant
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

