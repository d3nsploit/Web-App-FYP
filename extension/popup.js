
function transfer(){	
	var tablink;

	chrome.tabs.getSelected(null,function(tab) {

		tablink = tab.url;

		var xhr=new XMLHttpRequest();
		params="url="+tablink;
        // alert(params);
		var markup = "url="+tablink+"&html="+document.documentElement.innerHTML;
		xhr.open("POST","http://localhost:5000/scan/extension",false);
		xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
		xhr.send(markup);
		// Uncomment this line if you see some error on the extension to see the full error message for debugging.
        // alert(xhr.responseText);		

		var x = JSON.parse(xhr.responseText);  
		$('#loader').attr("id","stylo");
		if (x === 'benign'){
			$(".text").css('color','#05e650');
			$(".image").css('background-image','url("data:image/png;base64,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")');

		}
		else{
			$(".text").css('color','#e71111');
			$(".image").css('background-image','url("data:image/png;base64,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")');

		}
		$(".text").text(x);



		return xhr.responseText;
	});
}


$(document).ready(function(){
    $(".btn").click(function(){	
		$('#stylo').attr("id","loader");
		transfer();
    });
});

chrome.tabs.getSelected(null,function(tab) {
	var tablink = tab.url;
 $("#p2").text(tablink);
});