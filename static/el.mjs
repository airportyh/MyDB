const el = (() => {
    const el = {};
    const elements = [
        'div', 'ul', 'li', 'ol', 'a', 'h1', 'h2', 'h3', 'h4', 'h5',
        'style', 'textarea', 'form', 'input', 'label', 'button',
        'img', 'br', 'span', 'section', 'p', 'table', 'thead', 'tbody', 'tr', 'th', 'td'
    ];
    for (let e of elements) {
        el[e] = curry(element, e);
    }
    return el;
})();

function isObject(thing) {
    return thing !== null && typeof thing === 'object';
}

function isPlainObject(thing) {
    return isObject(thing) && thing.__proto__ === Object.prototype;
}

function isString(thing) {
    return typeof thing === 'string'
}

function isElement(thing) {
    return thing instanceof HTMLElement;
}

export function element(tag, attrs, ...children) {
    const elm = document.createElement(tag);
    if (attrs !== undefined && !isPlainObject(attrs)) {
        children.splice(0, 0, attrs);
    } else if (isObject(attrs)) {
        for (let attr in attrs) {
            if (attr === 'style') {
                applyStyles(elm, attrs[attr]);
                continue;
            }
            if (attr.startsWith('on')) {
                const event = attr.substring(2).toLowerCase();
                elm.addEventListener(event, attrs[attr]);
                continue;
            }
            elm.setAttribute(attr, attrs[attr]);
        }    
    }
    for (let child of children) {
        if (isElement(child)) {
            elm.appendChild(child);
        } else if (child === null) {
            elm.appendChild(text(''));
        } else {
            elm.appendChild(text(String(child)));
        }
    }
    return elm;
}

export function applyStyles(elm, styles) {
    if (!styles) {
        return;
    }

    if (isString(styles)) {
        elm.setAttribute('style', styles);
    }
    
    for (let key in styles) {
        elm.style[key] = styles[key];
    }
}

export function text(content) {
    const textNode = document.createTextNode(content);
    return textNode;
}

function curry(fn, ...args) {
    return (...restArgs) => {
       return fn(...args, ...restArgs); 
    };
}

export default el;



