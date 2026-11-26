/* Mini-Laufzeit: rendert die DC-Vorlagen (Holes, sc-if, sc-for, Events) mit DOM-Abgleich */
function DCLogic(props) { this.props = props || {}; this.state = this.state || {}; }
DCLogic.prototype.setState = function (p) {
  var u = typeof p === 'function' ? p(this.state, this.props) : p;
  this.state = Object.assign({}, this.state, u || {});
  this.__schedule && this.__schedule();
};
DCLogic.prototype.forceUpdate = function () { this.__schedule && this.__schedule(); };

var DC = (function () {
  var HOLE = /\{\{([^}]+)\}\}/g, WHOLE = /^\s*\{\{([^}]+)\}\}\s*$/;
  function look(path, scope) {
    path = path.trim();
    if (path === 'true') return true; if (path === 'false') return false;
    if (/^-?\d+(\.\d+)?$/.test(path)) return +path;
    if (/^'.*'$/.test(path)) return path.slice(1, -1);
    var parts = path.split('.'), v;
    for (var i = scope.length - 1; i >= 0; i--) { if (scope[i] && parts[0] in scope[i]) { v = scope[i][parts[0]]; break; } }
    for (var k = 1; k < parts.length; k++) v = v == null ? undefined : v[parts[k]];
    return v;
  }
  function interp(str, scope) { return str.replace(HOLE, function (_, p) { var v = look(p, scope); return v == null ? '' : String(v); }); }
  function build(node, scope, out) {
    if (node.nodeType === 3) { out.push({ text: node.data.indexOf('{{') >= 0 ? interp(node.data, scope) : node.data }); return; }
    if (node.nodeType !== 1) return;
    var tag = node.localName;
    if (tag === 'sc-if') {
      var a = node.getAttribute('value') || '', m = a.match(WHOLE);
      if (m ? look(m[1], scope) : a) kids(node, scope, out);
      return;
    }
    if (tag === 'sc-for') {
      var lm = (node.getAttribute('list') || '').match(WHOLE), list = lm ? look(lm[1], scope) : null, as = node.getAttribute('as') || 'item';
      (list || []).forEach(function (it, i) { var o = { $index: i }; o[as] = it; kids(node, scope.concat([o]), out); });
      return;
    }
    if (tag === 'dc-import') return;
    var v = { tag: tag, ns: node.namespaceURI, attrs: {}, on: {}, children: [] };
    for (var i = 0; i < node.attributes.length; i++) {
      var at = node.attributes[i], n = at.name, val = at.value;
      if (n.indexOf('hint-') === 0) continue;
      var wm = val.match(WHOLE);
      if (/^on/i.test(n) && wm) { var f = look(wm[1], scope); if (typeof f === 'function') v.on[n.slice(2).toLowerCase()] = f; continue; }
      var r = wm ? look(wm[1], scope) : (val.indexOf('{{') >= 0 ? interp(val, scope) : val);
      if (r === false || r == null) continue;
      v.attrs[n] = r === true ? '' : String(r);
    }
    kids(node, scope, v.children);
    out.push(v);
  }
  function kids(node, scope, out) { for (var c = node.firstChild; c; c = c.nextSibling) build(c, scope, out); }
  function create(v) {
    if (!v.tag) return document.createTextNode(v.text);
    var el = v.ns && v.ns !== 'http://www.w3.org/1999/xhtml' ? document.createElementNS(v.ns, v.tag) : document.createElement(v.tag);
    update(el, v); return el;
  }
  function same(el, v) { return v.tag ? (el.nodeType === 1 && el.localName === v.tag) : el.nodeType === 3; }
  function update(el, v) {
    if (!v.tag) { if (el.data !== v.text) el.data = v.text; return; }
    var cur = el.attributes;
    for (var i = cur.length - 1; i >= 0; i--) if (!(cur[i].name in v.attrs)) el.removeAttribute(cur[i].name);
    for (var n in v.attrs) if (el.getAttribute(n) !== v.attrs[n]) el.setAttribute(n, v.attrs[n]);
    if ('value' in v.attrs && (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') && el.value !== v.attrs.value) el.value = v.attrs.value;
    el.__on = v.on; el.__bound = el.__bound || {};
    for (var t in v.on) if (!el.__bound[t]) { el.__bound[t] = 1; (function (type) { var ev = type === 'change' && (el.tagName === 'TEXTAREA' || (el.tagName === 'INPUT' && el.type !== 'checkbox' && el.type !== 'radio')) ? 'input' : type; el.addEventListener(ev, function (e) { var h = el.__on && el.__on[type]; if (h) h(e); }); })(t); }
    patch(el, v.children);
  }
  function patch(parent, list) {
    for (var i = 0; i < list.length; i++) {
      var el = parent.childNodes[i], v = list[i];
      if (el && same(el, v)) update(el, v);
      else { var n = create(v); if (el) parent.replaceChild(n, el); else parent.appendChild(n); }
    }
    while (parent.childNodes.length > list.length) parent.removeChild(parent.lastChild);
  }
  function mount(Comp, tplRoot, host) {
    var inst = new Comp({}), queued = false, mounted = false;
    function render() {
      queued = false;
      var vals; try { vals = inst.renderVals() || {}; } catch (e) { console.error(e); return; }
      var out = []; build(tplRoot, [vals], out); patch(host, out);
      if (!mounted) { mounted = true; if (inst.componentDidMount) try { inst.componentDidMount(); } catch (e) { console.error(e); } }
    }
    inst.__schedule = function () { if (!queued) { queued = true; Promise.resolve().then(render); } };
    render();
    return inst;
  }
  return { mount: mount };
})();
