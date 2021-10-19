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

const tableSortingButton01 = document.querySelector('#table-tab-01 thead tr')
tableSortingButton01.addEventListener('click', function(e){
    if(!e.target.dataset.number) return
    tableTab01.sorting(e.target.dataset.number)
})

const tableSortingButton02 = document.querySelector('#table-tab-02 thead tr')
tableSortingButton02.addEventListener('click', function(e){
    if(!e.target.dataset.number) return
    tableTab02.sorting(e.target.dataset.number)
})

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
//프로토 타입은 변수 공유 안하나? <- 구조 분해 할당은 담아서 쓰는 건지
//디스 값 변경을 하지 않는듯(?)

const searchTable = document.querySelector('#table-tab-01')

searchTable.addEventListener('click', (e) => {
    let { target } = e
    if(target.nodeName !== 'BUTTON') return
    if(target.dataset.search !== 'product') return
    
    var productName = e.target.innerText
    console.log(productName)
    if(target.dataset.search){
        console.log(target.dataset.search)
        $.ajax({
            type: 'post',
            url: 'product_data',
            data : {'product': productName },

            success: function(data){
                const _productName = document.querySelector('#ProductName'),
                workStatus = document.querySelector('#workStatus'),
                worker = document.querySelector('#worker'),
                inspectionStatus = document.querySelector('#inspectionStatus'),
                inspecter = document.querySelector('#inspecter')

                console.log(data)
                console.log('Success: ' + data.tasker_id)
                console.log('Success: ' + data.inspector_id)
                console.log('Success: ' + data.task_process)
                console.log('Success: ' + data.inspect_process)

                _productName.innerText = productName
                workStatus.innerText = data.task_process
                worker.innerText = data.tasker_id
                inspectionStatus.innerText = data.inspect_process
                inspecter.innerText = data.inspector_id

                // showData(target.dataset.search, data)
            },
            error: function(err){
                console.log(err)
            }
        })
    }
})


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
            url: 'change_auth',
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

var searchForm = document.forms.searchForm

searchForm.addEventListener('submit', e => {
    e.preventDefault()
    var { workerNm, workType, workStatus, searchBgn, searchEnd, workGroup } = searchForm

    console.log(workerNm.value, workType.value, workStatus.value, searchBgn.value, searchEnd.value)

    let data = {
        workerNm: workerNm.value,
        workType: workType.value,
        workStatus: workStatus.value,
        searchBgn: searchBgn.value,
        searchEnd: searchEnd.value,
        groupId: workGroup.value
    }

    console.log(data)

    $.ajax({
        type: 'post',
        url: 'get_search_data',
        data : JSON.stringify(data),
        success: function(data){
            console.log(data)
           if(data.messages == 'false'){
            alert('검색 조건을 입력하세요.')
           }else{
            var workViewTable = document.querySelector('.workViewTable')

                if(data.length != 0){

                    workViewTable.innerHTML = ''
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
                            <td>${data[i].str_status? data[i].str_status: '-'}</td>
                            <td>${group_id? group_id: '-'}</td>
                            <td>${status? '<button data-work="admin_work_view">작업보기</button>' : '-'}</td>
                            <td>${data[i].reg_date? data[i].reg_date.split('T')[0]: '-'}</td>`

                        tr.innerHTML += status? `<input data-work='id' type='hidden' value=${data[i].work_id}>
                                <input data-work='type' type='hidden' value=${data[i].work_type}>
                                <input data-work='status' type='hidden' value=${data[i].work_status}>` : ''
                    }
                }else{
                    workViewTable.innerHTML = `<tr><td colspan='7'>검색 결과가 없습니다.</td></tr>`
                }
           }
        },
        error: function(err){
            alert('저장 실패')
        }
    })
})

//a , j, k, r4, l, i,
function statusButton(val){
    var condition = ['A', 'J', 'K', 'R4', 'L', 'I']

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
        case 'B' || 'R1':
            return 1
            break
        case 'D' || 'R2':
            return 2
            break
        case 'F' || 'R3':
            return 3
            break
        case 'H' || 'R4':
            return 4
            break
        case undefined:
            break
    }
}