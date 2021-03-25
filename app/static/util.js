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
