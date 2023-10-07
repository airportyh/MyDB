import el, { text } from './el.mjs';
import * as request from './request.mjs';

export class DataTable extends HTMLTableElement {
    constructor(db, tableName) {
        super();
        this.db = db;
        this.tableName = tableName;
        this.headerRow = el.tr();
        this.tbody = el.tbody();
        this.tableColumns = null;
        this.tableRows = null;
        
        this.initialize();
    }
    
    async initialize() {
        this.classList.add('table');
        this.setAttribute('border', 1);
        this.style.width = '100%';
        this.tableColumns = await request.get(`/databases/${this.db}/tables/${this.tableName}/columns`);
        this.tableRows = await request.get(`/databases/${this.db}/tables/${this.tableName}/rows`);
        
        const headerRow = el.tr();
        for (const column of this.tableColumns) {
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
        
        this.appendChild(el.thead(headerRow));
        
        
        for (const row of this.tableRows) {
            const tr = el.tr();
            for (const column of this.tableColumns) {
                const cell = new DataCell(row, column, this);
                tr.appendChild(cell);
            }
            this.tbody.appendChild(tr);
        }
        this.appendChild(this.tbody);
    }
    
    editNextCell(cell) {
        let nextCell = cell.nextSibling;
        if (nextCell) {
            nextCell.openEditor();
        } else {
            // look at next row
            let row = cell.parentNode;
            let nextRow = row.nextSibling;
            // TODO: don't edit primary key
            if (nextRow) {
                let firstCell = nextRow.firstChild;
                if (firstCell) {
                    firstCell.openEditor();
                }
            }
        }
    }
    
    editPreviousCell(cell) {
        let prevCell = cell.previousSibling;
        if (prevCell) {
            prevCell.openEditor();
        } else {
            // look at previous row
            let row = cell.parentNode;
            let prevRow = row.previousSibling;
            if (prevRow) {
                let lastCell = prevRow.lastChild;
                if (lastCell) {
                    lastCell.openEditor();
                } 
            }
        }
    }
    
    async addRow() {
        // async function addRow(tbody, columns, db, tableName, editNextCell, editPreviousCell) {
        const useColumns = this.tableColumns.filter(column => column.name !== 'id');
        const values = Array(useColumns.length);
        const resp = await fetch(`/databases/${this.db}/tables/${this.tableName}/rows`, {
            method: 'POST',
            body: JSON.stringify({
                columns: useColumns.map(column => column.name),
                values
            })
        });
        // TODO: error handling
        const row = await resp.json();
        const idColumn = this.tableColumns.find(c => c.name === 'id');
        const idCell = new DataCell(row, idColumn, this);
        const tr = el.tr(idCell);
        
        for (const column of useColumns) {
            row[column.name] = null;
            const cell = new DataCell(row, column, this);
            tr.appendChild(cell);
        }
        this.tbody.appendChild(tr);
    }
}

class DataCell extends HTMLTableCellElement {
    constructor(row, column, dataTable) {
        super();
        this.row = row;
        this.column = column;
        this.dataTable = dataTable;
        this.textInput = null;
        
        this.initialize();
    }
    
    initialize() {
        this.textContent = this.row[this.column.name];
        if (this.column.name === 'id') {
            this.classList.add('read-only');
        }
        if (this.column.name !== 'id') {
            this.addEventListener('dblclick', () => {
                this.openEditor();
            });
        }
    }
    
    openEditor() {
        const value = this.textContent;
        this.innerHTML = '';
        this.textInput = el.input({
            type: 'text',
            value,
            name: this.column.name,
            onKeypress: async e => {
                if (e.key === 'Enter') {
                    this.textInput.remove();
                }
            },
            onBlur: e => {
                this.saveAndCloseEditor();
            },
            onKeydown: async e => {
                if (e.key === 'Tab') {
                    e.preventDefault();
                    this.textInput.remove();
                    if (e.shiftKey) {
                        this.dataTable.editPreviousCell(this);
                    } else {
                        this.dataTable.editNextCell(this);
                    }
                } else if (e.key === 'Escape') {
                    // cancel
                    this.textInput.remove();
                    this.appendChild(text(this.row[this.column.name]));
                }
            }
        });
        this.appendChild(this.textInput);
        setTimeout(() => {
            this.textInput.focus();
            this.textInput.select();
        });
    }
    
    async saveAndCloseEditor() {
        if (!this.textInput) {
            return;
        }
        this.row[this.column.name] = this.textInput.value;
        this.textInput = null;
        const db = this.dataTable.db;
        const tableName = this.dataTable.tableName;
        const resp = await fetch(`/databases/${db}/tables/${tableName}/rows/${this.row.id}`, {
            method: 'PUT',
            body: JSON.stringify({
                columns: [this.column.name],
                values: [this.row[this.column.name]]
            })
        });
        const reply = await resp.json();
        if (reply.updated) {
            // TODO: error handling
            this.appendChild(text(this.row[this.column.name]));
        }
    }
}

customElements.define('data-table', DataTable, {
    extends: 'table'
});
customElements.define('data-cell', DataCell, {
    extends: 'td'
});