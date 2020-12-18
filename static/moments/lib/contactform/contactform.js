    jQuery(document).ready(function($){

	$('form#contactForm').submit(function() {
		$('form#contactForm .error').css({"display":"none"});
		var hasError = false;
		$('.requiredField').each(function() {
			if(jQuery.trim($(this).val()) == '') {
				var labelText = $(this).prev('label').text();
				$(this).parent().find('.error').css({"display":"block"});
				hasError = true;
			} else if($(this).hasClass('email')) {
				var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
				if(!emailReg.test(jQuery.trim($(this).val()))) {
					var labelText = $(this).prev('label').text();
					$(this).parent().find('.error').css({"display":"block"});
					hasError = true;
				}
			}
		});
		if(!hasError) {
			var formInput = $(this).serialize();
			$.post($(this).attr('action'),formInput, function(data){
				$('form#contactForm').slideUp("fast", function() {
					$('.thanks').css({"display":"block"});
				});
			});
		}
		  return false;

	});
});