country_select_id = typeof COUNTRY_SELECT_ID !== 'undefined' ? COUNTRY_SELECT_ID : 'id_country';

var country_select = document.getElementById(country_select_id);
country_select.status = false;

// display countries name and calling code
country_select.addEventListener('mousedown', function () {
  if (!this.status) {
    Array.prototype.forEach.call(this.options, function(option) {
      option.text = option.getAttribute('name') + ' (' + option.getAttribute('calling_code') + ')';
    });
    this.status = true;
  }
});

// display only countries calling code
country_select.addEventListener('mouseout', function () {
  if (this.status) {
    Array.prototype.forEach.call(this.options, function(option) {
      option.text = option.getAttribute('calling_code');
    });
    this.status = false;
  }
});

// display only countries calling code
country_select.addEventListener('change', function () {
  if (this.status) {
    Array.prototype.forEach.call(this.options, function(option) {
      option.text = option.getAttribute('calling_code');
    });
    this.status = false;
  }
});
