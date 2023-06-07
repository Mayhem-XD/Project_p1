/*!
* Start Bootstrap - Simple Sidebar v6.0.6 (https://startbootstrap.com/template/simple-sidebar)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-simple-sidebar/blob/master/LICENSE)
*/
// 
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }
        // 버튼 클릭 시 datepicker가 나타나도록 이벤트 리스너 추가
    document.getElementById('button1').addEventListener('click', function() {
        showDatePicker('datepickerContainer', '날짜1');
    });
    
    document.getElementById('button2').addEventListener('click', function() {
        showDatePicker('datepickerContainer', '날짜2');
    });
    
    // datepicker 생성 함수
    function showDatePicker(containerId, dateLabel) {
        // 이전에 생성된 datepicker가 있다면 삭제
        var container = document.getElementById(containerId);
        while (container.firstChild) {
        container.removeChild(container.firstChild);
        }
    
        // datepicker 요소 생성
        var datePicker = document.createElement('input');
        datePicker.type = 'date';
    
        // 선택한 날짜가 변경되었을 때 이벤트 처리
        datePicker.addEventListener('change', function() {
        var selectedDate = datePicker.value;
        alert(dateLabel + ': ' + selectedDate);
        // 여기에서 원하는 추가 동작을 수행할 수 있습니다.
        });
    
        // datepicker 요소를 컨테이너에 추가
        container.appendChild(datePicker);
    }
    


});
