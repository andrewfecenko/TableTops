var validate_form = {
	add_space: [
		{
			id: 'name',
			error: "The field 'name' was not filled out."
		},
		{
			id: 'description',
			error: "The field 'description' was not filled out."
		},
		{
			id: 'address',
			error: "The field 'address' was not filled out.",
		},
		{
			id: 'city',
			error: "The field 'city' was not filled out."
		},
		{
			id: 'country',
			error: "The field 'country' was not filled out."
		},
		{
			id: 'units',
			error: "The number of total units not entered.",
			validator: function(val) {
				try {
					val = parseInt(val);
					return val > 0;
				} catch (e) {
					return false;
				}
			}
		},
		{
			id: 'price',
			error: "A valid price must be entered.",
			validator: function(val) {
				try {
					val = parseFloat(val);
					return val >= 0;
				} catch (e) {
					return false;
				}
			}
		},
		{
			id: 'lat',
			error: "Please pin the location on the map.",
			validator: function(val) {
				try {
					val = parseFloat(val);
					return (val <= 90.0 && val >= -90.0);
				} catch (e) {
					return false;
				}
			}
		},
		{
			id: 'lon',
			error: "Please pin the location on the map.",
			validator: function(val) {
				try {
					val = parseFloat(val);
					return (val <= 180.0 && val >= -180.0);
				} catch (e) {
					return false;
				}
			}
		}
	]
}

function validateForm(name) {
	var validate_fields = validate_form[name];
	if (validate_fields) {
		for (var i = 0; i < validate_fields.length; i++) {
			var field = validate_fields[i];
			try {
				var val = document.getElementById(field.id).value.trim();
				if (!val) {
					alert(field.error);
					return false;
				} else if (field.validator && !field.validator(val)) {
					alert(field.error);
					return false;
				}
			} catch (e) {
				alert(field.error);
				return false;
			}
		}
	}
	return true;
}