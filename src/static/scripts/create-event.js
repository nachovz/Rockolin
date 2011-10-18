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

$(function() {
	$("table#table-songs").tablesorter({ sortList: [[1,0]] });
	//$("table#table-emails").tablesorter({ sortList: [[1,0]] });
});

$('.next-button').click(function() {
	var step = $('fieldset:regex(class,^step):not(:regex(css:display,none))').attr('class');

	switch(step){
		case "step1":
			if ($('.validate').validate().element('#name') && $('.validate').validate().element('#description') && $('.validate').validate().element('#image_upload') && $('.validate').validate().element('#start-date')) {	
				$('.'+step).fadeOut('fast').hide();
				$('.step2').fadeIn().show();
				$('.step2-circle').animate({opacity: 0.3, opacity : 1}, 1000);
				$('#start-date').val(formatDate($('#start-date-picker').val()));
				$('.back-button').show();
			}
		break;
		case "step2":
			if ($('.check-song').length - $('.check-song:unchecked').length != 0) {
				$('.'+step).fadeOut('fast').hide();
				$('.step3').fadeIn().show();
				$('.step3-circle').animate({opacity: 0.3, opacity : 1}, 1000);
				$('.next-button').hide();
				$('.create-button').css('display','inline-block');
			};
		break;
		case "step3":
			if (true) {	
				$('.'+step).fadeOut('fast').hide();
				$('.step2').fadeIn().show();
				$('.step2-circle').animate({opacity: 0.3, opacity : 1}, 1000);
			};
		break;
	}
});

$('.back-button').click(function() {
	var step = $('fieldset:regex(class,^step):not(:regex(css:display,none))').attr('class');

	switch(step){
		case "step2":
			$('.'+step).fadeOut('fast').hide();
			$('.step1').fadeIn().show();
			$('.step2-circle').animate({opacity: 1, opacity : 0.3}, 1000);
			$('.back-button').hide();
		break;
		case "step3":
			$('.'+step).fadeOut('fast').hide();
			$('.step2').fadeIn().show();
			$('.step3-circle').animate({opacity: 1, opacity : 0.3}, 1000);
			$('.create-button').hide();
		break;
	}
});

AnyTime.picker("start-date-picker",{ format: "%M %d, %Z at %h:%i%p", firstDOW: 1 });


$(".add-email-button").click(function(){
	if ($('.validate').validate().element('.email')) {
		addEmail();
	};
});

function addEmail(){
	var text = document.getElementById("add-email").value;	
	$('.contacts-header').show();
	$('#table-emails').append('<tr> <td><input type="checkbox" name="contacts[]" value="'+text+'" checked class="check-email"></td> <td><strong class="fn">'+text+'</strong></td></tr>');
	
	}
function formatDate(dateIn){
	var defaultConv = new AnyTime.Converter({
		format: "%M %d, %Z at %h:%i%p"
	});
	var date = defaultConv.parse(dateIn);
	
	var peluOut = new AnyTime.Converter({
		format:"%Y-%m-%d-%H-%i"
	});
	return peluOut.format(date);
}

function validateAndSend(){
	if ($('.check-email').length >= 1) {
		$('#create-form').submit();
	};
}
