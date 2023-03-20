<!-- Login HTML Template sourced from https://www.w3schools.com/howto/howto_css_login_form.asp -->

<!DOCTYPE html>
<html lang="en-US">
<head>
<style>
input[type=text], input[type=password] {
  width: 250px;
  padding: 12px 20px;
  margin: 16px 0;
  display: inline-block;
  border: 1px solid #ccc;
  box-sizing: border-box;
}

<!--classes-->

button {
  background-color: #04AA6D;
  color: white;
  padding: 14px 20px;
  margin: 8px 0;
  border: none;
  cursor: pointer;
  width: 100%;
}
button:hover {
  opacity: 0.5;
}

.cancelbtn {
  width: auto;
  padding: 10px 18px;
  background-color: #f44336;

}
.makeacc{
 width: auto;  
 padding: 10px 18px;
 background-color: yellow;

}
.container {
  padding: 16px;
}

span.psw {
  float: right;
  padding-top: 16px;
}
.title {
  text-align: center;
}

</style>
</head>
<body>
<div class="title">
    <h1>Clinic Website  </h1>
</div>
<h2>Create New Account</h2>



<form action="/login.php" method="post">
  <div class="container">
    
    <label for="username"><b>Username</b></label>
    <input type="text" placeholder="Enter Username" name="username" required>
    <label for="psw"><b>Password</b></label>
    <input type="password" placeholder="Enter Password" name="psw" required>
    <button type="submit">Create Account</button>
    <p style="color:red;">Password Requirements</p>
    <p>Must not contain your first or last name</p>
    <p>Must be length of 6 or more</p>
    
    <!--Remember me Checkbox, functionality non-existant-->
    <!--label>
      <input type="checkbox" checked="checked" name="remember"> Remember me
    </label-->
  </div>
<!-- need to incorporate new page for Forgot Password-->
  <div class="container" style="background-color:#f1f1f1">
    <button type="button" class="cancelbtn"><a href="{% url 'Login' %}">Cancel</a></button>
  

    <!--

        <button type="button" class="makeacc"><a href="_blank">Make New Account</a></button>
    -->
    
  </div>
 
</form>


</body>
</html>