jQuery.expr[':'].regex = function(elem, index, match) {
    var matchParams = match[3].split(','),
        validLabels = /^(data|css):/,
        attr = {
            method: matchParams[0].match(validLabels) ? 
                        matchParams[0].split(':')[0] : 'attr',
            property: matchParams.shift().replace(validLabels,'')
        },
        regexFlags = 'ig',
        regex = new RegExp(matchParams.join('').replace(/^\s+|\s+$/g,''), regexFlags);
    return regex.test(jQuery(elem)[attr.method](attr.property));
}

$('.next-button').click(function() {
	var step = $('fieldset:regex(class,^step):not(:regex(css:display,none))').attr('class');

	switch(step){
		case "step1":
			$('.'+step).fadeOut('fast').hide();
			$('.step2').fadeIn().show();
			$('.step2-circle').animate({opacity: 0.3, opacity : 1}, 1000);
		break;
		case "step2":
			$('.'+step).fadeOut('fast').hide();
			$('.step3').fadeIn().show();
			$('.step3-circle').animate({opacity: 0.3, opacity : 1}, 1000);
			$('.next-button').hide();
			$('.create-button').css('display','inline-block');
		break;
		case "step3":
			$('.'+step).fadeOut('fast').hide();
			$('.step2').fadeIn().show();
			$('.step2-circle').animate({opacity: 0.3, opacity : 1}, 1000);
		break;
	}
});
