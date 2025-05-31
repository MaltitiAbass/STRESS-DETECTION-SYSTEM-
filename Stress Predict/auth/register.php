<?php
include 'db.php';

$first_name = $_POST['first_name'];
$last_name = $_POST['last_name'];
$email = $_POST['email'];
$phone_number = $_POST['phone_number'];
$username = $_POST['first_name'] . " " . $_POST['last_name'];
$password = $_POST['password'];

$query = "INSERT INTO users (first_name, last_name, email, phone_number, username, password) 
          VALUES ('$first_name', '$last_name', '$email', '$phone_number', '$username', '$password')";

if ($conn->query($query) === TRUE) {
    echo json_encode(["success" => true]);
} else {
    echo json_encode(["success" => false, "error" => $conn->error]);
}
?>
