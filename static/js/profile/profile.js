$(document).ready(function(){

	$('#eeb').click(function(){
		$('#email_edit').css('display', 'block');
		$('#ecb').css('display', 'block');
		$('#eeb').css('display', 'none');

	});

	$('#feb').click(function(){
		$('#first_edit').css('display', 'block');
		$('#fcb').css('display', 'block');
		$('#feb').css('display', 'none');

	});

	$('#leb').click(function(){
		$('#last_edit').css('display', 'block');
		$('#lcb').css('display', 'block');
		$('#leb').css('display', 'none');

	});

	$('#ecb').click(function(){
		$('#email_edit').css('display', 'none');
		$('#ecb').css('display', 'none');
		$('#eeb').css('display', 'block');

	});

	$('#fcb').click(function(){
		$('#first_edit').css('display', 'none');
		$('#fcb').css('display', 'none');
		$('#feb').css('display', 'block');

	});

	$('#lcb').click(function(){
		$('#last_edit').css('display', 'none');
		$('#lcb').css('display', 'none');
		$('#leb').css('display', 'block');

	});

	$('#predelete_account').click(function(){
		$(this).css('display', 'none');
		$('#sure').css('display', 'block');
		$('#delete_account').css('display', 'block');
		$('#cancel_delete').css('display', 'block');

	});

	$('#cancel_delete').click(function(){
		$(this).css('display', 'none');
		$('#sure').css('display', 'none');
		$('#delete_account').css('display', 'none');
		$('#predelete_account').css('display', 'block');

	});






});




