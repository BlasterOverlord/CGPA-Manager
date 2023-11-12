let rowCount = 0;

function remove(count) {
    let row = document.getElementById('row' + count);

    if (row) {
        row.parentNode.removeChild(row);
    }
}


function add() {
    let tableBody = document.getElementById('table-body');
    let newRow = tableBody.insertRow();
    newRow.id = 'row' + rowCount;
    newRow.innerHTML = '<td><div class="input-group mb-3"><input type="text" autocomplete="off" class="form-control mx-auto w-auto" name="course" placeholder="Course"></div></td><td><div class="input-group mb-3"><input type="number" required class="form-control mx-auto w-auto" name="credit" placeholder="Credit" step=".01" min="0" max="9"></div></td><td><div class="input-group mb-3"><input type="number" required class="form-control mx-auto w-auto" name="gpa" placeholder="GPA" step=".01" min="0" max="4"></div></td><td><a class="btn btn-danger btn-floating btn-sm mt-1 rounded-circle" onclick="remove('+ rowCount +')"><i class="bi bi-x"></i></a></td></tr>'
    rowCount++;
}
