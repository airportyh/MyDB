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
import { DataTable } from './data_table.mjs';

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
    const table = new DataTable(db, tableName);
    root.appendChild(table);
}