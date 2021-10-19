let isStart = true;
let startTime = 0;
let endTime = 0;
var newRegion;

var GLOBAL_ACTIONS = { // eslint-disable-line

    // spacebar 키로 영역 설정
    addRegion: function() {
        if(isStart){
            startTime = window.wavesurfer.getCurrentTime();
            isStart = false;
            console.log("start : " + startTime);

            window.wavesurfer.clearMarkers();

            window.wavesurfer.addMarker({
                time: startTime,
                label: "START",
                color: '#ff990a',
                position: 'top'
            })
        }else{
            endTime = window.wavesurfer.getCurrentTime();
            isStart = true;
            console.log("end : " + endTime);

            window.wavesurfer.addMarker({
                time: endTime,
                label: "END",
                color: '#ff990a',
                position: 'top'
            })
            newRegion = window.wavesurfer.addRegion({
                start: startTime,
                end: endTime,
                drag: false,
                resize : false,
                color: randomColor(0.25)
            });
            createClip(newRegion);      
            clipInfo.set(newRegion.id, []);
            sortClip();

            

            window.wavesurfer.clearMarkers();
        }
    },          


    play: function() {
        if(!appStatus.isVideo) return alert('비디오를 업로드 하세요.')

        window.wavesurfer.playPause();
        removeBBox();
        removeCanvas();
        document.getElementById("playBtn").disabled = false;
        document.getElementById("saveBtn").disabled = true;
        $('#occupantArea').empty();
        $('#accordion').empty();
    },

    back: function() {
        window.wavesurfer.skipBackward();        
    },

    forth: function() {
        window.wavesurfer.skipForward();
    },

    'toggle-mute': function() {
        window.wavesurfer.toggleMute();
    }
};

// Bind actions to buttons and keypresses
document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('keydown', function(e) {
        let map = {
            87: 'addRegion', // w(add region)
            32: 'play', // space
        };
        let action = map[e.keyCode];
        if (action in GLOBAL_ACTIONS) {
            if (document == e.target || document.body == e.target || e.target.attributes["data-action"]) {
                e.preventDefault();
            }
        let clip = document.createElement('video');
        clip.addEventListener('dblclick', function (e) {
            e.preventDefault();
        })

            GLOBAL_ACTIONS[action](e);
        }
    });

    [].forEach.call(document.querySelectorAll('[data-action]'), function(el) {
        el.addEventListener('click', function(e) {
            let action = e.currentTarget.dataset.action;
            if (action in GLOBAL_ACTIONS) {
                e.preventDefault();
                GLOBAL_ACTIONS[action](e);
            }
        });
    });
});



// Misc
document.addEventListener('DOMContentLoaded', function() {
    // Web Audio not supported
    if (!window.AudioContext && !window.webkitAudioContext) {
        let demo = document.querySelector('#demo');
        if (demo) {
            demo.innerHTML = '<img src="/example/screenshot.png" />';
        }
    }

    // Navbar links
    let ul = document.querySelector('.nav-pills');
    if ( !ul ) {
        return;
    }

    let pills = ul.querySelectorAll('li');
    let active = pills[0];
    if (location.search) {
        let first = location.search.split('&')[0];
        let link = ul.querySelector('a[href="' + first + '"]');
        if (link) {
            active = link.parentNode;
        }
    }
    active && active.classList.add('active');
});
