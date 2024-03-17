window.host = "http://localhost:8001"

async function sendJSONWithToken(url, payload, noToken){
    console.log(url)
    console.log(payload)
    let resp = undefined;
    try{
        if(noToken){
            resp = await fetch(`${window.host}${url}`, {
                method: "POST",
                body: JSON.stringify(payload),
                headers: {"Content-Type": "application/json"}
            })

        } else {
            resp = await fetch(`${window.host}${url}`, {
                method: "POST",
                body: JSON.stringify(payload),
                headers: {"Content-Type": "application/json", "token": window.token},
            })
        }
    } catch(e){
        alert(`[POST]Something went wrong when access login API: ${e}`)
        return undefined;
    }
    if(resp.status === 401){
        alert("Please login before you request.")
        return undefined;
    }
    return resp;

}

async function getWithToken(url, noToken){
    let headers;
    if(!noToken){
        headers = {token: window.token? window.token : ""};
    } else {
        headers = {};
    }
    let response = undefined;
    try{
        response = await fetch(`${window.host}${url}`, {method: "GET", headers: headers})
    }catch(e){
        alert(`[GET]Error when handling ${url}: ${e}`)
        return undefined;
    }
    if(response === null){
        console.log("it's null")
        return undefined;
    }
    if(response.status === 401){
        alert("Please login before you requset.")
        return undefined;
    }
    return response;
}