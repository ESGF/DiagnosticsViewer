function cross(a) {
  return function(d, i) {
    var c = [];
    for (var j = 0, n = a.length; j < n; j++) c.push({x: d, y: a[j], i: i});
    return c;
  };
}
