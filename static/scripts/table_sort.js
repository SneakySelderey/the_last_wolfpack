"use strict"

function sortTableByColumn(column, asc = true) {
    const dirModifier = asc ? 1 : -1;
    const tBody = table.tBodies[0];
    const rows = Array.from(tBody.querySelectorAll("tr"));

    const sortedRows = rows.sort((a, b) => {
        if (column !== 0){
            var aColText = a.querySelector(`td:nth-child(${ column + 1 })`).textContent.trim();
            var bColText = b.querySelector(`td:nth-child(${ column + 1 })`).textContent.trim();
        }
        else {
            var aColText = a.querySelector(`td:nth-child(${ column + 1 })`);
            var bColText = b.querySelector(`td:nth-child(${ column + 1 })`);
        }

        return aColText > bColText ? (1 * dirModifier) : (-1 * dirModifier);
    });
    var newBody = document.createElement('tbody');
    tBody.parentNode.replaceChild(newBody, tBody)
    newBody.append(...sortedRows);
}

var table = document.querySelector('.table-sortable');
document.querySelector('#sort_id').addEventListener("click", () => sortTableByColumn(0, true));
document.querySelector('#sort_alph').addEventListener("click", () => sortTableByColumn(1, true));
document.querySelector('#sort_alph_rev').addEventListener("click", () => sortTableByColumn(1, false));