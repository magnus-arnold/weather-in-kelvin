
update = function(data) {

    let div = document.getElementById('weather-div');
    div.innerHTML = `\
      <div class="left-div"> \
        <div class="weather-city"> ${data.name}</div> \
        <div class="weather-text">${data.weather[0].description}</div> \
        <div class="weather-cur-temp">${data.main.temp} K</div> \
        <div class="weather-feels-like">Feels like ${data.main.feels_like} K</div> \
      </div> \
      <div class="right-div"> \
        <div class="weather-min-temp">Minimum temperature ${data.main.temp_min} K</div> \
        <div class="weather-max-temp">Maximum temperature ${data.main.temp_max} K</div> \
        <div class="weather-humidity">Humidity ${data.main.humidity} %</div> \
        <div class="weather-pressure">Barometric pressure ${data.main.pressure} hPa</div> \
      </div> \
      `;
}

lookup = function() {
    // Show waiting spinner.
    let div = document.getElementById('weather-div');
    div.innerHTML = `<div class="waiting">Searching ...</div>`;

    // First dig the location out of the input widget.
    const input = document.getElementById('city-input');

    // Request weather data.
    fetch('/weather/' + input.value)
        .then((response) => {
            if (!response.ok) {
                throw new Error(`HTTP error: ${response.status}`);
            }
            return response.json();
        })
        .then((json) => update(json))
        .catch((err) => {
            div.innerHTML = `<div class="error">Error: unable to find weather for location '${input.value}'</div>`;
            console.error(`Fetch problem: ${err.message}`);
        });
}

init = function() {

    // Trap 'Enter' keypress in search bar.
    let input = document.getElementById('city-input');
    input.addEventListener("keyup", (event) => {
        if (event.key === 'Enter') {
            lookup();
        }
    })
}
