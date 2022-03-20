function searchByName(event){
    const tBody = table.tBodies[0];
    const rows = Array.from(tBody.querySelectorAll("tr"));
    // for (var i = 0; i < rows.length - 500, ++i;){
    //     console.log(rows[i].style.display + 'a');
    //     rows[i].style.display = '';
    // }
    for (var i = 0; i < rows.length, ++i;){
        var name = rows[i].cells[1].innerText.trim().toLowerCase();
        if(!name.includes(event.target.value)){
            rows[i].style.display = 'none';
        }
    }
}


var table = document.querySelector('.table-sortable');
document.querySelector('#search-data').addEventListener("input", searchByName);