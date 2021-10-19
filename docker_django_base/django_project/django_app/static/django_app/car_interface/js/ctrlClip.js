/**
 * 구간 클립 정보 (Key : regionId, Value : Frame(array))
 */

 var clipInfo = new Map();

 const clipsContainer = document.querySelector('.clips-container')
 
 let recentlyPlay
 
 clipsContainer.addEventListener('click', e => {
     if (setFramesRun) return
     let div = e.target.closest('DIV')
     console.log(div)
     if (!div.id || div.id === 'clips') return
     let region = wavesurfer.regions.list[div.id]
     let video = div.querySelector('video')
     recentlyPlay = region
     video.src = orgVideo.src + '#t=' + region.start + ',' + region.end
     video.play()
 })
 
 clipsContainer.addEventListener('mouseout', e => {
     // console.log('mouseout 작동')
     if (setFramesRun) return
     if (!recentlyPlay) return
     if (e.target.id === recentlyPlay.id) {
         let region = wavesurfer.regions.list[recentlyPlay.id]
         let video = document.getElementById(recentlyPlay.id)
         // video.currentTime = region.start;
         // video.pause()
         // change constructure : video -> div/video
         video.querySelector('video').currentTime = region.start;
         video.querySelector('video').pause();
 
         recentlyPlay = null
     } else if (e.target.id !== recentlyPlay.id && e.target.nodeName === 'VIDEO') {
         let region = wavesurfer.regions.list[e.target.id]
         recentlyPlay = region
     }
 })
 
 clipsContainer.addEventListener('dblclick', e => {
     // e.target.id는 regionId
     // console.log(e.target.id);
     e.stopPropagation();
 
     // 삭제 시 tmpImage가 삭제된 regionId를 가지므로 오류발생
     var imageAlt = imgElement.getAttribute('alt');
     if (imageAlt != null) {
         var imageInfo = imgElement.getAttribute('alt').split("^");
         if(clipInfo.has(imageInfo[0])){
             saveSkeleton();
         }  
     }
 
     let div = e.target.closest('DIV')
 
     if (!div.id || div.id === 'clips') return
     let _div = document.getElementById(div.id)
     let video = _div.querySelector('video')
     // console.log(video)
 
     video.pause()
     clearCanvas();
     editAnnotation(wavesurfer.regions.list[div.id])
     showNote(wavesurfer.regions.list[div.id])
     // setFrames -> createFrames -> showFrame
     setFrames(wavesurfer.regions.list[div.id])
 
     function clipHl(){
         // 클립 선택한 것 하이라이트
         var clips = document.querySelectorAll('#clips div video');
 
         for(let elem of clips){
             elem.classList.remove('yellow');
         }
         
         var highlight = document.querySelector(`#clips #${wavesurfer.regions.list[div.id].id} video`);
         highlight.classList.add('yellow');
         
          //경진
          if (mode == '작업' || mode == '재작업'){
             document.getElementById("modelLoad").disabled = false;
             document.getElementById("modelReload").disabled = false;
             document.querySelector(".btn-danger").disabled = false;
             document.getElementById("handpose").disabled = false;
             document.getElementById("note").disabled = false;   
         }

         viewNowClipRejection()
     }
     clipHl();
 
 
     // 세트, 현재 클립 번호(0부터 시작한다.)
     var clipsObject = document.querySelectorAll('#clips div video');
     var yellow_num;
     for(var k=0; k<clipsObject.length; k++){
         if(clipsObject[k].classList.contains('yellow')){
             yellow_num = k;
             break;
         }
     }
     nowClip = [];
     nowClip.push(yellow_num);
     console.log(nowClip);
 
     // 로딩화면
     const frames = document.querySelector(".frames-container");
     const bcRect = frames.getBoundingClientRect();
     const loader = document.querySelector(".loader");
     loader.style.top = bcRect.top+(bcRect.height-120)/2+"px";
     // console.log(bcRect.top)
     loader.style.left = bcRect.left+(bcRect.width-120)/2+"px";
 
     loader.classList.toggle("hide");
 
     setTimeout(function(){
         loader.classList.toggle("hide");
     },1000);
 
     // // 클립(.json) 내보내기 버튼 비활성화
     // const target = document.getElementById('saveResult');
     // target.disabled = true;
 })
 
 function statusDisplayElement(){
     var _div =  document.createElement('div')
     _div.classList.add('clip-status')
     return _div
 }
 
 async function createClip(region, isNowClip) {
     // update clip
     console.count();
     if (document.getElementById(region.id)) return await (function () {
         console.log("createClip region.id : " + region.id)
         updateClip(region)
         if (document.getElementById('frames').children.length) {
             setFrames(region)
         }
     })()
 
 
     // create clip
     let clips = document.querySelector("#clips")
     let clip = document.createElement('div')
     let video = document.createElement('video')
 
     clip.appendChild(video)
     clip.appendChild(statusDisplayElement())
     clipStatusMark(clip.querySelector('.clip-status'), region.data.status)
 
     clip.id = region.id;
     video.src = orgVideo.src + '#t=' + region.start + ',' + region.end;
     video.type = 'video/mpeg';
     // video.id = region.id;
 
     // highlight the now created clip
     var clipsVideo = document.querySelectorAll('#clips div video');
     for (var i = 0; i < clipsVideo.length; i++) {
         clipsVideo[i].classList.remove('yellow');
     }
     video.classList.add('yellow')
 
     clips.appendChild(clip);
 
     //경진
     if (mode == '작업' || mode == '재작업'){
         document.getElementById("modelLoad").disabled = false;
         document.getElementById("modelReload").disabled = false;
         document.querySelector(".btn-danger").disabled = false;
         document.getElementById("handpose").disabled = false;
         document.getElementById("note").disabled = false;   
     }
 
     if(isNowClip){
         // set frames
         setFrames(region)
 
     }
 }
 
 function updateClip(region) {
     console.log('업데이트 작동')
     console.log(region)
     let clip = document.getElementById(region.id)
     let video = clip.querySelector('video')
     video.src = orgVideo.src + '#t=' + region.start + ',' + region.end;
 }
 
 function sortClip() {
     let array = []
     let clips = document.querySelector("#clips")
     
     Object.keys(wavesurfer.regions.list).map(id => {
         let region = wavesurfer.regions.list[id]
         // console.log(region)
         array.push({ id: id, start: region.start, status: region.status })
     })
 
     array.sort((a, b) => {
         if (a.start > b.start) return 1
         if (a.start < b.start) return -1
         return 0
     })
 
     array.map(array => {
         let region = document.getElementById(array.id)
         if(region != null) {
             clips.append(region)
         }  // if not use "if(region != null)" -> null will be shown on clips
     })
 
 }
 
 //  function saveClip() {
 //      var clipTime = [];
 
 //      Object.keys(wavesurfer.regions.list).map(function (id) {
 //          console.log(id)
 //          let region = wavesurfer.regions.list[id];
 
 //          let clips = document.querySelector("#clips");
 //          let clip = document.createElement('video');
 
 //          clip.id = region.id;
 //          clip.src = orgVideo.src + '#t=' + region.start + ',' + region.end;
 //          clip.type = 'video/mpeg';
 
 //          var tIdx = clipTime.length-1;
 
 //          if (tIdx < 0){
 //             clips.appendChild(clip);
 //             clipTime.push(region.start);
 //          }else{
 //             var isChecked = false;
 
 //             while(tIdx >=0){
 //                 if(clipTime[tIdx] <= region.start){
 //                     if(tIdx==clipTime.length-1){
 //                         clips.appendChild(clip);
 //                     }else{
 //                         clips.insertBefore(clip, clips.childNodes[tIdx+1]);
 //                     }
 //                     clipTime.splice(tIdx+1, 0, region.start);
 //                     isChecked = true;
 //                     break;
 //                 }
 //                 tIdx--;
 //             }
 
 //             if(!isChecked){
 //                 if(clipTime[0] >= region.start){
 //                     clips.prepend(clip);
 //                     clipTime.unshift(region.start);
 //                 }else{
 //                     clips.appendChild(clip);
 //                     clipTime.push(region.start);
 //                 }
 //             }
 //          }
 //      })
 
 //  }
 
 //상민
 //데이터 찍기 용
 function viewData(){
     console.log('모든 클립 객체 배열: ')
     console.log(allRegions)
     console.log('모든 클립 5개 묶음 객체 배열: ')
     console.log(sptRegions)
     console.log('작업 중인 세트: ')
     console.log(nowSet)
     console.log('작업 중인 클립: ')
     console.log(nowClip)
     console.log('작업 중인 클립의 완료한 프레임 배열: ')
     console.log(workedFrames)
     console.log('작업 완료한 클립 배열: ')
     console.log(workedClips)
 }

 function viewNowClipRejection(){
    var returned_work = document.forms.returned
    if(!returned_work) return
    console.log('작동한건가?')
    var attributesNum = document.querySelector('#attributes').value
    var textarea = document.querySelector('.middle textarea')
    console.log(attributesNum)
     for(let key in wavesurfer.regions.list){
    textarea.value = ''
        if(wavesurfer.regions.list[key].attributes[attributesNum]){
           textarea.value = wavesurfer.regions.list[key].data.rejection? wavesurfer.regions.list[key].data.rejection : ''
           return
        }
     }
 }
 
 //상민
 function formChangeCheck(){
     var labeling_form = document.forms.edit
     var returned_work = document.forms.returned
     var addRejection = document.querySelector('#addRejection')
     var removeRejection = document.querySelector('#removeRejection')
     var textarea = document.querySelector('.middle textarea')
     var attributesNum = document.querySelector('#attributes')

     labeling_form.addEventListener('change', e => {
         // console.log(e)
         // console.log(nowClip)
         // console.log(allRegions)
         // console.log(wavesurfer.regions.list)
         // console.log(sptRegions)
         statusWorking()
     })
 
     if(returned_work){
         addRejection.addEventListener('click', e => {
             e.preventDefault()

             if(attributesNum.value != ''){
                 var rejectionInfo =  returned_work.rejection.value == '반려 사유 없음'? textarea.value : returned_work.rejection.value
                 textarea.value = textarea.value + rejectionInfo
                 statusRejection('반려', textarea.value)
            }else{
                alert('선택된 클립이 없습니다.')
            }
         })
 
         removeRejection.addEventListener('click', e => {
             e.preventDefault()
             statusRejection('제거')
         })
     }
 
 }
 
 function statusRejection(status, val){
     if(val == '0') return
     console.log(sptRegions[nowSet[0]][nowClip[0]])

     for(let i = 0; i < sptRegions[nowSet[0]].length; i++){
            if(sptRegions[nowSet[0]][i].attributes == sptRegions[nowSet[0]][nowClip[0]].attributes){
             let element = document.getElementById(sptRegions[nowSet[0]][i].id)//리전
             sptRegions[nowSet[0]][i].data['status'] = status
             clipStatusMark(element.querySelector('.clip-status'), status)

             if(status === '반려'){
                 sptRegions[nowSet[0]][i].data['rejection'] =
                 sptRegions[nowSet[0]][i].data['rejection']? sptRegions[nowSet[0]][i].data['rejection']+ ' / ' + val: val
             }else{
                 if(sptRegions[nowSet[0]][i].data['rejection']){
                     delete sptRegions[nowSet[0]][i].data['rejection']

                     clipStatusMark(element.querySelector('.clip-status'), '제거')
                     sptRegions[nowSet[0]][i].data['status'] = ''
                 }
             }

             return (function(){
                console.log(status)
               let task_api_url;
               var param;
               if (window.location.pathname == '/admin/index/adminview'){
                task_api_url = "/admin/index/adminview/task_api"
                param = {
                     id: sptRegions[nowSet[0]][i].id,
                     start: form.elements.start.value,
                     end: form.elements.end.value,
                     attributes: form.elements.attributes.value,
                     group: document.getElementById("groupId").value,
                     work_id : document.getElementById("work_id").value,
                     data: {
                         note: form.elements.note.value,
                         handpose: form.elements.handpose.value,
                         skeleton: sptRegions[nowSet[0]][i].data.skeleton,
                         status: status === '반려'? status : '',
                     }
                 }

                }else{
                    task_api_url = 'task_api'
                    param = {
                         id: sptRegions[nowSet[0]][i].id,
                         start: form.elements.start.value,
                         end: form.elements.end.value,
                         attributes: form.elements.attributes.value,
                         group: document.getElementById("groupId").value,
                         data: {
                             note: form.elements.note.value,
                             handpose: form.elements.handpose.value,
                             skeleton: sptRegions[nowSet[0]][i].data.skeleton,
                             status: status === '반려'? status : '',
                         }
                     }
                }

                 if(status === '반려'){
                    param.data.rejection = val

                   let arrayIndex = memoArray.findIndex(arr => arr.attributes == form.elements.attributes.value)
                    console.log(arrayIndex)
                    if(arrayIndex != -1){ //있으면 업데이트
                        memoArray[arrayIndex] = {
                            attributes: form.elements.attributes.value,
                            rejection: val
                        }
                    }else{ //없으면 추가
                         memoArray.push({
                            attributes: form.elements.attributes.value,
                            rejection: val
                        })
                    }
                 }

                 $.ajax({
                     type : 'POST',
                     url : task_api_url,
                     dataType : 'json',
                     data : JSON.stringify(param),
                     success : function(data){
                         // console.log('Success');
                         // console.log(data)
                         //여기에 클립 완료 표시
                         //상민
                         // alert("정보가 업데이트되었습니다.")
                         console.log('정보 업데이트')
                         setMarkInit()
                     },
                     error : function(e){
                         // console.log('Error');
                         // console.log(e);
                     }
                 }); //ajax
             }())//IIFE
         }//if
     }//for
 }

 
 function statusWorking(){
     for(let key in wavesurfer.regions.list){
         if(wavesurfer.regions.list[key].attributes === (nowSet * 5) + nowClip[0]){//attribute가 맞을 
 
             let element = document.getElementById(wavesurfer.regions.list[key].id)//리전 아이디로 요소 선택
 
             if(wavesurfer.regions.list[key].data['status'] !== '반려' && wavesurfer.regions.list[key].data['status'] !== '완료'){
                 //반려또는 완료가 아닐 때 작업중으로 업데이트 한다.
                 wavesurfer.regions.list[key].data['status'] = '작업중'
                 // console.log('조건 1: ')
                 // console.log(wavesurfer.regions.list[key])
                 clipStatusMark(element.querySelector('.clip-status'), '작업중')
 
                 wavesurfer.regions.list[key].data.note = document.forms.edit.note.value
                 wavesurfer.regions.list[key].data.handpose = document.forms.edit.handpose.value
             }

             return (function(){


               let task_api_url;
               var param;
               if (window.location.pathname == '/admin/index/adminview'){
                task_api_url = "/admin/index/adminview/task_api"
                     param = {
                     id: wavesurfer.regions.list[key].id,
                     start: form.elements.start.value,
                     end: form.elements.end.value,
                     attributes: form.elements.attributes.value,
                     group: document.getElementById("groupId").value,
                     work_id : document.getElementById("work_id").value,
                     data: {
                         note: form.elements.note.value,
                         handpose: form.elements.handpose.value,
                         skeleton: wavesurfer.regions.list[key].data.skeleton,
                         status: status === '반려'? status : '',
                     }
                 }
                }
               else {
                task_api_url = 'task_api'
                       var param = {
                     id: wavesurfer.regions.list[key].id,
                     start: form.elements.start.value,
                     end: form.elements.end.value,
                     attributes: form.elements.attributes.value,
                     group: document.getElementById("groupId").value,
                     data: {
                         note: form.elements.note.value,
                         handpose: form.elements.handpose.value,
                         skeleton: wavesurfer.regions.list[key].data.skeleton,
                         status:  wavesurfer.regions.list[key].data.status
                     }
                 }
                }

 
                 $.ajax({
                     type : 'POST',
                     url : task_api_url,
                     dataType : 'json',
                     data : JSON.stringify(param),
                     success : function(data){
                         // console.log('Success');
                         // console.log(data)
                         //여기에 클립 완료 표시
                         //상민
                         // alert("정보가 업데이트되었습니다.")
                         setMarkInit()            
                     },
                     error : function(e){
                         // console.log('Error');
                         // console.log(e);
                     }
                 });
             }())
         }
     }
 }
 
 // function statusWorkingInit(){
 
 // }//set버튼 클릭시 발생하는 함수
 
 formChangeCheck()//한번만