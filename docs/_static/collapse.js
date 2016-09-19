function collapse_dd(){
        if ($(this).hasClass('collapsed')) {
            $(this).removeClass('collapsed')
            $(this).children('dd').show('fast')
        } else {
            $(this).addClass('collapsed')
            $(this).children('dd').hide('fast')
        }
        return false;
    }
$(document).ready(function() {
    // $('dl.class > dd').hide()
    $('dl.class').click(collapse_dd)
    $('dl.attribute').click(collapse_dd)
    // $('dl.method > dd').hide()
    $('dl.method').click(collapse_dd)
    // $('div.section > dl.function > dd').hide()
    $('div.section > dl.function').click(collapse_dd)
 
    $('a').click(function(e) {
        e.stopPropagation();
    })
 
    if (window.location.hash.length != 0) {
        base = window.location.hash.replace(/\./g, '\\.');
        base = $(base);
        base.removeClass('collapsed');
        base.parents('dd').show();
        base.parents('dl').removeClass('collapsed');
        base.siblings('dd').show();
    }
});
