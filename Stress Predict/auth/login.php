<?php
include 'db.php';

$username = $_POST['username'];
$password = $_POST['password'];

$query = "SELECT * FROM users WHERE username='$username' AND password='$password'";
$result = $conn->query($query);

if ($result->num_rows > 0) {
    session_start();
    $user = $result->fetch_assoc();
    $_SESSION['first_name'] = $user['first_name'];
    $_SESSION['last_name'] = $user['last_name'];
    echo json_encode(["success" => true, "username" => $username]);
} else {
    echo json_encode(["success" => false]);
}
?>
