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