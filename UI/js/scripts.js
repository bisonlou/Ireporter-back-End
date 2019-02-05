

function register(){
  url = 'https://knightedge.herokuapp.com/api/v1/auth/signup';
  // url = 'http://127.0.0.1:5000/api/v1/auth/signup';

  headers = get_headers()
  body = JSON.stringify({
    'user_name': get_element_value('username'),
    'email': get_element_value('email'),
    'first_name': get_element_value('firstname'),
    'last_name': get_element_value('lastname'),
    'phone_number': get_element_value('phonenumber'),
    'password': get_element_value('password'),
    'other_names': get_element_value('othernames'),
    'is_admin': false
})

  fetch(url, {
    method: 'post',
    headers: headers,
    body: body
    })
  .then(response => {
    return response.json();
  }).then(data => {
    if (data['status'] == 201){
      navigate_to("login.html");      
    }
    else {
      display_errors(data);
    }
  }).catch(err => {
    console.log(err);
  });
}

function login(){
  url = 'https://knightedge.herokuapp.com/api/v1/auth/login';
  // url = 'http://127.0.0.1:5000/api/v1/auth/login';

  body = JSON.stringify({
    'email': get_element_value('email'),
    'password': get_element_value('password')
  });

  headers = get_headers();

  fetch(url,{
    method: 'post',
    headers: headers,
    body: body
    })
  .then(response => {
    return response.json();

  }).then(data => {
    if (data['status'] == 200){
      set_cookie(data);  
      navigate_to("index.html")
    }  
    else {
      display_errors(data);
    }      

  }).catch(err => {
    console.log(err);

  });
}


function getRedflags(){
  url = 'https://knightedge.herokuapp.com/api/v1/redflags';
  // url = 'http://127.0.0.1:5000/api/v1/redflags';

  fetch(url, {
    headers: get_headers()
    })

  .then(response => {
    return response.json();
  }).then(data => {

    if (data['status'] == 401){
      navigate_to('login.html')
    }
    
    table = get_element('redflag-table');
    populate_incident_table(data, table, 'red-flag')  
    update_dashboard(data, 'red-flag')  
  
  }).catch(err => {
    console.log(err);
  });
}

function getInterventions(){
  url = 'https://knightedge.herokuapp.com/api/v1/interventions';
  // url = 'http://127.0.0.1:5000/api/v1/interventions';

  fetch(url,{
    headers: get_headers()
    })

  .then(response => {
    return response.json();
  }).then(data => {

    if (data['status'] == 401){
      navigate_to('login.html');
    }    

    table = document.getElementById('intervention-table');
    populate_incident_table(data, table, 'intervention');
    update_dashboard(data, 'intervention')
  
  }).catch(err => {
    console.log(err);
  });
}



function postIncident(incidentType){
  url = 'https://knightedge.herokuapp.com/api/v1/incidents';
  // url = 'http://127.0.0.1:5000/api/v1/incidents';
  
  body = JSON.stringify({
    'title': get_element_value('title'),
    'comment': get_element_value('comment'),
    'location': '(00.000000, 00.000000)',
    'type': incidentType,
    'status': 'pending',
    'images': ['image_001.jpg'],
    'videos': ['video_001.mp4']
  })

  fetch(url, {
    method: 'post',
    body: body,
    headers: get_headers()
    })

  .then(response => {
    return response.json();
  }).then(data => {
    if (data['status'] == 201){
      navigate('index.html');
    }
  }).catch(err => {
    console.log(err);
  });
}

function putIncident(){
  url = '';
  if (incidentType == 'red-flag'){
    url = url = 'https://knightedge.herokuapp.com/api/v1/redflags/' + incidentId;
    // url = url = 'http://127.0.0.1:5000/api/v1/redflags/' + incidentId;
  }
  if (incidentType == 'intervention'){
    url = 'https://knightedge.herokuapp.com/api/v1/interventions/' + incidentId;
    // url = 'http://127.0.0.1:5000/api/v1/interventions/' + incidentId;
  }
  
  body = JSON.stringify({
    'title': get_element_value('title'),
    'comment': get_element_value('comment'),
    'location': '(00.000000, 00.000000)',
    'type': incidentType,
    'status': 'pending',
    'images': ['image_001.jpg'],
    'videos': ['video_001.mp4']
  })

  fetch(url, {
    method: 'post',
    body: body,
    headers: get_headers()
    })

  .then(response => {
    return response.json();
  }).then(data => {
    if (data['status'] == 201){
      navigate('index.html');
    }
  }).catch(err => {
    console.log(err);
  });
}

function getIncident(){
  var url = window.location.href;
  var incidentType = /type=([^&]+)/.exec(url)[1];
  var incidentId = /id=([^&]+)/.exec(url)[1];
  incidentId = parseInt(incidentId, 10)

  title = get_element('title');
  comment = get_element('comment');

  url = '';
  if (incidentType == 'red-flag'){
    url = url = 'https://knightedge.herokuapp.com/api/v1/redflags/' + incidentId;
    // url = url = 'http://127.0.0.1:5000/api/v1/redflags/' + incidentId;
  }
  if (incidentType == 'intervention'){
    url = 'https://knightedge.herokuapp.com/api/v1/interventions/' + incidentId;
    // url = 'http://127.0.0.1:5000/api/v1/interventions/' + incidentId;
  }

  fetch(url,{
    method: 'get',
    headers: get_headers()
    })

  .then(response => {
    return response.json();
  }).then(data => {
    if (data['status'] == 201){
      navigate_to('index.html')
    }

    title.value = data['data'][0]['title'];
    comment.innerHTML = data['data'][0]['comment'];

  }).catch(err => {
    console.log(err);
  });

}

function get_headers(){
  return {
    'Content-Type': 'application/json',
    'Authorization': document.cookie
  }
}

function get_element_value(element_id){
  return document.getElementById(element_id).value
}

function get_element(element_id){
  return document.getElementById(element_id)
}

function display_errors(data){
  message_div = document.getElementById('messages');
  errors= data['errors'];

  for (i=0; i<errors.length; i++){
    var paragraph = document.createElement("P");
    paragraph.style = "color:red";
    var error = document.createTextNode(errors[i]);

    paragraph.appendChild(error); 
    message_div.appendChild(paragraph);
  }
}

function navigate_to(page){
  window.location.href = "https://bisonlou.github.io/ireporter/UI/" + page ;
}

function set_cookie(data){
  token = data['data'][0]['access_token'];
  bearer_token = "Bearer " + token + ";";
  document.cookie = "token=" + bearer_token;
}

function populate_incident_table(data, table, type){
    for(i=0; i< (data['data'][0]).length; i++){
      var row = table.insertRow(i + 1);
      
      var cell1 = row.insertCell(0);
      var cell2 = row.insertCell(1);
      var cell3 = row.insertCell(2);
      var cell4 = row.insertCell(3);

  incidentId = data['data'][0][i]['id'];
  long_date_time = new Date(data['data'][0][i]['createdon']);

  var months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  var days = ["Sun", "Mon", "Tue", "Wed", "Thur", "Fri", "Sat"];

  month = months[long_date_time.getMonth()];
  day = days[long_date_time.getDay()];
  year = long_date_time.getFullYear();
  date = long_date_time.getDate();

  if(date < 10){
      date = "0" + date;
    }

  display_date = day + " " + date + " " + month + " " + year;

  cell1.innerHTML = display_date;
  cell2.innerHTML =  data['data'][0][i]['title'];
  cell3.innerHTML =  data['data'][0][i]['status'];
  cell4.innerHTML =  '<a href="./incident_edit.html?type=' + type + '&id=' + incidentId +
                    '">Edit</a> | <a href="./incident_confirm_delete.html?type=' + type + '&id=' + incidentId +
                    '">Delete</a>';

  }
}

function update_dashboard(data, type) {
  if (type == 'red-flag'){

    get_element('total-redflags').innerHTML = data['totals']['total']['count']
    get_element('pending-redflags').innerHTML = data['totals']['pending']['count']
    get_element('rejected-redflags').innerHTML = data['totals']['rejected']['count']

  }
  if (type == 'intervention'){

    get_element('total-interventions').innerHTML = data['totals']['total']['count']
    get_element('pending-interventions').innerHTML = data['totals']['pending']['count']
    get_element('rejected-interventions').innerHTML = data['totals']['rejected']['count']

  }
}