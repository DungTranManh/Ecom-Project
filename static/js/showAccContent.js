var url_getalluserAPI = 'http://127.0.0.1:8000/api/getallusers';
var modal = document.getElementById('id01');

function start() {
    GetAllAcc(function(allAccs){
        RenderAllAcc(allAccs);
    });
    
}
start();


function showModal(user_id, usernameDeleted) {
    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
    if(document.getElementById("username_login").innerHTML != usernameDeleted){
        document.getElementById('id01').style.display='block';
        document.querySelector(".deletebtn").addEventListener("click", function(){
        fetch('http://127.0.0.1:8000/api/account/' + user_id, {
            method: 'DELETE',
        })
        .then(res => console.log(res))
        .then(function(){
            var itemDeleted = document.querySelector("#tr-" +user_id);
            if(itemDeleted){
                itemDeleted.remove();
            } 
        })
        document.getElementById('id01').style.display='none';
    });
    }else{
        document.getElementById('id02').style.display='block';
    }
    
}

function showEditModal(user_id_target, username_target, email_target, admin_target) {
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
    document.getElementById('username_target_input').value = username_target;
    document.getElementById('email_target_input').value = email_target;
    if(admin_target == "admin"){
        document.getElementById('admin_target_selector').value = "1";
    }else if (admin_target == "member"){
        document.getElementById('admin_target_selector').value = "0";
    }
    document.getElementById('EditModal').style.display='block';
}
    

// Fetch all account and render a view
function GetAllAcc(callback) {
    fetch(url_getalluserAPI)
    .then((response) => response.json())
    .then(callback)
}

function RenderAllAcc(allAccs) {
    var ContentOfTable = document.querySelector("#content-of-table");
    var html1 = allAccs.map(function(allAcc){
        if (allAcc.is_admin == 1){
            allAcc.is_admin = "admin";
        }else{
            allAcc.is_admin = "member";
        }
        return `
        <tr id = "tr-${allAcc.user_id}">
            <th scope="row" class="text-center">${allAcc.user_id}</th>
            <td align ="center">${allAcc.username}</td>
            <td align ="center">${allAcc.email}</td>
            <td align ="center">${allAcc.is_admin}</td>
            <td align ="center">
                <button type="button" class="btn btn-square btn-outline-warning m-2" onclick="showEditModal(${allAcc.user_id},'${allAcc.username}','${allAcc.email}','${allAcc.is_admin}');" ><i class="fas fa-user-edit"></i></button>
                <button type="button" class="btn btn-square btn-outline-danger m-2" onclick="showModal(${allAcc.user_id},'${allAcc.username}');" id = "${allAcc.user_id}""><i class="fas fa-user-minus"></i></button>
            </td>
        </tr>
        `;
    });

    ContentOfTable.innerHTML = html1.join("");   
}



