<h1>Meeting room api</h1>

<h3>Information</h3>
<li>Postresql database is used and pushed to the cloud using AWS RDS</li>
<li>JWT is used for authorization of employees </li>
<li>API built using django and django rest framework and pushed to docker - https://hub.docker.com/r/arun445/meeting_room </li>



<h3>Instructions on how to use meeting room api:</h3>

All the API urls:
<li>/api/token/refresh/</li>
<li>/api/login/</li>
<li>/api/users/</li>
<li>/api/users/register/</li>
<li>/api/users/str:pk/</li>
<li>/api/rooms/</li>
<li>/api/rooms/create/</li>
<li>/api/rooms/str:pk/</li>
<li>/api/reservations/create/</li>
<li>/api/reservations/delete/str:pk/</li>

<h3>Authentication.</h3>
<ul>
<li>Register an employee using '/api/users/register/', this api takes in first_name, last_name, email, password.</li>
<li>Login with email and password in '/api/login/'. Api will output an access token and a refresh token. </li>
<li>Using that access token you can access other apis. Usage example {"Authorization" : "Bearer access:token"}</li>
</ul>
<h3>Using further apis, you must pass in the access token as authorization</h3>
<img>
<h3>Create a room</h3>
<ul>
<li>Create a room using '/api/rooms/create/', this api takes in name as an argument  </li>
</ul>
<h3>Create a reservation</h3>
<li>First check the meeting room for reservation availabilities using '/api/rooms/str:pk/', this api takes in the id of the room.</li>
<li>You can also filter the meeting room reservations by specific employee names./li>
<li>Then check all the available employees using '/api/users/', which lists all the emoplyees. </li>
<li>Before inviting employees to the room reservation, check if they have reservations on that time using '/api/users/str:pk/', this api takes in the id of the employee and outputs all employees reservation times.</li>
<li>Create a reservation using '/api/reservations/create/', this api takes in a title, reserved_from, reserved_to, room id where you want to create the reservation, and employees the ones you want to invite to the room (as a list of ids).</li>
<li>Invited employees will be reserved for that time automatically. </li>
<h3>Cancel a reservation</h3>
<li>If you are a reservations author you can easily cancel a reservation using '/api/reservations/delete/str:pk/', this api takes in the reservations id.</li>

