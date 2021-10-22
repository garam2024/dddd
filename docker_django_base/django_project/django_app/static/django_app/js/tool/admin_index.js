let currentPage = 0;


if (window.location.pathname == '/admin/index/'){

$.ajax({
    type:'POST',
    url : '/admin/index/get_statusDic',
    async:false,
    success : function(data){
        dbinfo = data
        console.log(dbinfo)
    },
    error:function(err){
    alert('작업상태불러오기실패_새로고침을눌러주세요')
    },
    })


function SortTable(table){
    this.table = table
} 

SortTable.prototype.sorting = function(n){
    let rows, switching, i, x, y, shouldSwitch, switchCount = 0
    table = document.querySelector(this.table)
    dir = 'asc'
    switching = true

    while(switching){
        switching = false
        rows = table.rows
        for(i = 1; i < (rows.length - 1); i++){
            shouldSwitch = false
            x = rows[i].getElementsByTagName('TD')[n]
            y = rows[i + 1].getElementsByTagName('TD')[n]

            if(dir === 'asc'){
                if(x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()){
                    shouldSwitch = true;
                    break
                }
            }else if(dir === 'desc'){
                if(x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()){
                    shouldSwitch = true;
                    break
                }
            }else{
                break
            }
        }

        if(shouldSwitch){
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i])
            switching = true
            switchCount++
        }else{
            if(switchCount === 0 && dir === 'asc'){
                dir = 'desc'
                switching = true
            }
        }
    }

}

const tableTab01 = new SortTable('#table-tab-01')
const tableTab02 = new SortTable('#table-tab-02')

if (window.location.pathname == '/admin/index/'){
const tableSortingButton01 = document.querySelector('#table-tab-01 thead tr')
tableSortingButton01.addEventListener('click', function(e){
    if(!e.target.dataset.number) return
    tableTab01.sorting(e.target.dataset.number)
})
}
else {
const tableSortingButton02 = document.querySelector('#table-tab-02 thead tr')
tableSortingButton02.addEventListener('click', function(e){
    if(!e.target.dataset.number) return
    tableTab02.sorting(e.target.dataset.number)
})
}









if (window.location.pathname == '/admin/index/'){
function Tabmenu(tabEl, btnEl){
    this.tabEl = tabEl
    this.btnEl = btnEl

    this._tabEl = document.querySelectorAll(this.tabEl)
    this._btnEl = document.querySelectorAll(this.btnEl)

    this.activeBtn
    this.activeTab
}

Tabmenu.prototype.showTab = function(activeBtn, activeTab){
    let { _btnEl, _tabEl } = this

    _btnEl.forEach(function(el, i){
        el.addEventListener('click', function(){

            if(activeBtn){
                activeBtn.classList.remove('active')
                activeTab.classList.remove('active')
            }
            el.classList.add('active')
            _tabEl[i].classList.add('active')
            activeBtn = el
            activeTab = _tabEl[i]
        })
    })
}

Tabmenu.prototype.init = function(){
    let { _tabEl, _btnEl, activeBtn, activeTab } = this

    _tabEl[0].classList.add('active')
    _btnEl[0].classList.add('active')

    activeTab = _tabEl[0]
    activeBtn = _btnEl[0]

    this.showTab(activeBtn, activeTab)
}

const tabmenu = new Tabmenu('.tab', '.side-nav button')

tabmenu.init()
}
else {}



var searchForm = document.forms.searchForm

searchForm.addEventListener('submit', e => {
    e.preventDefault()
    jsf_ajax_dataloading(0)
})
function jsf_ajax_dataloading(page){
    let user_group_id = $("#group_id").val();
    if(user_group_id == "-"){
        var { workerNm, workType, workStatus, searchBgn, searchEnd, workGroup } = searchForm;
        console.log(workerNm.value, workType.value, workStatus.value, searchBgn.value, searchEnd.value);
        searchData = {
            workerNm: workerNm.value,
            workType: workType.value,
            workStatus: workStatus.value,
            searchBgn: searchBgn.value,
            searchEnd: searchEnd.value,
            groupId: workGroup.value,
            page : page
        }
    }else{
        var { workerNm, workType, workStatus, searchBgn, searchEnd} = searchForm;
        console.log(workerNm.value, workType.value, workStatus.value, searchBgn.value, searchEnd.value);
        searchData = {
            workerNm: workerNm.value,
            workType: workType.value,
            workStatus: workStatus.value,
            searchBgn: searchBgn.value,
            searchEnd: searchEnd.value,
            groupId: user_group_id,
            page : page
        }
    }

    console.log(searchData)

    $.ajax({
        type: 'post',
        url: 'get_search_data',
        data : JSON.stringify(searchData),
        async: false,
        success: function(data){
            console.log(data)
           if(data.messages == 'false'){
            alert('검색 조건을 입력하세요.')
           }else{
            var workViewTable = document.querySelector('.workViewTable')

                if(data.length != 0){

                    workViewTable.innerHTML = ''
                    var worklist_len = $("#postLength").val(data[0].tot_cnt);
                    for(let i = 0; i < data.length; i ++){
                        var status = statusButton(data[i].work_status)

                        var tr = document.createElement('tr')
                        workViewTable.append(tr)
                        var group_id = group(data[i].group_id)
                        var statusNum = userByStatus(data[i].work_status)
                        tr.innerHTML +=`
                            <td>${data[i].work_id? data[i].work_id: '-'}</td>
                            <td>${data[i].str_type? data[i].str_type: '-'}</td>
                            <td>${data[i]['worker_name' + statusNum]? data[i]['worker_name' + statusNum]: '-'}</td>
                            <td>${data[i].str_status? data[i].str_status: '-'}</td>`
                        if (user_group_id == "-"){
                            tr.innerHTML +=`
                                <td>${group_id? group_id: '-'}</td>
                                <td>${status? '<button data-work="admin_work_view">작업보기</button>' : '-'}</td>
                                <td>${data[i].reg_date? data[i].reg_date.split('T')[0]: '-'}</td>`
                        }else{
                            tr.innerHTML +=`
                                <td>${status? '<button data-work="admin_work_view">작업보기</button>' : '-'}</td>
                                <td>${data[i].reg_date? data[i].reg_date.split('T')[0]: '-'}</td>`
                        }

                        tr.innerHTML += status? `<input data-work='id' type='hidden' value=${data[i].work_id}>
                                <input data-work='type' type='hidden' value=${data[i].work_type}>
                                <input data-work='status' type='hidden' value=${data[i].work_status}>` : ''
                    }

                    // paging.init()
                }else{
                    if (user_group_id == "-") {
                        workViewTable.innerHTML = `<tr><td colspan='7'>검색 결과가 없습니다.</td></tr>`
                    }else{
                        workViewTable.innerHTML = `<tr><td colspan='6'>검색 결과가 없습니다.</td></tr>`
                    }
                }
           }
            paging(page);
        },
        error: function(err){
            alert('저장 실패')
        }
    })
}

var dbinfo
//pathname 에 따라 페이지 설정해주기

//a , j, k, r4, l, i,
function statusButton(val){
    var condition = [dbinfo['status_work_deagi'], dbinfo['status_1cha_companion_cansel'], dbinfo['status_2cha_companion_cansel'], dbinfo['status_job_cansel'], dbinfo['status_3cha_companion_cansel'], dbinfo['status_complet']]

    if(condition.indexOf(val) == -1){
        return true
    }else{
        return false
    }
}

function group(group){
    var array_1 = ['tbit', 'dtw', 'gjac']
    var array_2 = ['으뜸정보기술', '디투리소스', '광주 인공지능센터']
    return array_2[array_1.findIndex(arr => arr == group)]
}

/*
        {% if item.work_status == "B" or item.work_status == "R1"  %}
        <td>{{item.worker_name1}}</td>
        {% elif item.work_status == "D" or item.work_status == "R2" %}
        <td>{{item.worker_name2}}</td>
        {% elif item.work_status == "F" or item.work_status == "R3" %}
        <td>{{item.worker_name3}}</td>
        {% elif item.work_status == "H" or item.work_status == "R4" %}
        <td>{{item.worker_name4}}</td>
        {% else %}
        <td>-</td>
*/

function userByStatus(status){

    switch(status){
        case dbinfo['status_work_run'] || dbinfo['status_1cha_companion_return']:
            return 1
            break
        case dbinfo['status_1cha_companion_return'] || dbinfo['status_2cha_companion_return']:
            return 2
            break
        case dbinfo['status_2cha_inspect_run'] ||  dbinfo['status_3cha_companion_return']:
            return 3
            break
        case dbinfo['status_3cha_inspect_run'] || dbinfo['status_job_cansel']:
            return 4
            break
        case undefined:
            break
    }
}

function paging(page){

    $(".paging").empty();
    let tot_cnt = $("#postLength").val();
    console.log(tot_cnt)
    let pageSize = 10;
    //가장 큰 수를 반환
    let pageTotNum = Math.floor(tot_cnt/pageSize) + (tot_cnt%pageSize > 0 ? 1 : 0);
    let pageStr = "<ul class = \"pageTable start\">";
    let startPage = Math.floor(page/pageSize);
    startPage = startPage*pageSize;
    let endPage = startPage + pageSize;
    endPage = endPage > pageTotNum ? pageTotNum : endPage;
    let prevPageSet = ((Math.floor(page/pageSize)*pageSize)-1) >= 0 ? ((Math.floor(page/pageSize)*pageSize)-1) : page;
    let nextPageSet = (Math.floor((page+pageSize)/pageSize)*pageSize) >= pageTotNum ? (pageTotNum - 1) : (Math.floor((page+pageSize)/pageSize)*pageSize);
    let prevPage = (page - 1) >= 0 ? (page - 1) : page;
    let nextPage = (page + 1) >= pageTotNum ? (pageTotNum - 1) : (page + 1);

    pageStr += "<li><a class=\"first\" href='#' onclick='jsf_ajax_dataloading(0)' \">처음</a></li>";
    pageStr += "<li><a class=\"prev\" href='#' onclick='jsf_ajax_dataloading(" + prevPageSet + ")' \"><<</a></li>";
    pageStr += "<li><a class=\"prevPageSet\" href='#' onclick='jsf_ajax_dataloading(" + prevPage + ")' \"><</a></li>";
    for(var i = startPage; i < endPage; i ++){
        if (page == i){
            pageStr += "<li><a class=\"active num\" href='#' onclick='jsf_ajax_dataloading(" + i + ")'\">"+ (i+1) +"</a></li>";
        }else{
            pageStr += "<li><a class=\"num\" href='#' onclick='jsf_ajax_dataloading(" + i + ")'\">"+ (i+1) +"</a></li>";
        }
    }
    pageStr += "<li><a class=\"next\" href='#' onclick='jsf_ajax_dataloading(" + nextPage + ")'\">></a></li>"
    pageStr += "<li><a class=\"nextPageSet\" href='#' onclick='jsf_ajax_dataloading(" + nextPageSet + ")'\">>></a></li>"
    pageStr += "<li><a class=\"last\" href='#' onclick='jsf_ajax_dataloading(" + (pageTotNum - 1) + ")'\">끝</a></li>"
    pageStr += "</ul>"
    $(".paging").html(pageStr);
}
}


function showData(search, data){

    switch(search){
        case 'product':
            const productEl = document.querySelectorAll('.selected-product ul')[1]

            data.forEach(data => {
                const li = document.createElement('li')
                li.append(data)
                productEl.append(li)
            })

        break

        case 'worker':
            const workerEl = document.querySelectorAll(`.selected-workman ul`)[1]

            data.forEach(data => {
                const li = document.createElement('li')
                li.append(data)
                workerEl.append(li)
            })

        // default:
    }
}

const inputChangeCheck = document.querySelector('#inputChangeCheck')
const inputChangeTr = document.querySelectorAll('#inputChangeCheck tr')
const inputChangeBtn = document.querySelectorAll('#inputChangeCheck tr .save-value')

inputChangeCheck.addEventListener('click', function(e){
    if(e.target.className.indexOf('save-value') !== -1){
        e.preventDefault()
        let value = []
        // let tr = document.querySelector(e.target.parentNode)
        for(let i=0; i<inputChangeBtn.length; i++){
            if(e.target === inputChangeBtn[i]){
                for(let j=0; j<inputChangeTr[i].children.length; j++){
                    if(inputChangeTr[i].children[j].querySelector('input')){
                        if(inputChangeTr[i].children[j].querySelector('input[type="checkbox"]')){
                            value.push(inputChangeTr[i].children[j].querySelector('input').checked)
                        }else{
                            value.push(inputChangeTr[i].children[j].querySelector('input').value)
                        }
                    }
                }
            }
        }

        var param = {
            worker: value[0],
            worker_id: value[1],
            workAuth: value[2],
            inspectAuth: value[3],
            adminAuth: value[4]
        }

        $.ajax({
            type: 'post',
            url: '/admin/index/userAuth/change_auth',
            data : JSON.stringify(param),
            success: function(data){
                if(data === 'True'){
                    alert('저장 성공')
                }else{
                    alert('저장 실패')
                }
            },
            error: function(err){
                alert('저장 실패')
            }
        })
    }
})

let searchData = {
    workerNm: '',
    workType: '',
    workStatus: '',
    searchBgn: '',
    searchEnd: '',
    groupId: ''
}


