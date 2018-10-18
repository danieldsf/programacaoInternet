console.log("KK eae man");

const apikey = 'AsusOpTRqTWOEofnjP3O9z';
const client = filestack.init(apikey);

$('#id_thumb').attr('readonly', true);

$('#id_thumb').click(function(){
	client.pick({
	  maxFiles: 1,
	  uploadInBackground: false,
	  onOpen: () => console.log('opened!'),
	})
	.then((res) => {
	  console.log(res.filesUploaded)
	  //
	  
	  $(this).val(res.filesUploaded[0].url)

	  console.log(res.filesFailed)
	});
});

$(document).ready(function() {
	$('#id_contents').select2();
	$('#id_expiration_date').datepicker();
});