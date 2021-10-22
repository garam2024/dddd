/**
 *  waveSurfer 변수
 **/
 var wavesurfer;

var createNum = function(list){
  var number = []
  console.log(list)
  if(Object.keys(list).length === 0) return 0
  for(let key in list){
    console.log(list[`${key}`].attributes)
    number.push(parseInt(list[`${key}`].attributes))
  }
    console.log(Math.max(...number) + 1)
  return Math.max(...number) + 1
}

 /**
  * 비디오 로딩
  */
 // document.addEventListener('DOMContentLoaded', function loadVideo() {
 function loadVideo(jsonFile, modeSelect) {

     console.log('비디오 로드 작동')
     window.mode = modeSelect;
     // console.log(modeSelect)
     wavesurfer = WaveSurfer.create({
         container: document.querySelector('#waveform'),
         waveColor: "#FFFFFF",
         progressColor: "#FFFFFF",
         cursorColor: "#333",
         cursorWidth: "4",
         height: 60,
         pixelRatio: 1,
         minPxPerSec: 100,
         scrollParent: true,
         normalize: true,
         splitChannels: false,
         backend: 'MediaElement',
         plugins: [
             WaveSurfer.regions.create(),
             WaveSurfer.minimap.create({
                 height: 20,
                 waveColor: '#ddd',
                 progressColor: '#999'
             }),
             WaveSurfer.timeline.create({
                 container: '#wave-timeline'
             }),
             WaveSurfer.cursor.create(),
             WaveSurfer.markers.create()
         ]
     });
 
 
     let mediaElt = document.querySelector('#demo video');
 
     //  canvas.setDimensions({
     //     width: mediaElt.width, 
     //     height: mediaElt.height
     // })
 
     wavesurfer.on('error', function (e) {
         console.warn(e);
     });
 
     wavesurfer.load(mediaElt);


     // 저장된 JSON 정보 불러오기
     wavesurfer.on('ready', function () {
         console.log('ready 작동')
         task_id = createNum(wavesurfer.regions.list)
         console.log(task_id)
         wavesurfer.enableDragSelection({
             // color: randomColor(0.25),
             slop: 1,
             loop: false
         });
 
         // wavesurfer.disableDragSelection({
         //     color: randomColor(0.25),
         //     slop: 1,
         //     loop: false,
 
         //     drag: false,
         //     resize: false
         // });
 
 
         if (jsonFile) {
             wavesurfer.enableDragSelection();
             wavesurfer.util
                 .fetchFile({
                     responseType: 'json',
                     url: jsonFile
                 })
                 .on('success', function (data) {
                     console.log(data)
                     loadRegions(data);
                     saveRegions();
                 });
         }
     });
 
     wavesurfer.on('region-click', function (region, e) {
         e.stopPropagation();
 
         console.log("----start----------------")
         console.log("region-click region.id : " + region.id)
 
         // array : sort regionTag
         var array = [];
         Object.keys(wavesurfer.regions.list).map(function (id) {
             array.push(wavesurfer.regions.list[id])
         })
         array.sort((a, b) => { // array : arr(생성된 region 개수) [{regionId, startTime}, {regionId, startTime} ......] 정렬
             if (a.start > b.start) return 1
             if (a.start < b.start) return -1
             return 0
         })
 
 
         let index = 0;
         let isCheckedIndx = false;
         for (var i = 0; i < array.length; i++) {
             if (region.id == array[i].id) {
                 index = i;
                 isCheckedIndx = true;
             }
         }
         if (!isCheckedIndx) {
             console.log("--------------------------------------------------")
             console.log("선택한 regions이 생성된 region 태그 목록에 없습니다.")
             console.log("seleted region.id : " + region.id)
             console.log("--------------------------------------------------")
         }
 
         // now set
         nowSet = []
         nowSet.push(parseInt(index / 5));
         // now clip
         nowClip = []
         nowClip.push(index % 5);
 
         // 상민
         // window.store['nowSelectedSet'] = i
 
 
         // reset setBtn with sptRegions.length
         $('#div_btn').html('');
         setClipButton(sptRegions.length);
 
         // setBtn highlight
         var setBtns = document.querySelectorAll('#sets');
         for (var j = 0; j < setBtns.length; j++) {
             setBtns[j].classList.remove('yellow');
         }
         setBtns[nowSet[0]].classList.add('yellow');
 
 
         if (sptRegions[nowSet[0]].length > 0) {
 
             function waitFrames() {
                 return new Promise((resolve, reject) => {
 
                     // reset view
                     clearCanvas();
                     window.wavesurfer.clearMarkers();
                     resetForm();
                     resetFrames();
                     deleteAllFrame(region);
                     resetClips();
 
 
                     // save json{start, end, attributes, note, handpose, sekleton} to localStorage.regions
                     saveRegions(sptRegions[nowSet[0]]);
                     // new clipInfo, createClip, sortClip with 'sptRegions[setNum][clipNum]'
                     let isNowClip = false;
                     for (var p = 0; p < sptRegions[nowSet[0]].length; p++) {
                         if (p == nowClip[0]) {
                             isNowClip = true
                         } else {
                             isNowClip = false
                         }
                         loadOneRegion(sptRegions[nowSet[0]][p], isNowClip)
                     }
                     // sptRegions[nowSet[0]].forEach(elm => {
                     //     loadOneRegion(elm);
                     // })
 
 
                     // show loading view on clips
                     const frames = document.querySelector(".clips-container");
                     const bcRect = frames.getBoundingClientRect();
                     const loader = document.querySelector(".loader");
                     loader.style.top = bcRect.top + (bcRect.height - 120) / 2 + "px";
                     // console.log(bcRect.top)
                     loader.style.left = bcRect.left + (bcRect.width - 120) / 2 + "px";
 
                     loader.classList.toggle("hide");
 
                     setTimeout(function () {
                         loader.classList.toggle("hide");
                     }, 800);
 
 
                     // save the skeleton of just before work
                     // img#tmpImage -> imgElement "alt" -> imageAlt.split("^")[0] -> if clipInfo.has(regionId) -> saveSkeleton
                     var imageAlt = imgElement.getAttribute('alt');
                     if (imageAlt != null) {
                         var imageInfo = imgElement.getAttribute('alt').split("^");
                         if (clipInfo.has(imageInfo[0])) {
                             saveSkeleton();
                         }
                     }
 
 
                     // show video with now created clip
                     const nowClipId = $("#clips").children()[nowClip[0]].getAttribute('id');
                     let video = document.getElementById(nowClipId).querySelector('video')
                     video.pause()
                     clearCanvas();
 
 
                     // highlight the now seleted clip
                     var clipsVideo = document.querySelectorAll('#clips div video');
                     for (var i = 0; i < clipsVideo.length; i++) {
                         clipsVideo[i].classList.remove('yellow');
                     }
                     video.classList.add('yellow')
 
 
                     // editAnnotation, showNote, setFrames with the region info of nowClipId
                     const clipRegion = wavesurfer.regions.list[nowClipId];
                     //console.log(clipRegion)
                     editAnnotation(clipRegion);
                     showNote(clipRegion);
                     // setFrames(clipRegion);
 
 
                     // highlight now clip
                     // var clips = document.querySelectorAll('#clips div video');
                     // for (let elem of clips) {
                     //     elem.classList.remove('yellow');
                     // }
                     // var highlight = document.querySelector(`#clips #${nowClipId} video`);
                     // highlight.classList.add('yellow');
 
 
                     // show loading view on frames
                     const framesCon = document.querySelector(".frames-container");
                     const framesBcRect = framesCon.getBoundingClientRect();
                     const frameLoader = document.querySelector(".loader");
                     frameLoader.style.top = framesBcRect.top + (framesBcRect.height - 120) / 2 + "px";
                     frameLoader.style.left = framesBcRect.left + (framesBcRect.width - 120) / 2 + "px";
 
                     frameLoader.classList.toggle("hide");
 
                     setTimeout(function () {
                         frameLoader.classList.toggle("hide");
                     }, 1000);
                     console.log("-----------------------------------------")
                     console.log("nowSet : " + nowSet[0])
                     console.log("nowClip : " + nowClip[0])
                     console.log("-----------------------------------------")
 
 
                     resolve();
                 });
             };
 
             async function regionPlay() {
                 await waitFrames();
 
                 //상민
                 // var clipsDiv = document.querySelectorAll('#clips .clip-status')
 
                 // for (let z = 0; z < window.store['sptRegions'][i].length; z++) {
                 //     let status = window.store['sptRegions'][i][z].data.status
                 //     clipStatusMark(clipsDiv[z], status)
                 // }
 
                 // setMark(i, setCheck(window.store['sptRegions'][i]))
 
 
                 // video play
                 // region.play를 setTimeout 하지 않으면 재생 2번됨
                 setTimeout(() => {
                     region.play();
                 }, 2000);
             }

             //211020
             // regionPlay();
         }
     });
 
 
 
     if (mode == '작업' || mode == '재작업') {
         // region create, move, resize
         wavesurfer.on('region-update-end', function (region) {
            console.log('업데이트 작동')
             if(regionOver(region)) return
             resetRegionInfo(region)

             console.log("------------------------------")
             console.log("nowSet : " + nowSet[0])
             console.log("nowClip : " + nowClip[0])
             console.log("------------------------------")


             // disable final submit btn
         })
         wavesurfer.on('region-updated', saveRegions);
         wavesurfer.on('region-removed', saveRegions);
 
     } else if (mode == '검수' || mode == '재검수') {
         // disable region create, move, resize
         wavesurfer.on('region-updated', function (region) {
             var regions = region.wavesurfer.regions.list;
             // if new created region -> remove
             if (Object.keys(region.data).length === 0){
                 regions[region.id].remove();
             }
         });
     }
 
 
     function resetRegionInfo(region) {
        console.log('resetRegionInfo 작동')
        console.log(region.id)
         // merge sptRegions
         let mergeSptRegions = []
         sptRegions.forEach(elm => {
             elm.forEach(m => {
                 mergeSptRegions.push(m)
             })
         })
 
         let checkInRegionTag = false;
         mergeSptRegions.forEach(elm => {
             if (elm.id == region.id) {
                 // move, resize region : true
                 // create : false
                 checkInRegionTag = true
             }
         })
 
         // check console.log(move, resize, create)
         if (checkInRegionTag) {
             // console.log("-------------------------------------------------")
             console.log('region-update-end 작동 : move, resize')
             // console.log("region not in sptRegions")
             // console.log("resize or moved reion.id : " + region.id)
             // console.log("existed region.id : ")
             // for(var i=0; i<mergeSptRegions.length; i++){
             //     console.log(mergeSptRegions[i].id)
             // }
             // console.log("-------------------------------------------------")
         } else {
             console.log('region-update-end 작동 : create')
         }
 
 
         if (!checkInRegionTag) { // if create region
             // 생성한 region에는 attributes, note, handpose, skeleton 값이 없으므로 설정
             region.attributes = task_id
             task_id++
             region.data = {
                 "note": "",
                 "handpose": "",
                 "skeleton": []
             }
         }
 
         // array : sort wavesurfer.regions.list 
         var array = [];
         Object.keys(wavesurfer.regions.list).map(function (id) {
             array.push(wavesurfer.regions.list[id])
         })
         array.sort((a, b) => { // array : arr(생성된 region 개수) [{regionId, startTime}, {regionId, startTime} ......] 정렬
             if (a.start > b.start) return 1
             if (a.start < b.start) return -1
             return 0
         })
 
         sptRegions = []
         var tmpArr = []
         let isNowClip = false;
         var clipNum = 0,
             setNum = 0; // clipNum : 5개 클립 중 순서, setNum : 세트 번호 중 순서
 
         for (var k = 0; k < array.length; k++) {
             // set the attributes value of region order by acending
             // array[k].attributes = k;
             // console.log("array k attributes-------------------------------")
             // console.log(array[k].attributes)
 
             if (tmpArr.length < 5) {
                 tmpArr.push(array[k]);
                 sptRegions.pop()
                 sptRegions.push(tmpArr)
             } else {
                 tmpArr = [];
                 tmpArr.push(array[k]);
                 sptRegions.push(tmpArr);
             }
 
             if (!isNowClip && array[k].id == region.id) {
                 clipNum = k % 5;
                 setNum = sptRegions.length - 1
                 isNowClip = true;
             }
         }
         console.log("------------------------")
         console.log("setNum : " + setNum)
         console.log("clipNum : " + clipNum)
         console.log("------------------------")
 
         // sptRegions 개수 보고 세트 버튼 생성
         $('#div_btn').html('');
         setClipButton(sptRegions.length);
 
 
         // setNum 순서 해당하는 set 버튼 하이라이트
         var setBtns = document.querySelectorAll('#sets');
         for (var j = 0; j < setBtns.length; j++) {
             setBtns[j].classList.remove('yellow');
         }
         setBtns[setNum].classList.add('yellow');
 
 
         if (sptRegions[setNum].length > 0) {
             // set now setNum value to nowSet
             nowSet = [];
             nowSet.push(setNum);
 
             // reset view
             clearCanvas();
             window.wavesurfer.clearMarkers();
             resetForm();
             resetFrames();
             deleteAllFrame(region);
             // if (sptRegions[setNum].length < 2) { // when create new setBtn
             //     resetClips();
             // }
             resetClips();
 
             // if (sptRegions[setNum].length < 2) { // when over 5 clips, reset Region except now created region
             //     resetClips();
             //     window.wavesurfer.clearMarkers();
             //     var regionsElm = document.getElementsByTagName("region"),
             //         index;
             //     for (index = regionsElm.length - 2; index >= 0; index--) {
             //         regionsElm[index].parentNode.removeChild(regionsElm[index]);
             //     }
             // }
 
 
 
             saveRegions(sptRegions[setNum]); // save json{start, end, attributes, note, handpose, sekleton} to localStorage.regions
             // if (!checkInRegionTag) { // if create region
             //     loadOneRegion(sptRegions[setNum][clipNum]); // addRegion, new clipInfo, createClip, sortClip with 'sptRegions[setNum][clipNum]'
             // } else {
             //     // resize, move
             //     sptRegions[setNum].forEach(elm => {
             //         loadOneRegion(elm);
             //     })
             // }
             sptRegions[setNum].forEach(elm => {
                 loadOneRegion(elm, true);
             })
 
 
             // show loading view on clips
             const frames = document.querySelector(".clips-container");
             const bcRect = frames.getBoundingClientRect();
             const loader = document.querySelector(".loader");
             loader.style.top = bcRect.top + (bcRect.height - 120) / 2 + "px";
             // console.log(bcRect.top)
             loader.style.left = bcRect.left + (bcRect.width - 120) / 2 + "px";
 
             loader.classList.toggle("hide");
 
             setTimeout(function () {
                 loader.classList.toggle("hide");
             }, 800);
 

             //211020
             // img#tmpImage -> imgElement "alt" -> imageAlt.split("^")[0] -> if clipInfo.has(regionId) -> saveSkeleton
             // var imageAlt = imgElement.getAttribute('alt');
             // if (imageAlt != null) {
             //     var imageInfo = imgElement.getAttribute('alt').split("^");
             //     if (clipInfo.has(imageInfo[0])) {
             //         saveSkeleton();
             //     }
             // }
 
 
             // set now clipNum value to nowClip
             nowClip = [];
             nowClip.push(clipNum);
 
 
             // show video with now created clip
             const nowClipId = $("#clips").children()[clipNum].getAttribute('id');
             let video = document.getElementById(nowClipId).querySelector('video')
             video.pause()
             clearCanvas();
 
 
             // editAnnotation, showNot, setFrames with the region info of nowClipId
             const clipRegion = wavesurfer.regions.list[nowClipId];
             //console.log(clipRegion)
             editAnnotation(clipRegion);
             showNote(clipRegion);
             // setFrames(clipRegion);
 
 
             // highlight now clip
             var clips = document.querySelectorAll('#clips div video');
             for (let elem of clips) {
                 elem.classList.remove('yellow');
             }
             var highlight = document.querySelector(`#clips #${nowClipId} video`);
             highlight.classList.add('yellow');
 
 
             // show loading view on frames
             const framesCon = document.querySelector(".frames-container");
             const framesBcRect = framesCon.getBoundingClientRect();
             const frameLoader = document.querySelector(".loader");
             frameLoader.style.top = framesBcRect.top + (framesBcRect.height - 120) / 2 + "px";
             frameLoader.style.left = framesBcRect.left + (framesBcRect.width - 120) / 2 + "px";
 
             frameLoader.classList.toggle("hide");
 
             setTimeout(function () {
                 frameLoader.classList.toggle("hide");
             }, 1000);
         } else {
             console.log("sptRegion[setNum].length == 0")
         }
         // console.log(sptRegions);
         console.log(region.id)

         return (function(region){
            console.log('리셋 리전 셋 프레임스' , region.id)
             setFrames(region)
            document.querySelector(".btn-success").disabled = true;

         }(region))


     };
 
 
     wavesurfer.on('region-created', region => {
         // console.log(region)
         // console.log(region.id)
         // console.log(wavesurfer.regions.list)
         //리전 수정 불가
        console.log('region 드래그 불가')
        region.drag = false
        region.resize = false
     })
 
     // else {
     //     wavesurfer.on('region-click', editAnnotation);
     // }
     wavesurfer.on('region-in', showNote);
     wavesurfer.on('region-out', hideNote);
     wavesurfer.on('region-play', function (region) {
         region.once('out', function () {
             wavesurfer.play(region.start);
             wavesurfer.pause();
         });
     });
 
     /* Toggle play/pause buttons. */
     let playButton = document.querySelector('#play');
     let pauseButton = document.querySelector('#pause');
 
     wavesurfer.on('play', function () {
         pauseButton.style.display = 'block';
         playButton.style.display = 'none';
 
         clearCanvas();
         render();
     });
 
     wavesurfer.on('pause', function () {
         playButton.style.display = 'block';
         pauseButton.style.display = 'none';
         cancelAnimationFrame(renderCanvas)
     });
 
     wavesurfer.on('waveform-ready', function () {
         loader.classList.toggle("hide");
     });
 
 }
 
 
 //  videoElement.addEventListener("loadedmetadata", render);
 let renderCanvas
 const videoElement = document.querySelector('#orgVideo');
 
 function render() {
     const canvas = document.querySelector('#canvas');
     const ctx = canvas.getContext('2d');
 
     ctx.drawImage(videoElement, 0, 0, 800, 450);
 
     // 첫 번째 인자로 비디오를 넣어준다.
     renderCanvas = requestAnimationFrame(render);
 }
 
 
 /**
  * 로컬스토리지에 전사, 라벨링, 스켈레톤 정보 저장
  */
 function saveRegions() {
     // console.log('saveRegions')
     localStorage.regions = JSON.stringify(
         Object.keys(wavesurfer.regions.list).map(function (id) {
             let region = wavesurfer.regions.list[id];
             if (region.attributes == {}) {
                 region.attributes = 0
             }
 
             var frameList = clipInfo.get(id);
             var frameJson = [];
 
             if (frameList != null) {
                 frameList.forEach(frame => {
                     frameJson.push({
                         'time': frame.time,
                         'skeleton_positions': frame.skeleton
                     });
                 });
             }
 
             // console.log("saveRegions attributes ----------------------")
             // console.log(region.attributes)
 
             return {
                 start: Math.round(region.start * 1000000) / 1000000,
                 end: Math.round(region.end * 1000000) / 1000000,
                 attributes: region.attributes,
                 data: {
                     note: region.data.note,
                     handpose: region.data.handpose,
                     skeleton: frameJson
                 }
             };
         })
     );
 }
 
 
 /**
  *  addRegion, new clipInfo, createClip, sortClip from json
  */
 function loadRegions(regions) {
     // console.log("loadRegions--------------------------")
 
     regions.forEach(function (elm) {
         // console.log(elm)
         tmpFramelist = [];
         // elm.color = randomColor(0.25);
         if (elm.data.skeleton.length > 0) {
             tmpFramelist = elm.data.skeleton
         }
 
         // add region to wavesurfer
         var newRegion = wavesurfer.addRegion(elm);
 
         // // 생성한 region을 drag, resize 방지
         // for(var i=0; i<wavesurfer.regions.list.length; i++){
         //     wavesurfer.regions.list[i].update({drag: false, resize: false});
         // }
 
         clipInfo.set(newRegion.id, tmpFramelist);
         createClip(newRegion, true);
     });
     sortClip();
     //상민
     // setMarkInit()
 }
 
 
 
 /**
  *  addRegion, new clipInfo, createClip, sortClip with 'sptRegions[setNum][clipNum]'
  */
 function loadOneRegion(elm, isNowClip) {
//      console.log("loadRegions--------------------------")
//      console.log(elm)
//      console.log(isNowClip)
     let tmpFramelist = [];
     // elm.color = randomColor(0.25);
     if (elm.data.skeleton && elm.data.skeleton.length > 0) { //
         tmpFramelist = elm.data.skeleton
     }


     // add region to wavesurfer
     // var newRegion = wavesurfer.addRegion(elm);
 
     // // 생성한 region을 drag, resize 방지
     // for(var i=0; i<wavesurfer.regions.list.length; i++){
     //     wavesurfer.regions.list[i].update({drag: false, resize: false});
     // }
     if (elm.hasOwnProperty("id")){
         clipInfo.set(elm.id, tmpFramelist);
         createClip(elm, isNowClip);
     }else{
         var newRegion = wavesurfer.addRegion(elm);

         clipInfo.set(newRegion.id, tmpFramelist);
         createClip(newRegion, isNowClip);
     }

     sortClip();
 }


 /**
  * Random RGBA color.
  */
 function randomColor(alpha) {
     return (
         'rgba(' + [
             ~~(Math.random() * 255),
             ~~(Math.random() * 255),
             ~~(Math.random() * 255),
             alpha || 1
         ] +
         ')'
     );
 }
 
 
 /**
  * Web Audio not supported의 경우 sample wave img 보여주기
  */
 // Misc
 document.addEventListener('DOMContentLoaded', function () {
     // Web Audio not supported
     if (!window.AudioContext && !window.webkitAudioContext) {
         let demo = document.querySelector('#demo');
         if (demo) {
             demo.innerHTML = '<img src="/example/screenshot.png" />';
         }
     }
 });


function regionOver(region) {
    let regionId = region.id;
    let startList = [];
    let endList = [];

    for (var key in wavesurfer.regions.list) {
        startList.push(wavesurfer.regions.list[key].start);
        endList.push(wavesurfer.regions.list[key].end);
    }
    startList = startList.sort(function (a, b) {
        return a - b;
    });;
    endList = endList.sort(function (a, b) {
        return a - b;
    });;
    let currntNum = startList.findIndex((e) => e === region.start);
    let backRegionEnd = endList[currntNum - 1];
    let nextRegionStart = startList[currntNum + 1];

    if (region.end > nextRegionStart || region.start < backRegionEnd) {
        if(wavesurfer.regions.list[regionId]){
            wavesurfer.regions.list[regionId].remove();
        }

        alert('구간설정 중복은 불가능 합니다.')
        return true
    }

    return false
}