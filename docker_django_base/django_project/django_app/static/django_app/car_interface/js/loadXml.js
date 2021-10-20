let isUploadedXml = false;

// xml파일을 #content-target의 text-area로 text load, json parse
const inputXmlFile = document.getElementById("xmlFile");
const xmlFileLoad = document.getElementById('xmlLoad')

xmlFileLoad.addEventListener('click', e => {
    let isExecuted = confirm("작업 내용을 모두 지우고\n새롭게 xml 정보를 로딩할까요?");
    if(isExecuted){
        clearCanvas();
        resetForm();
        resetFrames();
        resetClips()
        resetRegions();
        wavesurfer.regions.list = {};
        localStorage.regions = "";
        sptRegions = [];
        nowSet = [];
        nowClip = [];
        workedFrames = [];
        workedClips = [];
        $('#div_btn').innerHTML = '';
        Delete_Xml();
        inputXmlFile.click();
    }
})
//경진 xml 지우기
function Delete_Xml() {
    $.ajax({
           url: "xml_insert",
           type: "POST",
           success: function() {
       }
    });
}

inputXmlFile.addEventListener('change', getFile)

function getFile(event) {
    isUploadedXml = true;

    const input = event.target
    const file = input.files[0];  // 업로드한 파일이름
    if (!file) return
    if(file.name != xml_name){
        alert("다운로드한 xml 파일과 다른 업로드 파일입니다.")
    }else{
        if ('files' in input && input.files.length > 0) {
            placeFileContent(document.getElementById('content-target'), file)
            xmlFileLoad.querySelector('span').textContent = input.files[0].name.split('.')[0]
        }

        let task_api_url;
        if (window.location.pathname == '/admin/index/adminview') {
            task_api_url = "/admin/index/adminview/task_api"
        }else {
            task_api_url = "task_api"
        }


        // 업로드한 xml 전체 내용을 db insert
        function xmlDbInsert(){
            sptRegions.forEach(fiveRegions =>
                fiveRegions.forEach(param => {
                        let variable = {
                            "id": param.id,
                            "start": param.start,
                            "end": param.end,
                            "attributes": param.attributes,
                            "group" : document.getElementById("groupId").value,
                            "data":{
                                "note": param.data.note,
                                "handpose": param.data.handpose,
                                "skeleton": param.data.skeleton,
                                "status": param.data.status
                            }
                        }

                        $.ajax({
                            type : 'POST',
                            // 한 인스턴스에 모든 xml을 저장시켜 최종적으로 마지막 정보만 저장되는 문제
                            url : task_api_url,
                            dataType : 'json',
                            data : JSON.stringify(variable),
                            success : function(data){
                                // console.log('Success');
                                // console.log(data);
                            },
                            error : function(e){
                                // console.log('Error');
                                // console.log(e);
                            }
                        })
                    }
                )
            );
        }
        setTimeout(function(){
            xmlDbInsert();
        },1000);

    }
}

// 모든 클립 객체 배열
var allRegions = [];

// 모든 클립 5개 묶음 객체 배열
var sptRegions = [];

// 작업 중인 세트
var nowSet = [];

// 작업 중인 클립
var nowClip = [];

// 작업 중인 클립의 완료한 프레임 배열
var workedFrames = [];

// 작업 완료한 클립 배열
var workedClips = [];

function placeFileContent(target, file) {
    readFileContent(file).then(content => {
        target.value = content
        // console.log(content);

        // text to xml
        // parseXml(content)

        // xmlText to json
        // regions : JSON Array
        let regions = xmlText2Json(content)
        allRegions = regions;




        // regions : 227 개 배열
        let regionsLen = allRegions.length;

        if(allRegions.length > 0 && !allRegions[0].hasOwnProperty("id")){
            allRegions.forEach(elm=>{
                wavesurfer.addRegion(elm);
            })
            // allRegions : sort regionTag
            var allRegions = [];
            Object.keys(wavesurfer.regions.list).map(function (id) {
                allRegions.push(wavesurfer.regions.list[id])
            })
        }

        allRegions.sort((a, b) => { // allRegions : arr(생성된 region 개수) [{regionId, startTime}, {regionId, startTime} ......] 정렬
            if (a.start > b.start) return 1
            if (a.start < b.start) return -1
            return 0
        })

        sptRegions = [];
        // regions 5 요소씩 하위배열생성
        for (var i = 0; i < regionsLen; i += 5) sptRegions.push(allRegions.slice(i, i + 5));
        // for(var i=0; i<sptRegions.length; i++) console.log(sptRegions[i]);
        // console.log(sptRegions);

        // 클립 5개 묶음 버튼 생성
        setClipButton(sptRegions.length);

        var regionsasd = document.querySelectorAll('region')
        console.log(regionsasd.length)
    }).catch(error => console.log(error))
}

function readFileContent(file) {
    const reader = new FileReader()
    return new Promise((resolve, reject) => {
        reader.onload = event => resolve(event.target.result)
        reader.onerror = error => reject(error)
        reader.readAsText(file)
    })
}

function xmlText2Json(content){
    var xml2json = new XMLtoJSON();
    var objson = xml2json.fromStr(content);	// object 형식			
    // var strjson = xml2json.fromStr(content, 'string');	// string 형식
    // console.log(objson)
    // console.log(strjson)

    let videoItem = objson.BandicutProjectFile.VideoItem;

    let videoItemLen = Object.keys(videoItem).length;
    // console.log(videoItemLen);
    var regions = new Array();
    var elmJson = new Object();
    for(var i=0; i<videoItemLen; i++){
        let seq = videoItem[i]["@attributes"].Index;
        let title = videoItem[i]["@attributes"].Title;
        let start = String(videoItem[i]["@attributes"].Start / 1000000);
        let end = String(videoItem[i]["@attributes"].End / 1000000);
        // console.log("title : " + title + " | start : " + start + " | end : " + end);


        elmJson = {
            "start": start,
            "end": end,
            "attributes": seq,
            "group" : document.getElementById("groupId").value,
            "data":{
                "note": title,
                "handpose": "",
                "skeleton":[],
                "status": ""
            }
        }

        regions.push(elmJson);

    }
    // console.log(regions)

    return regions            
}


// xml 파싱 START
// function parseXml(inputXml){
    // if (window.DOMParser){
    //     parser=new DOMParser();
    //     xmlDoc=parser.parseFromString(inputXml,"text/xml");
    // } else // 인터넷 익스플로러
    // {
    //     xmlDoc=new ActiveXObject("Microsoft.XMLDOM");
    //     xmlDoc.async=false;
    //     xmlDoc.loadXML(inputXml); 
    // } 
    
    // var xml = xmlDoc.getElementsByTagName('VideoItem');
    // var name = xml[0];

    // console.log(name);
    // xml 파싱 END
// }
   
// const btnGetResult = document.getElementById('saveResult');
// if(workedFrames.includes(0) && workedFrames.includes(1) && workedFrames.includes(2) && workedFrames.includes(3) && workedFrames.includes(4)){
    // btnGetResult.disabled = false;
// }else{
    // btnGetResult.disabled = true;
// }