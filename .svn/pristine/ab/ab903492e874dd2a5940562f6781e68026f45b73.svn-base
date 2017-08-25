function updateQueryStringParameter(uri, key, value) {
  var re = new RegExp("([?&])" + key + "=.*?(&|$)", "i");
  var separator = uri.indexOf('?') !== -1 ? "&" : "?";
  if (uri.match(re)) {
    return uri.replace(re, '$1' + key + "=" + value + '$2');
  }
  else {
    return uri + separator + key + "=" + value;
  }
}


$("input[name=Order]").focusout(function(){
	if ($(this).val() == "Title (A-Z)") {
		redirect_uri = updateQueryStringParameter(document.URL, "order", "asce");
		redirect_uri = updateQueryStringParameter(redirect_uri, "order_type", "name");
	}
	if ($(this).val() == "Title (Z-A)") {
		redirect_uri = updateQueryStringParameter(document.URL, "order", "desc");
		redirect_uri = updateQueryStringParameter(redirect_uri, "order_type", "name");
	}
	if ($(this).val() == "Date (Older-Newer)") {
		redirect_uri = updateQueryStringParameter(document.URL, "order", "desc");
		redirect_uri = updateQueryStringParameter(redirect_uri, "order_type", "date");
	}
	if ($(this).val() == "Date (Newer-Older)") {
		redirect_uri = updateQueryStringParameter(document.URL, "order", "asce");
		redirect_uri = updateQueryStringParameter(redirect_uri, "order_type", "date");
	}
    window.location.href = redirect_uri;
});

$("input[name=MadeBys]").focusout(function(){
	if ($(this).val() == "Anyone") {
		redirect_uri = updateQueryStringParameter(document.URL, "owner_spaces", "false");
	}
	if ($(this).val() == "Me") {
		redirect_uri = updateQueryStringParameter(document.URL, "owner_spaces", "true");
	}
    window.location.href = redirect_uri;
});

$("input[name=Intrests]").focusout(function(){
	redirect_uri = updateQueryStringParameter(document.URL, "tags", $(this).val());
    window.location.href = redirect_uri;
});