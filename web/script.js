
var currCountry;

//Fetch countries for select element
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
        });

//fetch variants
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
            variantSelect.innerHTML = "";
            const emptyOption = document.createElement("option");
            emptyOption.textContent = "";
            variantSelect.append(emptyOption)
            for(const variant of variants){
                const variantElem = document.createElement("option");
                variantElem.textContent = variant;
                variantSelect.append(variantElem);
            }
        });
})

//Sort countries on button click
const sortButton = document.getElementById("sort-button");
sortButton.addEventListener('click', function(){
    fetch("http://127.0.0.1:5000/sort-countries", {
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
            countrySelector.innerHTML = "";
            countryList = data['countries'];
            const emptyOption = document.createElement("option");
            emptyOption.textContent = "";
            countrySelector.append(emptyOption)
            for(const country of countryList){
                const countryElem = document.createElement("option");
                countryElem.textContent = country;
                countrySelector.append(countryElem);
            }
            const prevPrefTable = document.getElementById("pref-table");
            if(prevPrefTable){
                prevPrefTable.remove();
            }

            const quickTime = data["quickTime"];
            const mergeTime = data["mergeTime"];
            const prefTable = document.createElement("table");
            prefTable.id = "pref-table"
            const infoElem = document.createElement("tr");
            const quickInfo = document.createElement("td");
            quickInfo.textContent = "Quick Sort Time (ns)";
            const mergeInfo = document.createElement("td");
            mergeInfo.textContent = "Merge Sort Time (ns)";
            infoElem.append(quickInfo);
            infoElem.append(mergeInfo);

            const timeElem = document.createElement("tr")
            const quickTimeElem = document.createElement("td"); 
            quickTimeElem.textContent = quickTime;
            const mergeTimeElem = document.createElement("td");
            mergeTimeElem.textContent = mergeTime;
            timeElem.append(quickTimeElem);
            timeElem.append(mergeTimeElem);

            prefTable.append(infoElem);
            prefTable.append(timeElem);
            const searchButton = document.getElementById("search-button");
            searchButton.append(prefTable);
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
            dateData = data["info"]
            var dailyTable = document.getElementById("daily-table")
            dailyTable.innerHTML = ""
            const infoElem = document.createElement("tr");
            const dateInfo = document.createElement("td");
            dateInfo.textContent = "Date";
            const infectionInfo = document.createElement("td");
            infectionInfo.textContent = "Total Infections";
            infoElem.append(dateInfo);
            infoElem.append(infectionInfo);
            dailyTable.append(infoElem);
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

            //Add plot
            const prevPlotImg = document.getElementById("graph");
            if (prevPlotImg){
                prevPlotImg.remove();
            }
            const plotImg = document.createElement("img")
            plotImg.id = "graph"
            plotImg.setAttribute("src", data["plot"])
            const countryState = document.getElementById("country-stats");
            countryState.append(plotImg);
        });
});

