var drone_port = 3000;
var server_port = 3000;

window.oncontextmenu = function ()
{return false;}

function move_element(elem){
    if(!check_right_click()){
        let flag = false
        let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0
        parent_ele = elem.parentElement
        parent_ele.onmousedown = dragMouseDown
        function dragMouseDown(){
            e = window.event
            pos3 = e.clientX
            pos4 = e.clientY
            document.onmouseup = closeDragElement
            document.onmousemove = elementDrag
        }

        function elementDrag(){
            e=window.event
            pos1 = pos3 - e.clientX;
            pos2 = pos4 - e.clientY;
            pos3 = e.clientX;
            pos4 = e.clientY;
            parent_ele.style.top = (parent_ele.offsetTop - pos2) + "px";
            parent_ele.style.left = (parent_ele.offsetLeft - pos1) + "px";
        }
        function closeDragElement(){
            document.onmousemove = null
            document.onmouseup = null
            flag = true
        }
    }   
}

function check_right_click() {
    var isRightMB;
    e = window.event;
    if ("which" in e)
        isRightMB = e.which == 3; 
    else if ("button" in e)
        isRightMB = e.button == 2; 
    console.log(isRightMB)
    return isRightMB;
} 
function click_drone(){
    if(check_right_click())
        alert("you clicked a drone")
}
function click_server(){
    if(check_right_click())
        alert("you clicked a server")
}
function add_drone(){
    drone_address = `http://127.0.0.2:${drone_port}`
    
    let elem_div = document.createElement('div')
    elem_div.className = "drone-object"
    elem_div.id = drone_address
    elem_div.onclick = click_drone
    elem_div.style.cssText = 'position:absolute;'
    let img = document.createElement('img')
    elem_div.appendChild(img)
    img.onmousedown = move_element(img)
    img.id = drone_address+'img'
    img.src ="images/drone.png"
    img.title = drone_address
    document.body.appendChild(elem_div);
    drone_port +=1
}

function add_server(){
    server_address = `http://127.0.0.1:${server_port}`
    let elem_div = document.createElement('div')
    elem_div.className = "server-object"
    elem_div.id = server_address
    elem_div.onclick = click_server
    elem_div.style.cssText = 'position:absolute;'
    let img = document.createElement('img')
    elem_div.appendChild(img)
    img.onmousedown = move_element(img)
    img.src ="images/server.png"
    img.title = server_address
    document.body.appendChild(elem_div);
    server_port +=1
}