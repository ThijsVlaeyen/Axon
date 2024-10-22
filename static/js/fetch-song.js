const colorThief = new ColorThief();
const socket = io();
let cur_song = "";

socket.on('song_update', function(data) {
    updateAll(data)
});

function fetchCurrentSong() {
    fetch('/current_song')
        .then(response => response.json())
        .then(data => {
            updateAll(data)
        })
        .catch(error => console.error('Error fetching current song:', error));
}
setInterval(fetchCurrentSong, 5000);

function updateAll(data) {
    if (cur_song != data.current_song_uri) {
        updateIndicator(data.normal, 'normal-playlist-indicator')
        updateIndicator(data.ultimate, 'ultimate-playlist-indicator')
        
        try {
            document.getElementById('played-count').innerHTML = data.played_count
            
            document.getElementById('normal-size').innerHTML = data.normal_length
            if (data.normal_id !== 'undefined' && data.normal_id !== null && data.normal_id !== '') {
                const normalEmbed = `<iframe src="https://open.spotify.com/embed/playlist/${data.normal_id}" 
                width="100%" height="190" frameborder="0" allowtransparency="true" allow="encrypted-media">
                </iframe>`;
                document.getElementById('normal-embed').innerHTML = normalEmbed;
            }
            
            document.getElementById('ultimate-size').innerHTML = data.ultimate_length
            if (data.ultimate_id !== 'undefined' && data.ultimate_id !== null && data.ultimate_id !== '') {
                const ultimateEmbed = `<iframe src="https://open.spotify.com/embed/playlist/${data.ultimate_id}" 
                width="100%" height="190" frameborder="0" allowtransparency="true" allow="encrypted-media">
                </iframe>`;
                document.getElementById('ultimate-embed').innerHTML = ultimateEmbed;
            }
        } catch(e) {}
        
        updateSpotifyEmbed(data.current_song_uri);
        let color = updateBackground(data.song_image_url, function(color) {
            updateChart(data.acousticness, data.danceability, data.energy, data.instrumentalness, data.liveness, data.loudness, data.speechiness, data.tempo, data.valence, color);
        });
        
        cur_song = data.current_song_uri
    }
}

function updateIndicator(status, pointer) {
    try {
        let el = document.getElementById(pointer)
        if (status) {
            el.style.backgroundColor = '#00A86B';
            el.innerHTML = '<div><i class="fa-regular fa-circle-check fa-xl"></i>&nbsp;&nbsp;In playlist</div>';
        } else {
            el.style.backgroundColor = '#c03030';
            el.innerHTML = '<div><i class="fa-regular fa-circle-xmark fa-xl"></i>&nbsp;&nbsp;Not in playlist</div>';
        }
    } catch (e) {}
}

function updateBackground(imageUri, callback) {
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    const img = document.getElementById('trackImage');
    
    img.src = imageUri
    img.crossOrigin = ''
    img.onload = function() {
        canvas.width = img.naturalWidth;
        canvas.height = img.naturalHeight;
        
        ctx.drawImage(img, 0, 0);
        let dominantColor = colorThief.getColor(img);
        document.body.style.background = `linear-gradient(#1cc458, rgb(${dominantColor[0]}, ${dominantColor[1]}, ${dominantColor[2]}))`;
        const navIcons = document.querySelectorAll('.nav-icon');
        navIcons.forEach(navIcon => {
            navIcon.style.backgroundImage = `-webkit-gradient(linear, left top, left bottom, from(#1cc458), to(rgb(${dominantColor[0]}, ${dominantColor[1]}, ${dominantColor[2]})))`;
        });
        
        callback(dominantColor);
    };
    
    img.onerror = function() {
        callback(null);
    };
}

function updateSpotifyEmbed(trackUri) {
    if (trackUri === undefined || trackUri === null || trackUri === '') return
    
    try {
        const embeds = document.getElementsByClassName('spotify-embed');
        for (let i = 0; i < embeds.length; i++) {
            let height = i == 0 ? 80 : 240;
            
            let embedHtml = `
            <iframe src="https://open.spotify.com/embed/track/${trackUri.split(':')[2]}"
            width="100%" height="${height}" frameborder="0" allowtransparency="true" allow="encrypted-media">
            </iframe>
            `;
            
            embeds[i].innerHTML = embedHtml;
        }
    } catch (e) {}
}

let myChart = null;
async function updateChart(acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, tempo, valence, color) {
    try {
        const el = document.getElementById('featuresIndicator');
        el.innerHTML = `<p>Tempo: ${tempo}bpm<br><br>Loudness: ${loudness}dB</p>`;
        
        const ctx = document.getElementById('featuresChart').getContext('2d');
        if (myChart) {
            myChart.destroy();
        }
        
        let r = color[0], g = color[1], b = color[2];
        if (r + g + b < 255) {
            r += 70;
            g += 70;
            b += 70;
        }
        
        myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Acousticness', 'Danceability', 'Energy', 'Instrumentalness', 'Liveness', 'Speechiness', 'Valence'],
                datasets: [{
                    label: 'Audio Features',
                    data: [acousticness, danceability, energy, instrumentalness, liveness, speechiness, valence],
                    backgroundColor: `rgba(${r}, ${g}, ${b}, 0.3)`,
                    borderColor: `rgba(${r}, ${g}, ${b}, 1)`,
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    tooltip: { enabled: false },
                    legend: { display: false }
                },
                scales: {
                    y: {
                        display: false,
                        ticks: { display: false },
                        border: { display: false }
                    }
                }
            }
        });
    } catch (e) {}
}