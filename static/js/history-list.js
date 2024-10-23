async function fetchSongs() {
    await fetch('/recent_songs_data')
        .then(response => response.json())
        .then(data => {
            const songList = document.getElementById('song-list');
            songList.innerHTML = '';

            let h = document.createElement("div");
            //h.className = "indicator"
            h.style = "grid-column: span 3; height: 50px"
            songList.appendChild(h);

            let toggle = document.createElement("div");
            toggle.className = "indicator";
            toggle.style = "height: 50px";
            console.log(stat)
            toggle.innerHTML = `
                    <div class="status-radio-buttons" style="width: 66%">
                        <label class="radio-button-container ignored">
                            <input type="radio" name="toggle" value="3" ${stat === 3 ? 'checked' : ''} onClick="updateStatus(3)">
                            <span class="text"><i class="fa-solid fa-circle-stop"></i></span>
                        </label>
                        <label class="radio-button-container no-whistle">
                            <input type="radio" name="toggle" value="2" ${stat === 2 ? 'checked' : ''} onClick="updateStatus(2)">
                            <span class="text"><i class="fa-solid fa-circle-xmark"></i></span>
                        </label>
                    </div>`;
            songList.appendChild(toggle);

            data.forEach(song => {
                const dateObj = new Date(song['timestamp']);
                const timeOnly = dateObj.toLocaleTimeString([], { 
                    hour: '2-digit', 
                    minute: '2-digit'
                  });

                let t = document.createElement("div");
                t.className = "indicator"
                t.style = "height: 50px; display: flex; justify-content: center";
                t.innerHTML = `<p class='song-text'>${timeOnly}</p>`
                songList.appendChild(t);

                let s = document.createElement("div");
                s.className = "indicator"
                s.style = "height: 50px"
                s.innerHTML = `<p class='song-text'>${song['title']} by ${song['artist']}</p>`
                songList.appendChild(s);

                let p = document.createElement("div");
                p.className = "indicator"
                if (song['in_ultimate_playlist'] === true) {
                    p.className = "indicator ultimate"
                    p.innerText = "ULTIMATE"
                } else if (song['in_normal_playlist'] === true) {
                    p.className = "indicator standard"
                    p.innerText = "VIBES"
                }
                
                p.style = "height: 50px"
                songList.appendChild(p);

                let sta = document.createElement("div");
                sta.className = "indicator"
                sta.style = "height: 50px";
                sta.innerHTML = `
                    <div class="status-radio-buttons">
                        <label class="radio-button-container ignored">
                            <input type="radio" name="status-${song['statistics_id']}" value="3" ${song['status_name'] == 'ignore' ? 'checked' : ''} onClick="updateWhistle(${song['statistics_id']}, 3)">
                            <span class="text"><i class="fa-solid fa-circle-stop"></i></span>
                        </label>
                        <label class="radio-button-container no-whistle">
                            <input type="radio" name="status-${song['statistics_id']}" value="2" ${song['status_name'] == 'no-whistle' ? 'checked' : ''} onClick="updateWhistle(${song['statistics_id']}, 2)">
                            <span class="text"><i class="fa-solid fa-circle-xmark"></i></span>
                        </label>
                        <label class="radio-button-container whistle">
                            <input type="radio" name="status-${song['statistics_id']}" value="1" ${song['status_name'] == 'whistle' ? 'checked' : ''} onClick="updateWhistle(${song['statistics_id']}, 1)">
                            <span class="text"><i class="fa-solid fa-circle-check"></i></span>
                        </label>
                    </div>`;
            songList.appendChild(sta);
            });
        })
        .catch(error => console.error('Error fetching song data:', error));
}

let stat = 2
async function fetchStatus() {
    await fetch('/get_status')
    .then(response => response.json())
    .then(data => {
        stat = data.status
    })
    .catch(error => console.error('Error fetching song data:', error));
}

async function updateSongListAndStatus() {
    await fetchStatus();
    await fetchSongs();
}
setInterval(updateSongListAndStatus, 5000);
updateSongListAndStatus();

function updateStatus(newStat) {
    fetch('/change_status', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ value: newStat })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Response:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

function updateWhistle(statisticId, status) {
    fetch('/change_statistic', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
             statistic_id: statisticId,
             status: status
            })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Response:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
