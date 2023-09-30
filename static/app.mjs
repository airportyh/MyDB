/*
1. List DBs
2. Allow adding a DB
3. Allow removing a DB
2. Choose a DB and list tables
3. Choose a table and show a structure tab vs a data tab
4. Structure tab:
    * show columns
    * allow adding columns
    * allow deleting columns
    * allow modifying columns
*/

import el, { text } from './el.mjs';
import { List } from './ui.mjs';
import * as request from './request.mjs';

main().catch(console.error);

const root = document.body;

async function main() {
    await openSelectDBPage();
}

async function openSelectDBPage() {
    const databases = await request.get('/databases');
    const page = el.div({ class: 'page' },
        el.h1('Select a Database'),
        List({
            items: databases, 
            render: db => db,
            onSelect: async (db) => {
                root.removeChild(page);
                await openSelectTablePage(db);
            }
        })
    );
    root.appendChild(page);
}

async function openSelectTablePage(db) {
    const tables = await request.get(`/databases/${db}/tables`);
    const page = el.div({ class: 'page' },
        el.h1(db),
        List({
            items: tables,
            render: table => table,
            onSelect: table => {
                root.removeChild(page);
                openTableEditorPage(db, table);
            }
        })
    );
    root.appendChild(page);
}

async function openTableEditorPage(db, tableName) {
    const columns = await request.get(`/databases/${db}/tables/${tableName}/columns`);
    console.log('columns', columns);
    const rows = await request.get(`/databases/${db}/tables/${tableName}/rows`);
    console.log('rows', rows);
    const page = el.div({ class: 'page' },
        el.h1(`${db} > ${tableName}`)
    );
    const table = el.table({
        class: 'table', 
        border: 1,
        style: {
            width: '100%'
        }
    });
    const headerRow = el.tr();
    for (const column of columns) {
        headerRow.appendChild(
            el.th(
                {
                    title: column.type,
                    style: {
                        cursor: 'default'
                    }
                }, 
                column.name
            )
        );
    }
    table.appendChild(el.thead(headerRow));
    const tbody = el.tbody();
    for (const row of rows) {
        const tr = el.tr();
        for (const column of columns) {
            const td = el.td({
                class: column.name == 'id' ? 'read-only' : '',
                onDblClick: () => {
                    if (column.name === 'id') {
                        return;
                    }
                    td.innerHTML = '';
                    openInlineTextEditor(td, column, row, db, tableName);
                }
            }, row[column.name]);
            tr.appendChild(td);
        }
        tbody.appendChild(tr);
    }
    table.appendChild(tbody);
    page.appendChild(table);
    page.appendChild(el.button({
        onClick: async e => {
            const useColumns = columns
                .filter(column => column.name !== 'id');
            const values = Array(useColumns.length);
            const resp = await fetch(`/databases/${db}/tables/${tableName}/rows`, {
                method: 'POST',
                body: JSON.stringify({
                    columns: useColumns.map(column => column.name),
                    values
                })
            });
            // TODO: error handling
            const row = await resp.json();
            const tr = el.tr(el.td(row.id));
            for (const column of useColumns) {
                row[column.name] = null;
                const td = el.td({
                    class: column.name == 'id' ? 'read-only' : '',
                    onDblClick: () => {
                        if (column.name === 'id') {
                            return;
                        }
                        td.innerHTML = '';
                        openInlineTextEditor(td, column, row, db, tableName);
                    }
                }, row[column.name])
                tr.appendChild(td);
            }
            tbody.appendChild(tr);
        }
    }, 'Add row'));
    root.appendChild(page);
}

function openInlineTextEditor(td, column, row, db, tableName) {
    const textInput = el.input({
        type: 'text',
        value: td.textContent,
        name: column.name,
        onKeypress: async e => {
            if (e.key === 'Enter') {
                textInput.remove();
                row[column.name] = textInput.value;
                const resp = await fetch(`/databases/${db}/tables/${tableName}/rows/${row.id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        columns: [column.name],
                        values: [row[column.name]]
                    })
                });
                // TODO: error handling
                td.appendChild(text(row[column.name]));
            }
        },
        onKeydown: e => {
            if (e.key === 'Tab') {
                e.preventDefault();
            }
        }
    });
    td.appendChild(textInput);
    setTimeout(() => {
        textInput.focus();
        textInput.select();
    });
}