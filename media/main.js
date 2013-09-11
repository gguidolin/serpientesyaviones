$('#loader1').click(function(){
	$(this).hide('slow', function(){
		$('#loader1Callback li').show('slow');
	});
});