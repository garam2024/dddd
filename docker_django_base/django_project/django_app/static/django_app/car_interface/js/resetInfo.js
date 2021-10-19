/**
 * delete-region bind controls.
 */
 function deleteRegion(){
    const confirmed = confirm("삭제 후 클립 생성이 불가능합니다.\n클립을 삭제하시겠습니까?");
    if (confirmed) {
        let form = document.forms.edit;
        let regionId = form.dataset.region;  // eg. wavesurfer_efohn92htho

        if (regionId) {
            // db region instance 삭제
            let regionInfo = wavesurfer.regions.list[regionId];
            let param = {
                "id": regionId,
                "start": regionInfo.start,
                "end": regionInfo.end,
                "attributes": regionInfo.attributes,
                "data":{
                    "note": regionInfo.data.note,
                    "handpose": regionInfo.data.handpose,
                    "skeleton":regionInfo.data.skeleton
                }
            }
            $.ajax({
                type : 'POST',
                url : 'task_region_delete',
                dataType : 'json',
                data : JSON.stringify(param),
                success : function(data){
                    console.log('Success');
                    console.log(data)
                },
                error : function(e){
                    console.log('Error');
                    console.log(e);
                }
            });


            // 브라우저 저장정보 삭제
            let framse = document.querySelector('#frames')
            if (framse.dataset.regionId === regionId) {
                framse.innerHTML = ''
                framse.dataset.regionId = ''
                deleteAllFrame(wavesurfer.regions.list[regionId])
            }
            wavesurfer.regions.list[regionId].remove();
            document.getElementById(regionId).remove()
            clipInfo.delete(regionId);
            form.reset();

            sptRegions[nowSet[0]].splice(nowClip[0], 1);
            if(sptRegions[nowSet[0]].length < 1){
                // delete sptRegions element
                sptRegions.splice(nowSet[0], 1)

                // delete setBtn
                document.querySelectorAll('#sets')[nowSet[0]].remove();

                // reset nowSet
                const beforeSet = nowSet[0]
                nowSet = []
                if(beforeSet > 0)  nowSet.push(beforeSet -1)
            }
            alert("영역이 삭제되었습니다.")
            //경진 클립 삭제후 버튼 끄기
            document.querySelector(".btn-danger").disabled = true;
            document.getElementById("modelLoad").disabled = true;
            document.getElementById("modelReload").disabled = true;
            document.getElementById("handpose").disabled = true;
            document.getElementById("note").disabled = true;

        }
        setMarkInit()
        chkFinalCmpl();
        window.wavesurfer.clearMarkers();
        clearCanvas();
    }
};

function resetForm(){
    // reset form
    let form = document.forms.edit;
    form.reset();
}

function resetFrames(){
    // reset all frames
    let framse = document.querySelector('#frames');
    framse.innerHTML = '';
    framse.dataset.regionId = '';
}

function resetClips(){
    // reset all clips
    $("#clips").empty();
    clips.dataset.regionId = '';
    // clipInfo.clear()를 지우면 xml import 작업 시 export에서 5개 세트 clipInfo의 순서가 꼬여 key를 읽지 못해 undefined를 export한다.
    // clipInfo.clear()를 지우면 out of memory 발생할 것
    clipInfo.clear();
}

function resetRegions(){
    // reset all region
    window.wavesurfer.clearMarkers();
    var regionsElm = document.getElementsByTagName("region"), index;
    for (index = regionsElm.length - 1; index >= 0; index--) {
        regionsElm[index].parentNode.removeChild(regionsElm[index]);
    }
    // wavesurfer.regions.list = {};
    // localStorage.regions = "";
}

function chkFinalCmpl(){
      // final_complete check
      let completeCnt = 0
      document.querySelectorAll('#sets').forEach(el => {
          if(el.classList.contains('complete')){
              completeCnt++;
          }
      });
      var ele = document.getElementById('div_btn');
      var eleCount = ele.childElementCount;
      if(completeCnt == eleCount){
          document.getElementById("final_complete").disabled = false;
      }
}