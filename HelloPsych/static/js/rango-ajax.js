<script>
function check(){
	var req_id, textis;
    req_id = $(this).attr("data-req_id");
    textis = document.getElementById("docnotes").value;
    alert(textis);
    $.get('/vline/update_comments/', {req_id: req_id, textis: textis}, function(data){
      	alert('ok');
        });
    return;
}
</script>