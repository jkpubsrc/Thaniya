var show = function(selector) {
	var elem = document.getElementById(selector);
	elem.style.display = 'inline-block';
};

var hide = function(selector) {
	var elem = document.getElementById(selector);
	elem.style.display = 'none';
};

var toggle = function(selector) {
	var elem = document.getElementById(selector);
	if (window.getComputedStyle(elem).display === 'inline') {
		elem.style.display = 'none';
		return false;
	} else {
		elem.style.display = 'inline';
		return true;
	}
};

var toggleInline = function(selector) {
	var elem = document.getElementById(selector);
	if (window.getComputedStyle(elem).display === 'inline-block') {
		elem.style.display = 'none';
		return false;
	} else {
		elem.style.display = 'inline-block';
		return true;
	}
};

var _buttonEvents = {};
document.addEventListener("click", function (event) {
	for (k in _buttonEvents) {
		if (event.target.matches(k)) {
			event.preventDefault();
			try {
				_buttonEvents[k](event);
			} catch (ee) {
				console.log(ee);
			}
		}
	}
}, false);

var registerEvent = function(identifier, callback) {
	_buttonEvents["." + identifier] = callback;
}

