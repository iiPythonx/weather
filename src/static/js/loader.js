// Copyright 2023 iiPython

// Initialization
const datapointEntries = [
    { k: "temp", n: "Temperature", s: "°" },
    { k: "pressure", n: "Air Pressure", s: "hPa" },
    { k: "humidity", n: "Humidity", s: "%" },
    { k: "wspeed", n: "Wind Speed", s: "mph" }
];

// Chart.js setup
window._lastChart = null;
window._lastData = null;
function setGraphFocus(key) {
    if (window._lastChart === null) return;
    let config = window._lastChart.config
        suffix = datapointEntries.find(i => i.k === key).s;
    config.data.labels = window._lastData.times;
    config.data.datasets = [ window._lastData[key] ];
    config.options.scales.y.ticks = { callback: (v, i, t) => { return v + suffix} }
    config.options.plugins = {
        tooltip: { callbacks: { label: (t, d) => { return t.formattedValue + suffix } } }
    }
    window._lastChart.update();
}
function renderData(date, desc, data) {

    // Process data
    window._lastData = data
    $("p#forecast-description").text(desc);

    // Handle chart updating (or creation)
    if (window._lastChart === null) {
        window._lastChart = new Chart($("#graph"), {
            type: "line",
            data: { labels: data.times, datasets: [] },
            options: { scales: { y: { beginAtZero: true } } }
        });
    }
    setGraphFocus("temp");

    // Flush info to table
    for (let dp of datapointEntries) {
        let items = data[dp.k].data;
        let parent = $(`tr[data-key='${dp.k}']`)
            current = `${items[items.length - 1]}${dp.s}`
            average = `${Math.round(items.reduce((ps, a) => ps + a, 0) / items.length, 2)}${dp.s}`;

        // Update all existing information
        if (!parent[0]) {
            $("#current-tb").append(`<tr data-key="${dp.k}">
                <th class="info-key">${dp.n}</th>
                <th>${current}</th>
                <th>${average}</th>
            </tr>`);

            // Create click handler
            $("#current-tb tr:last").find(".info-key").on("click", () => { setGraphFocus(dp.k) });
        } else {
            parent.children()[1].innerText = current;
            parent.children()[2].innerText = average;
        }
    }
    $("p.header").text(date.replace(/\-/g, "/") + " UTC");
}

// Handle tabs
const showInfoTab = () => {
    $("#info-frame").css("display", "flow-root");
    $("#historical-frame").css("display", "none");
}
const showHistTab = () => {
    $("#info-frame").css("display", "none");
    $("#historical-frame").css("display", "flow-root");
}
$("#info-btn").on("click", showInfoTab);
$("#historical-btn").on("click", showHistTab);

// Load data
function handleCallback(d) {

    // Parse API response into a Chart.js friendly format
    let parsed = { times: [] }
    for (let entry of d.data) {
        for (let dp of datapointEntries) {
            if (!(dp.k in parsed)) parsed[dp.k] = {
                label: dp.n, data: [], borderWidth: 1
            };
            parsed[dp.k].data.push(entry[dp.k]);
        }
        parsed.times.push(entry.time);
    }
    renderData(
        d.date, // To render on top of box
        d.data[0].desc,  // Basic forecast description
        parsed  // Actual data
    );
}
$.get("/api/today", {}, handleCallback);

// Populate the historical data list
$.get("/api/dates", {}, (d) => {
    for (let date of d.data) {
        let obj = $("#historical-frame").find("ul").append(`<li><a>${date}</a></li>`);
        $(obj.children().last()).on("click", () => {
            $.get(`/api/past/${date}`, {}, handleCallback);
            showInfoTab();
        });
    }
});
