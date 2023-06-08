function send(){
    let line = $('#input_line').val();
    let target = $('#input_target').val()
    let sm = $('#button1').val()
    let em = $('#button2').val()
    $.ajax({
        type: 'POST',
        url: '/heatmap',
        data: {addr:addr,line:line,target:target,sm:sm,em:em},
        success: function(msg){
            $('#addr').html(msg);
        }

    });
}

function send_info() {
    let target = $('#input_target').val();
    let cat = $("input[name = 'cat']:checked").val();
    $.ajax({
        type: 'POST',
        url: '/tour',
        data: {target: target, cat: cat},
        success: function(show) {
            $('#showmap').attr({"src": "{{url_for('static',filename='img/station.html')}}"});
        }
    });
}