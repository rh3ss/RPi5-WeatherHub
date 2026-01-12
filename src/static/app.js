let currentScreen = 0;
let chart;
const city = window.APP_CONFIG.city;
const refreshTime = window.APP_CONFIG.refresh_time;

function goScreen(i){
    currentScreen = i;
    localStorage.setItem("screen", i);
    document.getElementById("wrap").style.transform = `translateX(-${i * 100}vw)`;
    if(i === 1) loadDHT();
}

function updateDateTime(){
    const now = new Date();
    const time = now.toLocaleTimeString("de-DE",{hour:"2-digit",minute:"2-digit"});
    const weekday = now.toLocaleDateString("de-DE",{weekday:"long"});
    document.getElementById("locationLine").textContent = `${city}, ${time} ${weekday}`;
}
setInterval(updateDateTime, 1000 * 1);
updateDateTime();

function moveSun(sunrise, sunset){
    if(!sunrise || !sunset) return;
    const now = Date.now() / 1000;
    let position = (now - sunrise) / (sunset - sunrise);
    position = Math.max(0, Math.min(1, position));

    const path = document.getElementById("sunCurve");
    const point = path.getPointAtLength(position * path.getTotalLength());

    sunDot.style.left = point.x + "px";
    sunDot.style.top  = point.y + "px";
}

async function loadWeather(){
    const data = await (await fetch("/api/weather")).json();
    const now = Date.now() / 1000;
	const startIndex = data.hourly.findIndex(h => h.dt > now);
	const list = data.hourly.slice(startIndex, startIndex + 8);
    const cur = list[0];

    curTemp.textContent = Math.round(cur.temp)+"°";
    weather_desc.textContent = cur.desc;
    temp_min.textContent = Math.round(Math.min(...list.map(i=>i.temp)))+"°";
    temp_max.textContent = Math.round(Math.max(...list.map(i=>i.temp)))+"°";
    feels_like.textContent = Math.round(cur.feels_like)+"°";
    humidity.textContent = cur.humidity+"%";
    wind.textContent = Math.round(cur.wind_speed_kmh);

    sunrise.textContent = new Date(data.sunrise * 1000).toLocaleTimeString("de-DE",{hour:"2-digit",minute:"2-digit"});
    sunset.textContent = new Date(data.sunset * 1000).toLocaleTimeString("de-DE",{hour:"2-digit",minute:"2-digit"});

    moveSun(data.sunrise,data.sunset);
    
    hourContainer.innerHTML = list.map(it=>`
        <div class="hour-item">
        <div>${new Date(it.dt*1000).toLocaleTimeString("de-DE",{hour:"2-digit"})}</div>
        <div class="hour-icon"><img src="https://openweathermap.org/img/wn/${it.icon}.png"></div>
        <div class="hour-temp">${Math.round(it.temp)}°</div>
        <div class="hour-pop">☔ ${Math.round(it.pop*100)}%</div>
        </div>`).join("");
}
loadWeather();
setInterval(()=>{
    if(currentScreen === 0){
        loadWeather();
    }
},1000 * 60 * refreshTime);

async function loadDHT(){
    const d = await (await fetch("/db/data")).json();
    const ventilatedPoints = d.humidity.map((h,i) =>
		d.ventilated[i] === 1 ? h + 5 : NaN
	);

    avgTemp.textContent = d.avg_temp;
    avgHum.textContent = d.avg_hum;

    if(chart){
        chart.data.labels = d.labels;
        chart.data.datasets[0].data = d.temperature;
        chart.data.datasets[1].data = d.humidity;
        chart.data.datasets[2].data = ventilatedPoints;
        chart.update();
        return;
    }

    chart = new Chart(dhtChart,{
        type:"line",
        data:{
            labels:d.labels,
            datasets:[
                {data:d.temperature,borderColor:"#ffdb4d",yAxisID:"t"},
                {data:d.humidity,borderColor:"#7fd6ff",yAxisID:"h"},
                {data:ventilatedPoints,showLine:false,pointRadius:7,pointBackgroundColor:"#ff0000",yAxisID:"h"}
            ]
        },
        options:{
            plugins:{legend:{display:false}},
            scales:{
                t:{position:"left"},
                h:{position:"right",grid:{drawOnChartArea:false}}
            }
        }
    });
}
setInterval(()=>{
    if(currentScreen === 1){
        loadDHT();
    }
},1000 * 60 * refreshTime);

const savedScreen = localStorage.getItem("screen");
if(savedScreen !== null){
    goScreen(parseInt(savedScreen));
}
