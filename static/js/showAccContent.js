var url_getalluserAPI = 'http://127.0.0.1:8000/api/getallusers'
function start() {
    GetAllAcc(function(allAccs){
        RenderAllAcc(allAccs);
    });
}
start();


// Fetch all account and render a view
function GetAllAcc(callback) {
    fetch(url_getalluserAPI)
    .then((response) => response.json())
    .then(callback)
}

function RenderAllAcc(allAccs) {
    var ContentOfTable = document.querySelector("#content-of-table");
    var html = allAccs.map(function(allAcc){
        if (allAcc.is_admin == 1){
            allAcc.is_admin = "admin";
        }else{
            allAcc.is_admin = "member";
        }
        return `
        <tr>
            <th scope="row" class="text-center">${allAcc.user_id}</th>
            <td align ="center">${allAcc.username}</td>
            <td align ="center">${allAcc.email}</td>
            <td align ="center">${allAcc.is_admin}</td>
            <td align ="center">
                <button type="button" class="btn btn-square btn-outline-warning m-2"><i class="fas fa-user-edit"></i></button>
                <button type="button" class="btn btn-square btn-outline-danger m-2" id = "delete-item-${allAcc.user_id}"><i class="fas fa-user-minus"></i></button>
            </td>
        </tr>
        `;
    });
    ContentOfTable.innerHTML = html.join("");
}


