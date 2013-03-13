function test_ajax(postId) {
	$('#post' + postId).hide();
	$('#loading' + postId).show();
	$.post('/ajax',{
		text:'Send form Client\n'
	}).done(function(response){
		$('#post' + postId).text(response['text'] + 'Back into Client again! \n').show()
		$('#loading' + postId).hide()

	}).fail(function(){
		$('#post' + postId).text('Error!').show()
		$('#loading' + postId).hide()
	});
}