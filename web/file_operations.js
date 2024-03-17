var currrentPath = "/";
function _getDirBox(){
    return document.getElementById("folders")
}

function _getDOMCurrentPath(){
    return document.getElementById("currentPath")
}

function _updateDOMCurrentPath(){
    _getDOMCurrentPath().innerText = currrentPath;
}

function _backToLastFolder(){
    if(currrentPath === "/"){
        return
    }
    let paths = currrentPath.split("/")
    if(paths.length === 0){
        return
    }

    let tempPath = "";
    console.log(paths)
    for(let i = 1; i < paths.length - 2; i++){
        let currentSlicePath = paths[i];
        tempPath = `${tempPath}/${currentSlicePath}`
    }
    if(tempPath === ""){
        tempPath = "/"
    }
    console.log(tempPath)
    // _set_path(tempPath)
    currrentPath = ""
    gotoDir(tempPath)
}
function _cleanDirBox(){
    let box = _getDirBox()
    if(!box){
        alert("Can not found DOM dir box")
        return
    }

    while(1){
    console.log(box.firstChild)
        let children = box.firstChild;
        if(!children){
            break
        }
        box.removeChild(children)
    }
}

function _set_path(path){
    if(typeof path !== "string"){
        alert(`path ${path} is not a string`)
        return false
    }
    if(path[path.length - 1] !== "/"){
        path = `${path}/`
    }
    currrentPath = path
    _updateDOMCurrentPath()
    return true
}

function _add_path(path){
    if(typeof path !== "string"){
        alert(`path ${path} is not a string`)
        return false
    }
    if(path[path.length - 1] !== "/"){
        path = `${path}/`
    }
    currrentPath = `${currrentPath}${path}`
    _updateDOMCurrentPath()
    return true
}


// Get files from the remote server
async function getFile(){
    let responseData = null;
    let response = await getWithToken(`/files/get_files?root=${currrentPath}`, false);
    if(response === undefined){
        return
    }
    try{
        responseData = await response.json();
        console.log(responseData)
        return responseData;
    }catch(e){
        alert(`Error when handling getFile's json parse: ${e}`)
        return
    }

}

function copyLink(text){
    navigator.clipboard.writeText(`${window.host}/${text}`)
}

function getCopyLinkButton(link){
    let button = document.createElement("button")
    button.innerText = "Copy"
    button.setAttribute("onclick", `copyLink("${link}")`)
    return button;
}

async function gotoDir(name){
    if(typeof name === "undefined"){
        name = ""
    }

    if(name !== ""){
        _add_path(name)
    }
    let data = await getFile();
    _cleanDirBox();
    if(typeof data === "undefined"){
        return
    }
    console.log(`This is the data before render: ${data}`)
    _renderFileBox(data)
}

function _renderFileBox(dirData){
    let dirBox = _getDirBox();
    if(!dirBox){
        alert("Can not found DOM dir box!")
        return
    }

    _cleanDirBox();
    let dirs = dirData['dirs'];
    console.log(dirData)
    for(let i = 0; i < dirs.length; i++){
        let dir = dirs[i];
        let name = dir["name"];
        let isDir = dir['dir'];
        let filePath = dir['path'];
        console.log(isDir)
        let fileElement = document.createElement("p");
        if(!isDir){
        // fileElement.innerText = name;
            let dirLink = document.createElement("a")
            dirLink.innerText = name;
            dirLink.href = filePath;
            dirLink.classList.add("file")
            fileElement.appendChild(dirLink)
            let button = getCopyLinkButton(filePath)
            fileElement.appendChild(button)
        } else {
            let dirLink = document.createElement("a")
            dirLink.innerText = name;
            dirLink.setAttribute("onclick", `gotoDir("${name}")`)
            dirLink.classList.add("folder")
            fileElement.appendChild(dirLink)
        }
        dirBox.appendChild(fileElement)
    }

}

async function uploadFile(){
    const fileInput = document.getElementById("fileInput");
    const file = fileInput.files[0];
    console.log(file);
    const form = new FormData();
    form.append("file", file);
    form.append("path", currrentPath);
    let response = undefined;
    try{
        response = await fetch(`${window.host}/files/upload_file`,
         {method: "POST", body: form, headers: {token: window.token}})
    }catch(e){
        console.log(e)
    }
    if(typeof response === "undefined" || response === null){
        alert("Upload file failed");
        return;
    }
    if(response.status === 401){
        alert("Please login first.")
        return
    } else if(response.status !== 200) {
        alert("Something went wrong.Please press F12 and check it.")
        return
    }
    alert("Upload success");
}
// getFile()
_updateDOMCurrentPath()
gotoDir("")
console.log(window.host)