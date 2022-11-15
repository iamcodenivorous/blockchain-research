var drone_port = 3000;
var server_port = 3000;
var clicked = 'null'
var id = 'none'
var server_list = []
var drone_list = []


document.oncontextmenu = ()=> {return false};
document.onclick = hideMenu;
function hideMenu() {
    document.getElementById("context-menu-server").style.display = 'none'
    document.getElementById("context-menu-drone").style.display = 'none'
}

function adjustLine(from, to, line){
  var fT = from.offsetTop  + from.offsetHeight/2;
  var tT = to.offsetTop    + to.offsetHeight/2;
  var fL = from.offsetLeft + from.offsetWidth/2;
  var tL = to.offsetLeft   + to.offsetWidth/2;
  var CA   = Math.abs(tT - fT);
  var CO   = Math.abs(tL - fL);
  var H    = Math.sqrt(CA*CA + CO*CO);
  var ANG  = 180 / Math.PI * Math.acos( CA/H );
  if(tT > fT)
      var top  = (tT-fT)/2 + fT;
  else
      var top  = (fT-tT)/2 + tT;
  if(tL > fL)
      var left = (tL-fL)/2 + fL;
  else
      var left = (fL-tL)/2 + tL;
  if(( fT < tT && fL < tL) || ( tT < fT && tL < fL) || (fT > tT && fL > tL) || (tT > fT && tL > fL))
    ANG *= -1;
  top-= H/2;
  line.style.transform = 'rotate('+ ANG +'deg)';
  line.style.top    = top+'px';
  line.style.left   = left+'px';
  line.style.height = H + 'px';
}

function rightClick(e) {
    e.preventDefault()
    hideMenu();
    if(clicked == 'server'){
        var menu = document.getElementById("context-menu-server")
        id = e.currentTarget.id
        clicked = 'none'
    }
    else if(clicked == 'drone'){
        var menu = document.getElementById("context-menu-drone")
        id = e.currentTarget.id
        clicked = 'none'
    }
    else{
        hideMenu()
        id = 'none'
        return
    } 
    menu.style.display = 'block';
    menu.style.left = e.clientX + "px";
    menu.style.top = e.clientY + "px";
}

function move_element(evt){
    let flag = false
    let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0
    parent_ele = evt.currentTarget.parentNode;
    e = window.event
    pos3 = evt || e.clientX
    pos4 = evt || e.clientY
    document.onmousemove = elementDrag
    document.onmouseup = closeDragElement
    get_servers()
    get_drones()
    function elementDrag(){
        e=window.event
        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;
        parent_ele.style.top = (parent_ele.offsetTop - pos2) + "px";
        parent_ele.style.left = (parent_ele.offsetLeft - pos1) + "px";
    }
    function closeDragElement(evt){
        document.onmousemove = null
        document.onmouseup = null
        if(evt.target.parentNode.className == "drone-object")
            handle_drag(evt);
    }
}

function handle_drag(event) {
    const droneRect = event.target.parentNode.getBoundingClientRect();
    if(server_list.length > 0){
        for(let server in server_list){
            let server_div = document.getElementById(server_list[server])
            const serverRect = server_div.getBoundingClientRect();
            drone_address = event.target.parentNode.id
            server_address = server_list[server]
            if(!(droneRect.top > serverRect.bottom ||droneRect.right < serverRect.left || droneRect.bottom < serverRect.top || droneRect.left > serverRect.right)){
                fetch(`${server_address}/add-drone`, {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(
                    {
                        "drone_address": drone_address,
                    }
                )
                })
                .then(response => {
                    if(response.status == 200)
                        alert("Drone connected to server.")
                })

            }else{
                fetch(`${server_address}/remove-drone`, {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(
                    {
                        "drone_address": drone_address,
                    }
                )
                })
                .then(response => {
                    //if(response.status == 200)
                        //alert("Drone removed.")
                })
            }
        }
    }
}


function add_drone(){
    fetch('http://127.0.0.1:5000/start/drone', {
    method: 'POST',
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(
        {
            "ip": "127.0.0.2",
            "port": drone_port
        }
    )
    })
    .then(response => {
        if(response.status == 200){
            drone_address = `http://127.0.0.2:${drone_port}`
            let elem_div = document.createElement('div')
            elem_div.className = "drone-object"
            elem_div.addEventListener('contextmenu', function(ev) {
                ev.preventDefault();
                clicked = 'drone';
                rightClick(ev);
                return false;
            }, false);
            elem_div.id = drone_address
            elem_div.style.cssText = 'position:absolute;'
            let img = document.createElement('img')
            elem_div.appendChild(img)
            img.onmousedown = move_element
            img.id = drone_address+'img'
            img.src ="images/drone.png"
            img.title = drone_address
            document.body.appendChild(elem_div);
            drone_list.push(drone_address)
            drone_port +=1
            alert("Drone Added...")

        }
    })
}

function add_server(){
    fetch('http://127.0.0.1:5000/start/server', {
    method: 'POST',
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(
        {
            "ip": "127.0.0.1",
            "port": server_port
        }
    )
    })
    .then(response => {
        if(response.status == 200){
            server_address = `http://127.0.0.1:${server_port}`
            let elem_div = document.createElement('div')
            elem_div.className = "server-object"
            elem_div.addEventListener('contextmenu', function(ev) {
                ev.preventDefault();
                clicked = 'server';
                rightClick(ev);
                return false;
            }, false);
            elem_div.id = server_address
            elem_div.style.cssText = 'position:absolute;'
            let img = document.createElement('img')
            elem_div.appendChild(img)
            img.onmousedown = move_element
            img.src ="images/server.png"
            img.title = server_address
            document.body.appendChild(elem_div);
            server_list.push(server_address)
            server_port +=1
            alert("Server Added...")
        }
    })
}

function connect_server(){
    address = prompt('Insert address of server:', 'http://')
    if(address != null && address.length > 5 && server_list.includes(address)){
         fetch(`${id}/register-and-broadcast-node`, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(
                {
                    "new_node_url":address
                }
            )
            })
            .then(response => {
                if(response.status == 200){
                    get_servers();
                }
            })
    }else{
        alert("Server not found....")
    }
}

function get_servers(){
    document.querySelectorAll('.line').forEach(e => e.remove());
    const liners = new Set()
    server_list.forEach(server =>
        fetch(`${server}/get-connected-servers`, {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        })
        .then((response) => response.json())
        .then(data =>{
            servers = data["servers"]
            servers.forEach(s=>{
                if(!(liners.has(s+'to'+server) || liners.has(server+'to'+s))){
                    let line = document.createElement('div')
                    line.className = "line"
                    document.body.appendChild(line);
                    adjustLine(document.getElementById(server), 
                    document.getElementById(s),
                    line)
                    liners.add(s+'to'+server)
                }
            })
        })
    )
}

function get_drones(){
    document.querySelectorAll('.line-2').forEach(e => e.remove());
    const liners = new Set()
    drone_list.forEach(drone =>
        fetch(`${drone}/get-connected-drones`, {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        })
        .then((response) => response.json())
        .then(data =>{
            drones = data["drones"]
            drones.forEach(d=>{
                if(!(liners.has(d+'to'+drone) || liners.has(drone+'to'+d))){
                    let line = document.createElement('div')
                    line.className = "line-2"
                    document.body.appendChild(line);
                    adjustLine(document.getElementById(drone), 
                    document.getElementById(d),
                    line)
                    liners.add(d+'to'+drone)
                }
            })
        })
    )
}

function view_drone_data(){
    window.open(`${id}/drone`, '_blank');
}

function add_drone_data(){
    let input = prompt("Enter drone data \n(Format: cordinate => data)").split('=>')
    if(input.length > 1){
        cordinate = input[0].trim()
        data = input[1].trim()
        if(cordinate.length > 0 && data.length > 0){
            fetch(`${id}/add-data`, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(
                {
                    "cordinate": cordinate,
                    "data": data
                }
            )
            })
            .then(response => {
                if(response.status == 200){
                    alert("Data added successfully...")
                }
            })
        }else{
            alert("Enter valid data")
        }
    }else{
        alert("Enter data in data specified format")
    }
}

function display_data(){
    window.open(`${id}/blockchain`, '_blank');
}

function mine_data(){
    fetch(`${id}/mine`, {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if(response.status == 200){
            alert("data mined successfully");
        }
    })   
}

function add_neighbour_drone(){
    corrent_drone = id    
    let neighbour_drone_address = prompt("Enter neighbour drone address:", 'http://')
    if(neighbour_drone_address.length > 8 && drone_list.includes(neighbour_drone_address)){
        fetch(`${id}/add-neighbour-drone`, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(
            {
                "drone_address": neighbour_drone_address,
            }
        )
        })
        .then(response => {
            if(response.status == 200){
                get_drones()
                alert("Drone connected successfully...")
            }
        })
    }else{
        alert("Drone not found")
    }
}

function get_data(){
    let drone_address = prompt("Enter drone address:", "http://")
    if(drone_address.length > 8 && drone_list.includes(drone_address)){

        fetch(`${id}/get-data-from-drone`, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(
            {
                "drone_address": drone_address,
            }
        )
        })
        .then(response => {
            if(response.status == 200){
                get_drones()
                alert("Drone connected successfully...")
            }else if(response.status == 404){
                alert("Drone not connected to server...")
            }
        })
    }else{
        alert('Drone drone not found')
    }

}

function get_all_data(){
    fetch(`${id}/get-all-data-from-drones`, {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }})
        .then(response => {
            if(response.status == 200){
                alert("Data added successfully...")
            }else if(response.status == 404){
                alert("No drones connected to server...")
            }
        })
}

function disconnect_fanet(){
    fetch(`${id}/disconnect-fanet`, {
    method: 'GET',
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }})
    .then(response => {
        if(response.status == 200){
            alert("Drone Disconnected from fanet...")
            get_drones();
        }else if(response.status == 400){
            alert("Drone not connected to any fanet...")
        }
    })
}