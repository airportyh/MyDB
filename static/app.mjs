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
    function editNextCell(td) {
        console.log('editNextCell', td);
        if (td.nextSibling) {
            const newTd = td.nextSibling;
            const column = newTd.column;
            const row = newTd.row;
            openInlineTextEditor(newTd, column, row, db, tableName, editNextCell, editPreviousCell);
        } else {
            // look at next row
            const tr = td.parentNode;
            if (tr.nextSibling) {
                const td = tr.nextSibling.firstChild;
                // TODO: generic check for primary ID
                if (td) {
                    const newTd = td.nextSibling;
                    const column = newTd.column;
                    const row = newTd.row;
                    openInlineTextEditor(newTd, column, row, db, tableName, editNextCell, editPreviousCell);
                }
            }
        }
    }
    function editPreviousCell(td) {
        // if (!td.previousSibling) {
        //     return;
        // }
        // let newTd = td.previousSibling;
        // let column = newTd.column;
        // let row = newTd.row;
        // if (column.name !== 'id') {
        //     openInlineTextEditor(newTd, column, row, db, tableName, editNextCell, editPreviousCell);
        // } else {    
        //     // look at previous row
        //     const tr = td.parentNode;
        //     if (tr.nextSibling) {
        //         const td = tr.nextSibling.firstChild;
        //         // TODO: generic check for primary ID
        //         if (td) {
        //             const newTd = td.nextSibling;
        //             const column = newTd.column;
        //             const row = newTd.row;
        //             openInlineTextEditor(newTd, column, row, db, tableName, editNextCell, editPreviousCell);
        //         }
        //     }
        // }
    }
    table.appendChild(el.thead(headerRow));
    const tbody = el.tbody();
    for (const row of rows) {
        const tr = el.tr();
        for (const column of columns) {
            const td = createDataCell(row, column, db, tableName, editNextCell, editPreviousCell);
            tr.appendChild(td);
        }
        tbody.appendChild(tr);
    }
    table.appendChild(tbody);
    page.appendChild(table);
    page.appendChild(el.button({
        onClick: async e => {
            await addRow(tbody, columns, db, tableName, editNextCell, editPreviousCell);
        }
    }, 'Add row'));
    root.appendChild(page);
}

async function addRow(tbody, columns, db, tableName, editNextCell, editPreviousCell) {
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
        tr.appendChild(createDataCell(row, column, db, tableName, editNextCell, editPreviousCell));
    }
    tbody.appendChild(tr);
}

function createDataCell(row, column, db, tableName, editNextCell, editPreviousCell) {
    const td = el.td({
        class: column.name == 'id' ? 'read-only' : '',
        onDblClick: () => {
            if (column.name === 'id') {
                return;
            }
            openInlineTextEditor(td, column, row, db, tableName, editNextCell, editPreviousCell);
        }
    }, row[column.name]);
    td.column = column;
    td.row = row;
    return td;
}

function openInlineTextEditor(td, column, row, db, tableName, editNextCell, editPreviousCell) {
    const value = td.textContent;
    td.innerHTML = '';
    const textInput = el.input({
        type: 'text',
        value,
        name: column.name,
        onKeypress: async e => {
            console.log('keypress', e);
            if (e.key === 'Enter') {
                await saveAndClose();
            }
        },
        onKeydown: async e => {
            console.log('keydown', e);
            if (e.key === 'Tab') {
                e.preventDefault();
                if (e.shiftKey) {
                    editPreviousCell(td);
                } else {
                    await saveAndClose();
                    editNextCell(td);
                }
            } else if (e.key === 'Escape') {
                // cancel
                textInput.remove();
                td.appendChild(text(row[column.name]));
            }
        }
    });
    td.appendChild(textInput);
    setTimeout(() => {
        textInput.focus();
        textInput.select();
    });
    
    async function saveAndClose() {
        textInput.remove();
        row[column.name] = textInput.value;
        const resp = await fetch(`/databases/${db}/tables/${tableName}/rows/${row.id}`, {
            method: 'PUT',
            body: JSON.stringify({
                columns: [column.name],
                values: [row[column.name]]
            })
        });
        const reply = await resp.json();
        if (reply.updated) {
            // TODO: error handling
            td.appendChild(text(row[column.name]));
        }
    }
}