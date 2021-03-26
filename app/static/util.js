Math.randomRange = (min, max) => {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min)) + min;
}

HTMLElement.prototype.empty = function() {
    this.innerHTML = '';
}

HTMLElement.prototype.find = function(query) {
    return find(this, query);
}

HTMLElement.prototype.on = function(event, cb) {
    this.addEventListener(event, cb);
}

if (!HTMLElement.prototype.remove) {
    HTMLElement.prototype.remove = function () {
        this.parentNode.removeChild(this);
    }
}

Array.prototype.groupBy = function(groupKey) {
	return this.reduce(function (obj, item) {
		var key = item[groupKey];
		if (!obj.hasOwnProperty(key)) {
			obj[key] = [];
		}

		obj[key].push(item);

		return obj;
	}, {});
};

$ = (query) => find(document, query);

const find = (root, query) => {
    var nodes = root.querySelectorAll(query);
    if (nodes.length === 1) {
        return nodes[0];
    }
    else return nodes;
}

function render(data, id) {
	var template = document.getElementById(id).innerHTML;
	var tokens = template.match(/\{\{([a-zA-Z\d:\-_]+)\}\}/g)
    
	for (var x = 0; x < tokens.length; x++) {
		var prop = tokens[x].slice(2, tokens[x].length - 2)
		  , val = '';
			
		if (data.hasOwnProperty(prop)) {
			val = data[prop];
		}
		else {
			var subtemplate = prop.split(':');
			if (subtemplate.length == 3) {
				var d = data[subtemplate[1]];
				for (var i = 0; i < d.length; i++) {
					val += render(d[i], subtemplate[2]);
				}
			}
		}
		
		template = template.split(tokens[x]).join(val);
	}

	return template;
}