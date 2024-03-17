var token = "";

function getToken(){
    localToken = localStorage.getItem("token");
    return localToken;
}

function setToken(token){
    localStorage.setItem("token", token);
}

function initToken(){
    let localToken = getToken();
    if(localToken !== "" && localToken !== null){
        token = localToken
    }
}

async function login(){
    // Login and set the lcoalStorage
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;
    if (username === "" || password === ""){
        alert("Please enter your username or password")
        return
    }

    let resp = await sendJSONWithToken("/users/login", {username: username, password: password}, true)
    try{
        resp = await resp.json()
    } catch(e){
        alert(`Login error: Can not parse response to json: ${e}`)
        return
    }

    localStorage.setItem("token", resp.token)
    token = resp.token
    gotoDir("")
}
initToken()