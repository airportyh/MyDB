import el from './el.mjs';

export function List({ items, render, onSelect }) {
    const ul = el.ul({ class: 'list' });
    for (const item of items) {
        const li = el.li(
            render(item)
        );
        ul.appendChild(li);
        li.addEventListener("click", (e) => {
            onSelect(item, e);
        });
    }
    return ul;
}